"""Nhúng hiệu ứng chuyển cảnh và hiệu ứng xuất hiện cho bộ slide thuyết trình.

Script bổ sung trực tiếp vào cấu trúc OOXML của tệp `.pptx`:
1. `<p:transition>` — hiệu ứng chuyển cảnh riêng cho từng slide.
2. `<p:timing>` — chuỗi hiệu ứng xuất hiện (fade-in) cho các khối thẻ nội dung,
   so le theo hàng để các thẻ lần lượt hiện ra khi trình chiếu.

Cách dùng:
    python scripts/enrich_slide_animations.py
    python scripts/enrich_slide_animations.py --path reports/SLIDE_THUYET_TRINH_XLAS.pptx
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PPTX = PROJECT_ROOT / "reports" / "SLIDE_THUYET_TRINH_XLAS.pptx"

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}

# Hiệu ứng chuyển cảnh mong muốn cho từng slide (1-based).
TRANSITIONS: Dict[int, Tuple[str, str]] = {
    1: ("med", "<p:fade/>"),
    2: ("fast", '<p:push dir="l"/>'),
    3: ("med", '<p:wipe dir="l"/>'),
    4: ("med", "<p:zoom/>"),
    5: ("med", "<p:wheel/>"),
    6: ("med", "<p:comb/>"),
    7: ("med", "<p:circle/>"),
    8: ("med", '<p:cover dir="l"/>'),
    9: ("med", '<p:push dir="u"/>'),
    10: ("med", "<p:diamond/>"),
    11: ("med", "<p:dissolve/>"),
    12: ("med", "<p:wedge/>"),
    13: ("med", '<p:strips dir="ld"/>'),
    14: ("med", '<p:blinds dir="horz"/>'),
    15: ("med", '<p:checker dir="horz"/>'),
    16: ("med", '<p:randomBar dir="horz"/>'),
    17: ("med", '<p:wipe dir="u"/>'),
    18: ("med", '<p:push dir="d"/>'),
    19: ("med", '<p:split orient="horz" dir="out"/>'),
    20: ("med", "<p:fade/>"),
}

EMU_PER_INCH = 914400
SLIDE_W = 10.0
SLIDE_H = 5.625

CONTENT_TOP = 1.2          # bỏ qua tiêu đề/kicker phía trên
CONTENT_BOTTOM = 5.12      # bỏ qua dòng chân trang
MAX_AREA_RATIO = 0.55      # bỏ qua khối nền phủ gần kín slide
MAX_GROUPS = 6             # số nhịp xuất hiện tối đa mỗi slide
STEP_DELAY_MS = 280        # độ trễ giữa hai nhịp
EFFECT_DURATION_MS = 400   # thời lượng hiệu ứng fade-in

TRANSITION_RE = re.compile(r"<p:transition\b[^>]*?(?:/>|>.*?</p:transition>)", re.DOTALL)
TIMING_RE = re.compile(r"<p:timing>.*?</p:timing>", re.DOTALL)


def _shape_info(element: ET.Element):
    """Trả về (id, x, y, w, h) của một shape; None nếu không xác định được."""
    tag = element.tag.split("}")[-1]
    if tag == "sp":
        id_path, xfrm_path = "p:nvSpPr/p:cNvPr", "p:spPr/a:xfrm"
    elif tag == "pic":
        id_path, xfrm_path = "p:nvPicPr/p:cNvPr", "p:spPr/a:xfrm"
    elif tag == "graphicFrame":
        id_path, xfrm_path = "p:nvGraphicFramePr/p:cNvPr", "p:xfrm"
    else:
        return None

    c_nv_pr = element.find(id_path, NS)
    offset = element.find(f"{xfrm_path}/a:off", NS)
    extent = element.find(f"{xfrm_path}/a:ext", NS)
    if c_nv_pr is None or offset is None or extent is None:
        return None

    try:
        shape_id = int(c_nv_pr.get("id"))
        x = int(offset.get("x")) / EMU_PER_INCH
        y = int(offset.get("y")) / EMU_PER_INCH
        w = int(extent.get("cx")) / EMU_PER_INCH
        h = int(extent.get("cy")) / EMU_PER_INCH
    except (TypeError, ValueError):
        return None
    return shape_id, x, y, w, h


def content_groups(slide_xml: str) -> List[List[int]]:
    """Nhóm id các shape nội dung theo hàng để tạo nhịp xuất hiện."""
    root = ET.fromstring(slide_xml)
    sp_tree = root.find("p:cSld/p:spTree", NS)
    if sp_tree is None:
        return []

    slide_area = SLIDE_W * SLIDE_H
    rows: Dict[float, List[Tuple[float, int]]] = {}
    for child in sp_tree:
        info = _shape_info(child)
        if info is None:
            continue
        shape_id, x, y, w, h = info
        if not (CONTENT_TOP <= y <= CONTENT_BOTTOM):
            continue
        if w * h >= MAX_AREA_RATIO * slide_area:
            continue
        bucket = round(y * 2) / 2
        rows.setdefault(bucket, []).append((x, shape_id))

    groups = []
    for bucket in sorted(rows):
        groups.append([shape_id for _, shape_id in sorted(rows[bucket])])
    return groups[:MAX_GROUPS]


def build_timing(groups: List[List[int]]) -> str:
    """Sinh cây <p:timing> với hiệu ứng fade-in so le cho từng nhóm shape."""
    next_id = 100

    def new_id() -> int:
        nonlocal next_id
        next_id += 1
        return next_id

    effects = []
    for index, group in enumerate(groups):
        delay = index * STEP_DELAY_MS
        for shape_id in group:
            effect_id = new_id()
            set_c_tn = new_id()
            anim_c_tn = new_id()
            effects.append(
                f'<p:par><p:cTn id="{effect_id}" presetID="10" presetClass="entr" '
                f'presetSubtype="0" fill="hold" grpId="0" nodeType="withEffect">'
                f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst>'
                f"<p:childTnLst>"
                f"<p:set>"
                f"<p:cBhvr>"
                f'<p:cTn id="{set_c_tn}" dur="1" fill="hold">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                f'<p:tgtEl><p:spTgt spid="{shape_id}"/></p:tgtEl>'
                f"<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>"
                f"</p:cBhvr>"
                f'<p:to><p:strVal val="visible"/></p:to>'
                f"</p:set>"
                f'<p:animEffect transition="in" filter="fade">'
                f"<p:cBhvr>"
                f'<p:cTn id="{anim_c_tn}" dur="{EFFECT_DURATION_MS}"/>'
                f'<p:tgtEl><p:spTgt spid="{shape_id}"/></p:tgtEl>'
                f"</p:cBhvr>"
                f"</p:animEffect>"
                f"</p:childTnLst></p:cTn></p:par>"
            )

    if not effects:
        return ""

    effect_block = "".join(effects)
    return (
        "<p:timing><p:tnLst><p:par>"
        '<p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
        "<p:childTnLst>"
        '<p:seq concurrent="1" nextAc="seek">'
        '<p:cTn id="2" dur="indefinite" nodeType="mainSeq">'
        "<p:childTnLst>"
        "<p:par>"
        '<p:cTn id="3" fill="hold">'
        '<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        "<p:childTnLst>"
        "<p:par>"
        '<p:cTn id="4" fill="hold">'
        '<p:stCondLst><p:cond delay="0"/></p:stCondLst>'
        f"<p:childTnLst>{effect_block}</p:childTnLst>"
        "</p:cTn>"
        "</p:par>"
        "</p:childTnLst>"
        "</p:cTn>"
        "</p:par>"
        "</p:childTnLst>"
        "</p:cTn>"
        '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
        '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
        "</p:seq>"
        "</p:childTnLst>"
        "</p:cTn>"
        "</p:par></p:tnLst></p:timing>"
    )


def enrich_slide(slide_xml: str, index: int) -> str:
    """Gắn transition + timing cho một slide (idempotent)."""
    xml = TRANSITION_RE.sub("", slide_xml)
    xml = TIMING_RE.sub("", xml)

    speed, effect = TRANSITIONS.get(index, ("med", "<p:fade/>"))
    transition = f'<p:transition spd="{speed}">{effect}</p:transition>'

    groups = content_groups(xml)
    timing = build_timing(groups)

    if "</p:clrMapOvr>" in xml:
        xml = xml.replace("</p:clrMapOvr>", f"</p:clrMapOvr>{transition}", 1)
    else:
        xml = xml.replace("</p:cSld>", f"</p:cSld>{transition}", 1)

    xml = xml.replace("</p:sld>", f"{timing}</p:sld>", 1)
    return xml


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=str(DEFAULT_PPTX), help="Đường dẫn tệp .pptx")
    args = parser.parse_args(argv)

    pptx_path = Path(args.path)
    if not pptx_path.is_file():
        print(f"Không tìm thấy tệp: {pptx_path}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(pptx_path, "r") as source:
        entries = [(info, source.read(info.filename)) for info in source.infolist()]

    payloads = {info.filename: data for info, data in entries}
    slide_names = sorted(
        (name for name in payloads if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
        key=lambda name: int(re.search(r"slide(\d+)\.xml", name).group(1)),
    )

    updated: Dict[str, bytes] = {}
    for index, name in enumerate(slide_names, start=1):
        enriched = enrich_slide(payloads[name].decode("utf-8"), index)
        updated[name] = enriched.encode("utf-8")
        groups = content_groups(enriched)
        effect = TRANSITIONS.get(index, ("med", "<p:fade/>"))[1]
        print(f"Slide {index:>2}: {effect:<34} · {len(groups)} nhịp · "
              f"{sum(len(g) for g in groups)} đối tượng")

    with zipfile.ZipFile(pptx_path, "w", zipfile.ZIP_DEFLATED) as target:
        for info, data in entries:
            target.writestr(info, updated.get(info.filename, data))

    print(f"Đã nhúng hiệu ứng cho {len(slide_names)} slide: {pptx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
