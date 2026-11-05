"""Kết xuất 20 slide từ reports/SLIDE_THUYET_TRINH_XLAS.pdf sang ảnh PNG."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = REPO_ROOT / "reports" / "SLIDE_THUYET_TRINH_XLAS.pdf"
OUT_DIR = REPO_ROOT / "reports" / "slides"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path(r"C:\Users\xpaga\.gemini\antigravity-cli\brain\59f9c3cc-b2ad-48d6-8d49-530673873498")


def render_all_slides():
    doc = pymupdf.open(str(PDF_PATH))
    print(f"Đang kết xuất {len(doc)} slide từ {PDF_PATH} sang PNG (DPI 150)...")

    # Zoom matrix cho 150 DPI (150 / 72 ≈ 2.0833)
    zoom = 150.0 / 72.0
    matrix = pymupdf.Matrix(zoom, zoom)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        slide_name = f"slide_{i+1:02d}.png"
        out_file = OUT_DIR / slide_name
        pix.save(str(out_file))

        # Copy vào artifacts directory để hỗ trợ carousels
        if ARTIFACT_DIR.is_dir():
            art_file = ARTIFACT_DIR / slide_name
            shutil.copy2(out_file, art_file)

        print(f"  ✔ {slide_name}: {pix.width}x{pix.height}px ({out_file.stat().st_size / 1024:.1f} KB)")

    doc.close()
    print("Hoàn tất kết xuất 20 slide PNG chất lượng cao!")


if __name__ == "__main__":
    render_all_slides()
