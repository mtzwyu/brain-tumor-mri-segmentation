"""Chuẩn hóa 4 Jupyter Notebook của đồ án: loại bỏ 100% Unicode Emoji.

Phạm vi xử lý
-------------
1. Loại bỏ toàn bộ ký tự Unicode Emoji (U+1F000-U+1FAFF, U+2600-U+27BF,
   U+2B00-U+2BFF, U+FE0F, U+200D, U+20E3) trong source của mọi cell.
2. Chuẩn hóa tiêu đề Markdown có emoji thành tiêu đề học thuật trang trọng
   theo bảng ``HEADING_REWRITES`` (ánh xạ trực tiếp từ bảng quy tắc Ngày 7).
   Các tiêu đề chưa có trong bảng được xử lý tự động qua ``LABEL_BY_EMOJI``.
3. Sửa các ký tự điều khiển bị hỏng trong công thức LaTeX của cell Markdown
   (``\\frac``, ``\\approx``, ``\\rightarrow``, ``\\text``) - các công thức này
   bị biến dạng do escape khi sinh notebook, xem ``LATEX_REPAIRS``.
4. Bảo toàn nguyên vẹn cấu trúc JSON, toàn bộ code Python và toàn bộ output
   của cell (ảnh base64, bảng biểu, log kết quả).

Cách dùng
---------
    python scripts/clean_notebook_emojis.py          # chuẩn hóa + kiểm tra
    python scripts/clean_notebook_emojis.py --check  # chỉ kiểm tra (exit code 1 nếu còn emoji)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]

NOTEBOOKS: Tuple[Path, ...] = (
    PROJECT_ROOT / "notebooks" / "01_data_exploration.ipynb",
    PROJECT_ROOT / "notebooks" / "02_preprocessing_and_skull_stripping.ipynb",
    PROJECT_ROOT / "notebooks" / "03_tumor_segmentation_comparison.ipynb",
    PROJECT_ROOT / "notebooks" / "04_quantitative_evaluation.ipynb",
)

# Tệp sinh notebook: giữ đồng bộ để emoji không tái xuất hiện khi chạy lại generator.
SOURCE_GENERATOR = PROJECT_ROOT / "scripts" / "create_notebooks.py"

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F000-\U0001FAFF"  # Emoji & pictographs (U+1F300-U+1FAFF và mở rộng)
    "\U00002600-\U000027BF"  # Miscellaneous symbols & dingbats
    "\U00002B00-\U00002BFF"  # Miscellaneous symbols and arrows
    "\uFE0F"                 # Variation Selector-16
    "\u200D"                 # Zero Width Joiner
    "\u20E3"                 # Combining Enclosing Keycap
    "]"
)

# Tiêu đề học thuật thay thế (khóa: tiêu đề gốc đã chuẩn hóa khoảng trắng).
HEADING_REWRITES: Dict[str, str] = {
    # Notebook 1
    "# 📓 Notebook 1: Thu Thập, Khảo Sát & Chuẩn Bị Tập Dữ Liệu (TCGA-LGG)":
        "# Notebook 1: Thu Thập, Khảo Sát & Chuẩn Bị Tập Dữ Liệu (TCGA-LGG)",
    "## 🎯 1. Mục tiêu kỹ thuật (Theo Khung Tổng Quát)":
        "## 1. Mục tiêu nghiên cứu (Theo Khung Tổng Quát)",
    "## 📈 3. Phân Tích Thống Kê Phân Bố Khối U":
        "## 3. Trực quan hóa dữ liệu: Phân tích thống kê phân bố khối u",
    "## 🔬 4. Phân Loại 3 Nhóm Ca Bệnh (U Nhỏ, U Vừa, U Lớn)":
        "## 4. Quy trình thực nghiệm: Phân loại 3 nhóm ca bệnh (u nhỏ, u vừa, u lớn)",
    "## 🖼️ 5. Trực Quan Hóa Lưới Ảnh MRI & Ground Truth Mask":
        "## 5. Minh họa hình ảnh: Lưới ảnh MRI và Ground Truth Mask",
    # Notebook 2
    "# 📓 Notebook 2: Tiền Xử Lý & Tách Sọ Não (Skull Stripping)":
        "# Notebook 2: Tiền Xử Lý & Tách Sọ Não (Skull Stripping)",
    "## 🎯 1. Cơ sở lý thuyết DIP (Gonzalez & Woods Ch. 3, 5 & 9)":
        "## 1. Cơ sở lý thuyết DIP (Gonzalez & Woods Ch. 3, 5 & 9)",
    "## 🔬 2. Thử Nghiệm Chi Tiết Từng Bước Tách Sọ Trên Ca Mẫu":
        "## 2. Quy trình thực nghiệm: Thử nghiệm chi tiết từng bước tách sọ trên ca mẫu",
    "## 🩺 3. Đánh Giá Khả Năng Tăng Cường Tương Phản CLAHE":
        "## 3. Ý nghĩa y khoa: Đánh giá khả năng tăng cường tương phản CLAHE",
    "## 🔍 4. Kiểm Thử Tính Bền Vững Của Tách Sọ Trên 4 Ca Khác Nhau":
        "## 4. Phân tích kết quả: Kiểm thử tính bền vững của tách sọ trên 4 ca khác nhau",
    # Notebook 3
    "## 📏 2. Rút trích đặc trưng hình học & Đo lường (Bước 4)":
        "## 2. Đo đạc đặc trưng hình học: Rút trích đặc trưng hình học và đo lường (Bước 4)",
    # Notebook 4
    "## 📉 4. Biểu Đồ Cột So Sánh Điểm Dice Trên Từng Ca Bệnh":
        "## 4. Trực quan hóa dữ liệu: Biểu đồ cột so sánh điểm Dice trên từng ca bệnh",
}

# Nhãn học thuật dùng cho tiêu đề chưa có trong HEADING_REWRITES.
LABEL_BY_EMOJI: Dict[str, str] = {
    "\U0001F3AF": "Mục tiêu nghiên cứu:",          # 🎯
    "\U0001F4CA": "Trực quan hóa dữ liệu:",        # 📊
    "\U0001F4C8": "Trực quan hóa dữ liệu:",        # 📈
    "\U0001F4C9": "Trực quan hóa dữ liệu:",        # 📉
    "\U0001F52C": "Quy trình thực nghiệm:",        # 🔬
    "\U0001F50D": "Phân tích kết quả:",            # 🔍
    "\U0001F4CB": "Đánh giá định lượng:",          # 📋
    "\U0001FA7A": "Ý nghĩa y khoa:",               # 🩺
    "\U0001F4D0": "Đo đạc đặc trưng hình học:",    # 📐
    "\U0001F4CF": "Đo đạc đặc trưng hình học:",    # 📏
    "\U0001F5BC": "Minh họa hình ảnh:",            # 🖼
}

# Sửa công thức LaTeX bị hỏng bởi ký tự điều khiển (chỉ áp dụng cho cell Markdown).
LATEX_REPAIRS: Tuple[Tuple[str, str], ...] = (
    ("\x0c\nrac{", "\\frac{"),
    ("\x0crac{", "\\frac{"),
    ("\x07pprox", "\\approx"),
    ("\text{", "\\text{"),
    ("\nightarrow", "\\rightarrow"),
    ("\ufeff", ""),
)

HEADING_PATTERN = re.compile(r"^(#{1,6})\s*(.*)$")


def heading_key(line: str) -> str:
    """Chuẩn hóa khoảng trắng để tra cứu bảng ánh xạ tiêu đề."""
    return re.sub(r"\s+", " ", line.strip())


def strip_emoji(text: str) -> str:
    """Loại bỏ toàn bộ ký tự emoji khỏi chuỗi."""
    return EMOJI_PATTERN.sub("", text)


def normalize_heading(line: str) -> str:
    """Chuyển một dòng tiêu đề Markdown thành tiêu đề học thuật không emoji."""
    rewrite = HEADING_REWRITES.get(heading_key(line))
    if rewrite is not None:
        return rewrite

    match = HEADING_PATTERN.match(line)
    if match is None:
        return strip_emoji(line)

    level, body = match.group(1), match.group(2)
    leading = EMOJI_PATTERN.match(body)
    if leading is not None:
        label = LABEL_BY_EMOJI.get(leading.group()[0])
        rest = body[leading.end():].strip()
        body = f"{label} {rest}" if label and rest else (label or rest)
    body = re.sub(r"\s{2,}", " ", strip_emoji(body)).strip()
    return f"{level} {body}".rstrip() if body else level


def clean_markdown(text: str) -> str:
    """Chuẩn hóa toàn bộ cell Markdown: sửa LaTeX hỏng, bỏ emoji, sửa tiêu đề."""
    for broken, fixed in LATEX_REPAIRS:
        text = text.replace(broken, fixed)

    lines = []
    for line in text.split("\n"):
        if HEADING_PATTERN.match(line):
            lines.append(normalize_heading(line))
        else:
            lines.append(strip_emoji(line))
    return "\n".join(lines)


def count_emoji(text: str) -> int:
    """Đếm số ký tự emoji còn lại trong chuỗi."""
    return len(EMOJI_PATTERN.findall(text))


def clean_notebook(path: Path) -> int:
    """Chuẩn hóa một notebook, giữ nguyên định dạng JSON gốc. Trả về số emoji đã bỏ."""
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    trailing_newline = raw.endswith(b"\n")

    notebook = json.loads(raw.decode("utf-8"))
    removed = 0
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = "".join(cell.get("source", []))
        removed += count_emoji(source)
        cleaned = clean_markdown(source)
        if cleaned != source:
            cell["source"] = cleaned.splitlines(keepends=True)

    payload = json.dumps(notebook, indent=1, ensure_ascii=False)
    if newline != "\n":
        payload = payload.replace("\n", newline)
    if trailing_newline:
        payload += newline
    path.write_bytes(payload.encode("utf-8"))
    return removed


def clean_generator(path: Path) -> int:
    """Bỏ emoji trong generator notebook để không tái sinh emoji về sau."""
    if not path.is_file():
        return 0
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")
    removed = count_emoji(text)
    if removed:
        for original, rewritten in HEADING_REWRITES.items():
            text = text.replace(original, rewritten)
        text = EMOJI_PATTERN.sub("", text)
        text = re.sub(r"(?m)^(#{1,6}) {2,}", r"\1 ", text)
        path.write_bytes(text.encode("utf-8"))
    return removed


def scan(paths: Tuple[Path, ...]) -> List[Tuple[Path, int]]:
    """Đếm emoji còn lại trong từng tệp."""
    results = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        results.append((path, count_emoji(text)))
    return results


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Chỉ kiểm tra số lượng emoji, không ghi đè tệp",
    )
    args = parser.parse_args(argv)

    if not args.check:
        total = sum(clean_notebook(path) for path in NOTEBOOKS)
        total += clean_generator(SOURCE_GENERATOR)
        print(f"Đã loại bỏ {total} ký tự emoji.")

    failed = False
    for path, remaining in scan(NOTEBOOKS):
        status = "OK" if remaining == 0 else "FAIL"
        if remaining:
            failed = True
        print(f"[{status}] {remaining:>3} emoji còn lại - {path.relative_to(PROJECT_ROOT)}")

    if failed:
        print("Chưa đạt yêu cầu: vẫn còn emoji trong notebook.", file=sys.stderr)
        return 1
    print("Kiểm tra hoàn tất: 0 emoji trong cả 4 notebook.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
