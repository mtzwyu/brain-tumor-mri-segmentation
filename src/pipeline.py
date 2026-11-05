"""Class điều phối toàn diện BrainTumorPipeline kết nối 4 tầng xử lý ảnh số.

Quy trình khép kín:
Ảnh gốc MRI -> Lọc nhiễu Bilateral & CLAHE -> Tách sọ (Skull Stripping) 
           -> Phân đoạn u (Watershed / Region Growing) 
           -> Trích xuất đặc trưng & Bounding Box 
           -> Đánh giá định lượng so với Ground Truth (nếu có).
"""

from typing import Tuple, Optional, Dict, Any
import numpy as np

from src.preprocessing.filters import apply_bilateral_filter, apply_clahe
from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed
from src.segmentation.region_growing import segment_region_growing
from src.measurement.features import extract_tumor_features, DiagnosticResult
from src.measurement.visualization import draw_tumor_overlay, create_comparison_quad
from src.evaluation.metrics import calculate_dice, calculate_iou


def verify_tumor_presence(
    brain_image: np.ndarray,
    brain_mask: Optional[np.ndarray] = None,
    z_thresh: float = 2.3,
    min_brain_pixels: int = 100
) -> bool:
    """Kiểm tra sự tồn tại của tổn thương tăng sáng bất thường (Clinical Anomaly Gate).
    
    Trong xử lý ảnh y tế cổ điển (DIP):
    Khối u não trên ảnh MRI FLAIR/T1-CE là tổn thương tăng quang bất thường (Hyper-intense lesion)
    so với phân bố đồng nhất của nhu mô não lành. Nếu điểm sáng cực đại không đạt Z-score tối thiểu
    (z_max < z_thresh) hoặc khoang não quá nhỏ (< min_brain_pixels), lát cắt được kết luận là Não lành.
    
    Args:
        brain_image: Ảnh xám nhu mô não đã tách sọ (H, W), uint8.
        brain_mask: Mặt nạ nhị phân nhu mô não (H, W), uint8 {0, 255}.
        z_thresh: Ngưỡng Z-score tối thiểu của điểm cực đại trong não (mặc định 2.3).
        min_brain_pixels: Số pixel tối thiểu của khoang sọ não để tiến hành phân đoạn.
        
    Returns:
        bool: True nếu phát hiện dấu hiệu bất thường u não, False nếu là mô não lành tính.
    """
    if brain_mask is not None:
        brain_pixels = brain_image[brain_mask > 0]
    else:
        brain_pixels = brain_image[brain_image > 0]

    if len(brain_pixels) < min_brain_pixels:
        return False

    mean_val = float(np.mean(brain_pixels))
    std_val = float(np.std(brain_pixels))
    if std_val <= 1e-3:
        return False

    max_val = float(np.max(brain_pixels))
    z_max = (max_val - mean_val) / std_val

    return bool(z_max >= z_thresh)


