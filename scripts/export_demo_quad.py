"""Xuất hình minh chứng "Comparison Quad" (4 khung nhìn) cho slide Demo lâm sàng.

Chạy pipeline DIP thật trên một ca bệnh TCGA-LGG có u rõ nét, xuất lưới ảnh
reports/figures/demo_comparison_quad.png (2x2: Ảnh gốc | Não tách sọ | Mặt nạ u |
Bounding Box) và in ra các chỉ số chẩn đoán để đối chiếu trên slide.
"""

from pathlib import Path
import sys
import time

import cv2

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline import BrainTumorPipeline  # noqa: E402

CASE_ID = "TCGA_DU_6404_19850629_40"
DATA_DIR = ROOT / "data" / "full"
OUTPUT = ROOT / "reports" / "figures" / "demo_comparison_quad.png"


def main() -> None:
    image = cv2.imread(str(DATA_DIR / "images" / f"{CASE_ID}.png"), cv2.IMREAD_GRAYSCALE)
    gt_mask = cv2.imread(str(DATA_DIR / "masks" / f"{CASE_ID}_mask.png"), cv2.IMREAD_GRAYSCALE)
    if image is None or gt_mask is None:
        raise SystemExit(f"Không tìm thấy ca bệnh {CASE_ID} trong {DATA_DIR}")

    pipeline = BrainTumorPipeline(method="watershed")
    result, intermediates = pipeline.process(image, gt_mask if gt_mask.max() > 0 else None)

    started = time.perf_counter()
    for _ in range(5):
        pipeline.process(image)
    latency_ms = (time.perf_counter() - started) / 5 * 1000

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUTPUT), intermediates["quad"])

    print(f"Ca bệnh      : {CASE_ID}")
    print(f"Diện tích u  : {result.tumor_area_px} px")
    print(f"Tỷ lệ u/não  : {result.tumor_ratio_percent:.2f} %")
    print(f"Độ tròn C    : {result.circularity:.3f}")
    print(f"Dice / IoU   : {result.dice_score:.4f} / {result.iou_score:.4f}")
    print(f"BBox         : {result.bbox}")
    print(f"Độ trễ TB    : {latency_ms:.1f} ms")
    print(f"Đã ghi       : {OUTPUT}")


if __name__ == "__main__":
    main()
