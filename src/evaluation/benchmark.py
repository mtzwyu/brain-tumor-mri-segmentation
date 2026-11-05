"""Hệ thống đánh giá thực nghiệm hàng loạt (Batch Benchmark) trên 20 mẫu ảnh TCGA-LGG.

Phụ trách: Huỳnh Tâm Trí (MSSV: 2045240315).
"""

from __future__ import annotations
from typing import List, Dict, Any, Callable
import os
import time
import pandas as pd
import numpy as np
import cv2
from .metrics import calculate_all_metrics


def run_benchmark(
    images_dir: str,
    masks_dir: str,
    predict_fn: Callable[[np.ndarray], np.ndarray],
    method_name: str = "method",
    max_samples: Optional[int] = None,
    sample_ids: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Chạy thực nghiệm đánh giá trên tập dữ liệu và tính toán độ trễ trung bình.
    
    Args:
        images_dir: Đường dẫn thư mục ảnh MRI gốc (.png).
        masks_dir: Đường dẫn thư mục mặt nạ Ground Truth (.png).
        predict_fn: Hàm nhận ảnh MRI gốc và trả về mặt nạ phân đoạn u nhị phân.
        method_name: Tên phương pháp để ghi nhận vào bảng báo cáo.
        max_samples: Số lượng mẫu tối đa cần đánh giá (mặc định None là toàn bộ).
        sample_ids: Danh sách mã ca cụ thể cần đánh giá (mặc định None).
        
    Returns:
        pd.DataFrame: Bảng kết quả chi tiết từng ca bệnh và dòng Mean ± Std ở cuối.
    """
    image_files = sorted([f for f in os.listdir(images_dir) if f.endswith(".png")])
    if sample_ids is not None:
        target_set = {s if s.endswith(".png") else f"{s}.png" for s in sample_ids}
        image_files = [f for f in image_files if f in target_set]
    elif max_samples is not None:
        image_files = image_files[:max_samples]

    records: List[Dict[str, Any]] = []
    latencies: List[float] = []

    for fname in image_files:
        img_path = os.path.join(images_dir, fname)
        sample_id = fname.replace(".png", "")
        mask_path = os.path.join(masks_dir, f"{sample_id}_mask.png")

        if not os.path.exists(mask_path):
            continue

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        gt_mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        start_t = time.perf_counter()
        pred_mask = predict_fn(img)
        elapsed_ms = (time.perf_counter() - start_t) * 1000.0
        latencies.append(elapsed_ms)

        m = calculate_all_metrics(pred_mask, gt_mask)
        records.append({
            "sample_id": sample_id,
            "method": method_name,
            "dice": m["dice"],
            "iou": m["iou"],
            "sensitivity": m["sensitivity"],
            "specificity": m["specificity"],
            "latency_ms": round(elapsed_ms, 2)
        })

    df = pd.DataFrame(records)
    return df