class BrainTumorPipeline:
    """Hệ thống điều phối xử lý ảnh số chẩn đoán khối u não MRI."""

    def __init__(self, method: str = "watershed", params: Optional[Dict[str, Any]] = None) -> None:
        """Khởi tạo pipeline với phương pháp phân đoạn mong muốn.
        
        Args:
            method: 'watershed' (Baseline chính) hoặc 'region_growing' (Đối chứng).
            params: Dictionary chứa các siêu tham số tùy chỉnh:
                - dist_thresh_ratio (float): Tỷ lệ ngưỡng khoảng cách cho Watershed (mặc định 0.4).
                - intensity_tolerance (int): Dung sai độ sáng cho Region Growing (mặc định 15).
                - min_tumor_area (int): Diện tích tối thiểu để công nhận là u (mặc định 50).
                - enable_presence_gate (bool): Bật/tắt bộ lọc sàng lọc não lành tính (mặc định True).
                - z_thresh (float): Ngưỡng Z-score kiểm định u (mặc định 2.3).
                - min_contrast_ratio (float): Ngưỡng tương phản tối thiểu giữa u và não lành (mặc định 0.15).
        """
        self.method = method.lower()
        self.params = params or {}

    def process(
        self,
        image: np.ndarray,
        gt_mask: Optional[np.ndarray] = None
    ) -> Tuple[DiagnosticResult, Dict[str, np.ndarray]]:
        """Thực thi toàn bộ pipeline xử lý từ ảnh đầu vào đến kết quả đo lường và hình ảnh trực quan.
        
        Args:
            image: Ảnh MRI gốc (H, W), uint8.
            gt_mask: Mặt nạ Ground Truth (nếu có để tính Dice/IoU).
            
        Returns:
            Tuple[DiagnosticResult, Dict[str, np.ndarray]]:
                - DiagnosticResult: Chứa diện tích, tỷ lệ, độ tròn, bbox, Dice, IoU.
                - Dict: Các ảnh trung gian {'original', 'filtered', 'stripped', 'tumor_mask', 'overlay', 'quad'}.
        """
        # 1. Tiền xử lý lọc nhiễu
        filtered = apply_bilateral_filter(image)

        # 2. Tách sọ não (Skull Stripping)
        stripped_brain, brain_mask = strip_skull(filtered)

        # 3. Kiểm định sàng lọc bất thường y sinh (Lớp 1: Clinical Anomaly Gate)
        enable_gate = self.params.get("enable_presence_gate", True)
        z_thresh = self.params.get("z_thresh", 2.3)
        has_tumor_signs = True
        if enable_gate:
            has_tumor_signs = verify_tumor_presence(stripped_brain, brain_mask, z_thresh=z_thresh)

        # 4. Phân đoạn khối u theo phương pháp đã chọn (Strategy Pattern)
        if not has_tumor_signs:
            tumor_mask = np.zeros_like(stripped_brain, dtype=np.uint8)
        elif self.method == "region_growing":
            tol = self.params.get("intensity_tolerance", 15)
            tumor_mask = segment_region_growing(stripped_brain, tolerance=tol)
        else:
            ratio = self.params.get("dist_thresh_ratio", 0.4)
            min_area = self.params.get("min_tumor_area", 50)
            tumor_mask = segment_watershed(stripped_brain, dist_thresh_ratio=ratio, min_tumor_area=min_area)

        # 5. Kiểm định độ tương phản vùng tổn thương ứng viên (Lớp 2: Candidate Contrast Gate)
        if enable_gate and (tumor_mask > 0).sum() > 0:
            t_pixels = stripped_brain[tumor_mask > 0]
            bg_pixels = stripped_brain[(brain_mask > 0) & (tumor_mask == 0)]
            if len(t_pixels) > 0 and len(bg_pixels) > 0:
                t_mean = float(np.mean(t_pixels))
                bg_mean = float(np.mean(bg_pixels))
                min_contrast = self.params.get("min_contrast_ratio", 0.15)
                rel_contrast = (t_mean - bg_mean) / bg_mean if bg_mean > 0 else 0.0
                if rel_contrast < min_contrast:
                    tumor_mask = np.zeros_like(stripped_brain, dtype=np.uint8)

        # 6. Đo lường đặc trưng hình thái học
        diag_res = extract_tumor_features(tumor_mask, brain_mask)

        # 7. Nếu có Ground Truth, tính chỉ số đánh giá y khoa
        if gt_mask is not None:
            diag_res.dice_score = calculate_dice(tumor_mask, gt_mask)
            diag_res.iou_score = calculate_iou(tumor_mask, gt_mask)

        # 8. Trực quan hóa
        overlay = draw_tumor_overlay(image, tumor_mask, diag_res)
        quad = create_comparison_quad(image, stripped_brain, tumor_mask, overlay)

        intermediates = {
            "original": image,
            "filtered": filtered,
            "stripped": stripped_brain,
            "brain_mask": brain_mask,
            "tumor_mask": tumor_mask,
            "overlay": overlay,
            "quad": quad
        }

        return diag_res, intermediates
