"""Tập lệnh thực thi trực quan 4 Jupyter Notebooks và xuất báo cáo HTML.

Quy trình:
1. Đọc và thực thi tuần tự 4 Jupyter Notebooks trong thư mục notebooks/.
2. In trực tiếp tiến trình và toàn bộ cell outputs (văn bản, bảng số liệu, kết quả đo) ra terminal.
3. Lưu các cell outputs vào tệp .ipynb tại chỗ.
4. Xuất 4 tệp báo cáo HTML độc lập vào reports/notebooks/ để mở xem trực quan trên trình duyệt.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
REPORTS_DIR = REPO_ROOT / "reports" / "notebooks"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

NOTEBOOK_FILES = [
    ("01_data_exploration.ipynb", "Notebook 1: Khảo Sát & Phân Tầng Dữ Liệu TCGA-LGG"),
    ("02_preprocessing_and_skull_stripping.ipynb", "Notebook 2: Tiền Xử Lý & Tách Sọ Não (Skull Stripping)"),
    ("03_tumor_segmentation_comparison.ipynb", "Notebook 3: Phân Đoạn Watershed vs. Region Growing & Anomaly Gate"),
    ("04_quantitative_evaluation.ipynb", "Notebook 4: Đánh Giá Định Lượng & Phân Tích Trường Hợp Thất Bại"),
]


def run_single_notebook(filename: str, title: str) -> dict:
    """Thực thi một notebook và in cell outputs chi tiết ra console."""
    nb_path = NOTEBOOKS_DIR / filename
    html_path = REPORTS_DIR / filename.replace(".ipynb", ".html")

    print("\n" + "=" * 80)
    print(f"▶ BẮT ĐẦU THỰC THI: {title}")
    print(f"  Tệp nguồn: {nb_path}")
    print("=" * 80)

    start_time = time.perf_counter()

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

    # Chạy notebook với thư mục làm việc là notebooks/
    ep.preprocess(nb, {"metadata": {"path": str(NOTEBOOKS_DIR)}})

    elapsed = time.perf_counter() - start_time

    # Lưu lại notebook đã chạy
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    # In kết quả các cell ra màn hình
    print(f"\n[KẾT QUẢ ĐẦU RA CỦA CÁC CELL TRONG {filename}]:")
    print("-" * 80)

    cell_idx = 1
    total_outputs = 0
    for cell in nb.cells:
        if cell.cell_type == "code":
            has_output = False
            for out in cell.get("outputs", []):
                total_outputs += 1
                if out.output_type == "stream":
                    text = out.get("text", "").strip()
                    if text:
                        print(f"[Cell #{cell_idx} Stream Output]:\n{text}\n")
                        has_output = True
                elif out.output_type in ("execute_result", "display_data"):
                    data = out.get("data", {})
                    if "text/plain" in data:
                        text = data["text/plain"].strip()
                        if text:
                            print(f"[Cell #{cell_idx} Data Output]:\n{text}\n")
                            has_output = True
                    if "image/png" in data:
                        print(f"[Cell #{cell_idx} Visual Output]: Đã tạo đồ thị/ảnh minh họa (PNG base64).")
                        has_output = True
            cell_idx += 1

    # Xuất file HTML báo cáo
    html_exporter = HTMLExporter()
    html_data, _ = html_exporter.from_notebook_node(nb)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_data)

    html_size_kb = html_path.stat().st_size / 1024
    print(f"✔ Đã xuất tệp HTML báo cáo: {html_path} ({html_size_kb:.1f} KB)")
    print(f"✔ Thời gian thực thi: {elapsed:.2f} giây | Tổng outputs: {total_outputs}")

    return {
        "filename": filename,
        "title": title,
        "elapsed_sec": elapsed,
        "total_outputs": total_outputs,
        "html_size_kb": html_size_kb,
    }


def main():
    print("=" * 80)
    print("TRÌNH THỰC THI TRỰC QUAN 4 JUPYTER NOTEBOOKS — ĐỒ ÁN XỬ LÝ ẢNH SỐ HUIT")
    print("=" * 80)

    overall_start = time.perf_counter()
    results = []

    for filename, title in NOTEBOOK_FILES:
        res = run_single_notebook(filename, title)
        results.append(res)

    total_time = time.perf_counter() - overall_start

    print("\n" + "=" * 80)
    print("TỔNG HỢP KẾT QUẢ THỰC THI 4 JUPYTER NOTEBOOKS")
    print("=" * 80)
    print(f"{'STT':<4} | {'Tệp Notebook':<44} | {'Outputs':<8} | {'HTML (KB)':<10} | {'Thời gian':<10}")
    print("-" * 84)

    for i, r in enumerate(results, 1):
        print(
            f"{i:<4} | {r['filename']:<44} | {r['total_outputs']:<8} | "
            f"{r['html_size_kb']:<10.1f} | {r['elapsed_sec']:<8.2f}s"
        )

    print("-" * 84)
    print(f"Tổng thời gian toàn bộ tiến trình: {total_time:.2f} giây.")
    print("Tất cả 4 Notebooks đã được thực thi thành công 100% và sẵn sàng báo cáo!\n")


if __name__ == "__main__":
    main()
