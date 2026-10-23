/**
 * Sinh bộ slide thuyết trình bảo vệ đồ án Xử lý ảnh số (20 trang).
 *
 * Đề tài: Phân đoạn và phát hiện tổn thương trên ảnh y tế (Trọng tâm: Khối u não trên ảnh cộng hưởng từ MRI TCGA-LGG)
 * Nhóm: Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315) - HUIT
 *
 * Chạy: node scripts/generate_slides.js
 */

const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");

// ---------------------------------------------------------------------------
// 1. Design tokens
// ---------------------------------------------------------------------------
const FONT = "Segoe UI";
const FONT_STRONG = "Segoe UI Semibold";
const FONT_MONO = "Courier New";

const C = {
  primary: "065A82",
  primaryDeep: "03405C",
  secondary: "028090",
  accent: "00A896",
  dark: "21295C",
  ink: "1E293B",
  muted: "5F7186",
  card: "F0F7F9",
  cardAlt: "EBF4F6",
  border: "D1E3E8",
  white: "FFFFFF",
  bg: "F8FAFC",
  tint: "E3F1F4",
  warn: "B45309",
  warnBg: "FDF3E3",
};

const L = {
  w: 10,
  mx: 0.55,
  cw: 8.9,
  foot: 5.2,
};

const FIG_DIR = path.resolve(__dirname, "..", "reports", "figures");
const OUT_FILE = path.resolve(__dirname, "..", "reports", "SLIDE_THUYET_TRINH_XLAS.pptx");

const shadowSoft = {
  type: "outer",
  color: "0B2B3C",
  opacity: 0.1,
  blur: 2,
  angle: 90,
  offset: 1,
};

// ---------------------------------------------------------------------------
// 2. Helpers
// ---------------------------------------------------------------------------
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_16x9";
pptx.author = "Hà Mạnh Trường & Huỳnh Tâm Trí";
pptx.company = "HUIT - Khoa Công nghệ Thông tin - Ngành Khoa học Dữ liệu - Bộ môn Xử lý ảnh số";
pptx.subject = "Phân đoạn và phát hiện tổn thương trên ảnh y tế";
pptx.title = "SLIDE_THUYET_TRINH_XLAS";
pptx.theme = { headFontFace: FONT_STRONG, bodyFontFace: FONT, lang: "vi-VN" };

function figure(name) {
  const file = path.join(FIG_DIR, name);
  if (!fs.existsSync(file)) {
    throw new Error(`Không tìm thấy hình minh chứng: ${file}`);
  }
  return file;
}

function addNotes(slide, speaker, content) {
  slide.addNotes(`[${speaker}] ${content}`);
}

function addCard(slide, x, y, w, h, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.06,
    fill: { color: opts.fill || C.card },
    line: { color: opts.line === undefined ? C.border : opts.line, width: 0.75 },
    ...(opts.shadow ? { shadow: shadowSoft } : {}),
  });
}

function addText(slide, text, opts) {
  slide.addText(text, {
    fontFace: FONT,
    color: C.ink,
    margin: 0,
    valign: "top",
    ...opts,
  });
}

function addKicker(slide, kicker) {
  addText(slide, kicker, {
    x: L.mx,
    y: 0.36,
    w: L.cw,
    h: 0.22,
    fontFace: FONT_STRONG,
    fontSize: 9,
    color: C.secondary,
    charSpacing: 1.6,
    valign: "middle",
  });
}

function addFooter(slide, page, section) {
  addText(slide, section, {
    x: L.mx,
    y: L.foot,
    w: 6.5,
    h: 0.2,
    fontSize: 8,
    color: C.muted,
    valign: "middle",
  });
  addText(slide, `${String(page).padStart(2, "0")} / 20`, {
    x: L.w - L.mx - 1.1,
    y: L.foot,
    w: 1.1,
    h: 0.2,
    fontSize: 8,
    color: C.muted,
    align: "right",
    valign: "middle",
  });
}

function contentSlide(kicker, title, page, section, opts = {}) {
  const slide = pptx.addSlide();
  slide.background = { color: C.bg };
  addKicker(slide, kicker);
  addText(slide, title, {
    x: L.mx,
    y: opts.titleY || 0.6,
    w: L.cw,
    h: opts.titleH || 0.55,
    fontFace: FONT_STRONG,
    fontSize: opts.titleSize || 22,
    color: C.dark,
    lineSpacingMultiple: 1.05,
    valign: "middle",
  });
  addFooter(slide, page, section);
  return slide;
}

function bullets(slide, items, opts = {}) {
  const runs = items.map((item, index) => ({
    text: item,
    options: {
      bullet: { code: "25CF" },
      breakLine: index < items.length - 1,
      paraSpaceAfter: opts.gap === undefined ? 7 : opts.gap,
    },
  }));
  slide.addText(runs, {
    x: opts.x,
    y: opts.y,
    w: opts.w,
    h: opts.h,
    fontFace: FONT,
    fontSize: opts.fontSize || 11,
    color: opts.color || C.ink,
    lineSpacingMultiple: opts.lineSpacing || 1.25,
    margin: 0,
    valign: "top",
  });
}

function chip(slide, x, y, w, h, label, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.04,
    fill: { color: opts.fill || C.tint },
    line: { color: opts.line || C.border, width: 0.75 },
  });
  addText(slide, label, {
    x: x + 0.1,
    y,
    w: w - 0.2,
    h,
    fontSize: opts.fontSize || 9.5,
    fontFace: opts.fontFace || FONT,
    color: opts.color || C.primary,
    bold: opts.bold !== false,
    align: "center",
    valign: "middle",
  });
}

function numberedCard(slide, x, y, w, h, number, title, body, opts = {}) {
  addCard(slide, x, y, w, h, { fill: opts.fill || C.white, shadow: true });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: x + 0.22,
    y: y + 0.22,
    w: 0.4,
    h: 0.4,
    fill: { color: opts.badge || C.primary },
    line: { color: opts.badge || C.primary, width: 0.75 },
  });
  addText(slide, number, {
    x: x + 0.22,
    y: y + 0.22,
    w: 0.4,
    h: 0.4,
    fontSize: 12,
    fontFace: FONT_STRONG,
    color: C.white,
    align: "center",
    valign: "middle",
  });
  addText(slide, title, {
    x: x + 0.74,
    y: y + 0.2,
    w: w - 0.94,
    h: 0.26,
    fontSize: 12.5,
    fontFace: FONT_STRONG,
    color: C.dark,
    valign: "middle",
  });
  addText(slide, body, {
    x: x + 0.74,
    y: y + 0.5,
    w: w - 0.94,
    h: h - 0.66,
    fontSize: 10,
    color: C.muted,
    lineSpacingMultiple: 1.2,
    valign: "top",
  });
}

function kpiCard(slide, x, y, w, h, value, label, opts = {}) {
  addCard(slide, x, y, w, h, { fill: opts.fill || C.white, shadow: true });
  addText(slide, value, {
    x: x + 0.2,
    y: y + 0.14,
    w: w - 0.4,
    h: 0.42,
    fontSize: opts.valueSize || 22,
    fontFace: FONT_STRONG,
    color: opts.valueColor || C.primary,
    valign: "middle",
  });
  addText(slide, label, {
    x: x + 0.2,
    y: y + 0.58,
    w: w - 0.4,
    h: h - 0.68,
    fontSize: 9,
    color: C.muted,
    lineSpacingMultiple: 1.1,
    valign: "top",
  });
}

function formulaCard(slide, x, y, w, h, { tag, formula, caption }) {
  addCard(slide, x, y, w, h, { fill: C.white, shadow: true });
  addText(slide, tag, {
    x: x + 0.22,
    y: y + 0.16,
    w: w - 0.44,
    h: 0.24,
    fontSize: 9,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.1,
    valign: "middle",
  });
  addText(slide, formula, {
    x: x + 0.22,
    y: y + 0.46,
    w: w - 0.44,
    h: 0.5,
    fontSize: 14,
    fontFace: FONT,
    italic: true,
    color: C.dark,
    align: "center",
    valign: "middle",
  });
  addText(slide, caption, {
    x: x + 0.22,
    y: y + 0.94,
    w: w - 0.44,
    h: h - 0.98,
    fontSize: 8.5,
    color: C.muted,
    lineSpacingMultiple: 1.1,
    valign: "top",
  });
}

function fractionBlock(slide, opts) {
  const { x, y, w, h, label, numerator, denominator, suffix } = opts;
  const fontSize = opts.fontSize || 13;
  const labelW = opts.labelW || 0.8;
  const suffixW = suffix ? 0.62 : 0;
  const fracX = x + labelW + 0.1;
  const fracW = w - labelW - 0.1 - suffixW;
  const barY = y + h / 2;

  addText(slide, label, {
    x,
    y,
    w: labelW,
    h,
    fontSize,
    fontFace: FONT_STRONG,
    italic: true,
    color: C.dark,
    align: "right",
    valign: "middle",
  });

  const addTerm = (content, top) => {
    if (typeof content === "string") {
      addText(slide, content, {
        x: fracX,
        y: top,
        w: fracW,
        h: 0.29,
        fontSize,
        italic: true,
        color: C.ink,
        align: "center",
        valign: "middle",
      });
      return;
    }
    slide.addText(content, {
      x: fracX,
      y: top,
      w: fracW,
      h: 0.29,
      fontFace: FONT,
      fontSize,
      color: C.ink,
      align: "center",
      valign: "middle",
      margin: 0,
    });
  };

  addTerm(numerator, barY - 0.31);
  slide.addShape(pptx.ShapeType.line, {
    x: fracX,
    y: barY,
    w: fracW,
    h: 0,
    line: { color: C.primary, width: 1.25 },
  });
  addTerm(denominator, barY + 0.02);

  if (suffix) {
    addText(slide, suffix, {
      x: fracX + fracW + 0.04,
      y,
      w: suffixW,
      h,
      fontSize: Math.min(fontSize - 1.5, 10.5),
      italic: true,
      color: C.dark,
      align: "left",
      valign: "middle",
    });
  }
}

function figureCaption(slide, text, x, y, w) {
  addText(slide, text, {
    x,
    y,
    w,
    h: 0.22,
    fontSize: 8,
    italic: true,
    color: C.muted,
    align: "center",
    valign: "middle",
  });
}

// ---------------------------------------------------------------------------
// 3. Slide 1 — Bìa đồ án
// ---------------------------------------------------------------------------
{
  const slide = pptx.addSlide();
  slide.background = { color: C.bg };

  addText(slide, "TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH (HUIT)", {
    x: L.mx,
    y: 0.5,
    w: 6.2,
    h: 0.24,
    fontSize: 10.5,
    fontFace: FONT_STRONG,
    color: C.primary,
    charSpacing: 0.8,
    valign: "middle",
  });
  addText(slide, "KHOA CÔNG NGHỆ THÔNG TIN  ·  NGÀNH KHOA HỌC DỮ LIỆU  ·  BỘ MÔN XỬ LÝ ẢNH SỐ", {
    x: L.mx,
    y: 0.76,
    w: 6.2,
    h: 0.22,
    fontSize: 8.5,
    color: C.muted,
    charSpacing: 0.8,
    valign: "middle",
  });

  addText(slide, "BÁO CÁO ĐỒ ÁN MÔN HỌC  ·  XỬ LÝ ẢNH SỐ", {
    x: L.mx,
    y: 1.34,
    w: 6.2,
    h: 0.22,
    fontSize: 9,
    fontFace: FONT_STRONG,
    color: C.accent,
    charSpacing: 1.4,
    valign: "middle",
  });

  addText(slide, "PHÂN ĐOẠN VÀ PHÁT HIỆN\nTỔN THƯƠNG TRÊN ẢNH Y TẾ", {
    x: L.mx,
    y: 1.56,
    w: 6.35,
    h: 0.95,
    fontSize: 22,
    fontFace: FONT_STRONG,
    color: C.dark,
    lineSpacingMultiple: 1.12,
    valign: "top",
  });

  addText(slide, "(Nghiên cứu trọng tâm: Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI — Bộ dữ liệu chuẩn TCGA-LGG)", {
    x: L.mx,
    y: 2.58,
    w: 6.35,
    h: 0.46,
    fontSize: 10.5,
    italic: true,
    color: C.secondary,
    lineSpacingMultiple: 1.15,
    valign: "middle",
  });

  addText(slide, "Giảng viên hướng dẫn: ThS. Đỗ Hùng Dũng", {
    x: L.mx,
    y: 3.14,
    w: 6.2,
    h: 0.24,
    fontSize: 10,
    color: C.ink,
    valign: "middle",
  });

  const members = [
    { name: "Hà Mạnh Trường", mssv: "2045240326", role: "Nhóm trưởng", share: "50%" },
    { name: "Huỳnh Tâm Trí", mssv: "2045240315", role: "Thành viên", share: "50%" },
  ];
  members.forEach((member, index) => {
    const x = L.mx + index * 3.15;
    addCard(slide, x, 3.52, 2.95, 1.02, { fill: C.white, shadow: true });
    addText(slide, member.name, {
      x: x + 0.2,
      y: 3.62,
      w: 2.55,
      h: 0.24,
      fontSize: 11.5,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, `MSSV ${member.mssv}  ·  ${member.role}`, {
      x: x + 0.2,
      y: 3.88,
      w: 2.55,
      h: 0.2,
      fontSize: 8.5,
      color: C.muted,
      valign: "middle",
    });
    chip(slide, x + 0.2, 4.15, 0.72, 0.26, member.share, {
      fill: C.tint,
      color: C.primary,
      fontSize: 8.5,
    });
    addText(slide, "Đóng góp", {
      x: x + 1.0,
      y: 4.15,
      w: 1.55,
      h: 0.26,
      fontSize: 8.5,
      color: C.muted,
      valign: "middle",
    });
  });

  addText(slide, "TP. Hồ Chí Minh, Năm 2026", {
    x: L.mx,
    y: 4.74,
    w: 6.2,
    h: 0.24,
    fontSize: 10,
    fontFace: FONT_STRONG,
    color: C.dark,
    valign: "middle",
  });

  // Panel dữ liệu thực nghiệm
  addCard(slide, 7.05, 0.5, 2.4, 4.62, { fill: C.primary, line: C.primary, shadow: true });
  addText(slide, "DỮ LIỆU\nTHỰC NGHIỆM", {
    x: 7.32,
    y: 0.78,
    w: 1.9,
    h: 0.5,
    fontSize: 9.5,
    fontFace: FONT_STRONG,
    color: "9FE8DC",
    charSpacing: 1.4,
    lineSpacingMultiple: 1.1,
    valign: "top",
  });

  const stats = [
    { value: "3.929", label: "lát cắt MRI" },
    { value: "110", label: "bệnh nhân LGG" },
    { value: "1.373", label: "lát cắt có u" },
    { value: "256×256", label: "pixel, FLAIR / T1" },
  ];
  stats.forEach((stat, index) => {
    const y = 1.72 + index * 0.78;
    addText(slide, stat.value, {
      x: 7.32,
      y,
      w: 1.9,
      h: 0.34,
      fontSize: 19,
      fontFace: FONT_STRONG,
      color: C.white,
      valign: "middle",
    });
    addText(slide, stat.label, {
      x: 7.32,
      y: y + 0.34,
      w: 1.9,
      h: 0.2,
      fontSize: 8.5,
      color: "CBE8EF",
      valign: "middle",
    });
  });

  addNotes(
    slide,
    "Trường",
    "Kính thưa Thầy và các bạn, em là Hà Mạnh Trường, nhóm trưởng. Đề tài của nhóm là Phân đoạn và phát hiện tổn thương trên ảnh y tế, trong đó nghiên cứu tập trung chuyên sâu vào phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI (chuẩn TCGA-LGG) gồm 3.929 lát cắt của 110 bệnh nhân. Nhóm gồm hai thành viên, đóng góp 50/50."
  );
}

// ---------------------------------------------------------------------------
// 4. Slide 2 — Đặt vấn đề
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "01  ·  ĐẶT VẤN ĐỀ",
    "Vì sao cần phân đoạn khối u não tự động?",
    2,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  addText(
    slide,
    "U thần kinh đệm (Glioma) có tính xâm lấn cao. Xác định chính xác vị trí và thể tích khối u là đầu vào bắt buộc cho lập phác đồ xạ trị, phẫu thuật và theo dõi tiến triển bệnh.",
    {
      x: L.mx,
      y: 1.4,
      w: 4.1,
      h: 1.15,
      fontSize: 11,
      color: C.ink,
      lineSpacingMultiple: 1.25,
      valign: "top",
    }
  );

  addCard(slide, L.mx, 2.62, 4.1, 1.02, { fill: C.white, shadow: true });
  addText(slide, "Khoanh vùng thủ công", {
    x: L.mx + 0.22,
    y: 2.76,
    w: 3.6,
    h: 0.22,
    fontSize: 10.5,
    fontFace: FONT_STRONG,
    color: C.dark,
    valign: "middle",
  });
  addText(slide, "Hàng trăm lát cắt mỗi ca chụp, tốn thời gian và phụ thuộc chủ quan bác sĩ đọc phim.", {
    x: L.mx + 0.22,
    y: 3.02,
    w: 3.66,
    h: 0.52,
    fontSize: 9.5,
    color: C.muted,
    lineSpacingMultiple: 1.15,
    valign: "top",
  });

  addCard(slide, L.mx, 3.78, 4.1, 1.02, { fill: C.primary, line: C.primary, shadow: true });
  addText(slide, "Định hướng của đồ án", {
    x: L.mx + 0.22,
    y: 3.92,
    w: 3.6,
    h: 0.22,
    fontSize: 10.5,
    fontFace: FONT_STRONG,
    color: "9FE8DC",
    valign: "middle",
  });
  addText(slide, "Pipeline xử lý ảnh số chạy trên CPU, cho kết quả tức thời và có thể giải thích từng bước.", {
    x: L.mx + 0.22,
    y: 4.18,
    w: 3.66,
    h: 0.52,
    fontSize: 9.5,
    color: C.white,
    lineSpacingMultiple: 1.15,
    valign: "top",
  });

  addText(slide, "03 THÁCH THỨC LỚN TRÊN ẢNH MRI", {
    x: 4.95,
    y: 1.38,
    w: 4.5,
    h: 0.22,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });

  const challenges = [
    {
      title: "Tương phản thấp",
      body: "Cường độ mô u gần như trùng với vùng phù nề và chất trắng lân cận, biên mờ khó tách.",
    },
    {
      title: "Bờ khối u gồ ghề",
      body: "Bờ u xâm lấn không đều, nhiều múi, gây under-segmentation nếu chỉ dùng ngưỡng toàn cục.",
    },
    {
      title: "Nhiễu từ xương sọ",
      body: "Xương sọ và mô mềm ngoài sọ cho tín hiệu hyperintense rất mạnh, dễ bị nhận nhầm là u.",
    },
  ];
  challenges.forEach((item, index) => {
    const y = 1.66 + index * 1.12;
    numberedCard(slide, 4.95, y, 4.5, 1.06, `0${index + 1}`, item.title, item.body);
  });

  addNotes(
    slide,
    "Trường",
    "Glioma là loại u có tính xâm lấn cao, việc khoanh vùng chính xác quyết định phác đồ xạ trị. Trên ảnh MRI có ba thách thức kỹ thuật: tương phản thấp, bờ u gồ ghề và nhiễu hyperintense từ xương sọ. Đây chính là ba bài toán mà pipeline của nhóm phải giải quyết."
  );
}

// ---------------------------------------------------------------------------
// 5. Slide 3 — Mục tiêu & đóng góp
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "02  ·  MỤC TIÊU NGHIÊN CỨU",
    "Bốn mục tiêu cốt lõi và đóng góp kỹ thuật",
    3,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const goals = [
    {
      title: "Quy trình DIP khép kín",
      body: "Xử lý trọn chuỗi từ ảnh thô đến kết quả đo, triển khai bằng OpenCV trên CPU, không phụ thuộc GPU đắt tiền.",
    },
    {
      title: "Tách sọ não chính xác cao",
      body: "Quy trình 6 bước loại bỏ xương sọ và mô mềm, giữ lại trọn vẹn nhu mô não.",
    },
    {
      title: "Đối kháng 2 phương pháp",
      body: "Marker-controlled Watershed (baseline) so với Seeded Region Growing 8 láng giềng BFS.",
    },
    {
      title: "Đo lường y khoa & Web Demo",
      body: "Rút trích chỉ số hình học, đánh giá Dice/IoU và giao diện chẩn đoán tương tác cho bác sĩ.",
    },
  ];
  goals.forEach((goal, index) => {
    const x = L.mx + (index % 2) * 4.5;
    const y = 1.42 + Math.floor(index / 2) * 1.72;
    numberedCard(slide, x, y, 4.3, 1.44, `0${index + 1}`, goal.title, goal.body, {
      fill: C.white,
      badge: index % 2 === 0 ? C.primary : C.secondary,
    });
  });

  addText(slide, "Đóng góp nổi bật: bộ đánh giá định lượng chuẩn y khoa trên toàn bộ 3.929 lát cắt và Web Demo tái lập được kết quả.", {
    x: L.mx,
    y: 4.92,
    w: L.cw,
    h: 0.24,
    fontSize: 9.5,
    italic: true,
    color: C.secondary,
    valign: "middle",
  });

  addNotes(
    slide,
    "Trường",
    "Nhóm đặt bốn mục tiêu: xây dựng quy trình xử lý khép kín trên CPU, tách sọ chính xác, so sánh đối kháng hai thuật toán phân đoạn kinh điển, và cuối cùng là đo lường y khoa kèm Web Demo. Điểm nhấn là toàn bộ kết quả đều tái lập được qua các bước thực nghiệm."
  );
}

// ---------------------------------------------------------------------------
// 6. Slide 4 — Kiến trúc pipeline 4 tầng
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "03  ·  KIẾN TRÚC HỆ THỐNG",
    "Pipeline xử lý ảnh số 4 tầng",
    4,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const tiers = [
    {
      id: "T1",
      title: "Tiền xử lý",
      body: "Bilateral Filter khử nhiễu giữ cạnh + CLAHE cân bằng tương phản cục bộ",
      tags: ["Bilateral", "CLAHE"],
    },
    {
      id: "T2",
      title: "Tách sọ não (Skull Stripping)",
      body: "Sáu bước hình thái học trích xuất Brain Mask sạch xương sọ và mô mềm",
      tags: ["Otsu", "Opening", "LCC", "Fill Holes"],
    },
    {
      id: "T3",
      title: "Phân đoạn khối u lõi",
      body: "Marker-controlled Watershed (baseline) và Seeded Region Growing (đối chứng)",
      tags: ["Watershed", "Region Growing"],
    },
    {
      id: "T4",
      title: "Đặc trưng, đánh giá & Demo",
      body: "Rút trích hình học, tính Dice/IoU trên 3.929 lát cắt, xuất giao diện bác sĩ",
      tags: ["Features", "Metrics", "Streamlit"],
    },
  ];

  tiers.forEach((tier, index) => {
    const y = 1.36 + index * 0.92;
    addCard(slide, L.mx, y, L.cw, 0.82, { fill: C.white, shadow: true });
    slide.addShape(pptx.ShapeType.roundRect, {
      x: L.mx + 0.14,
      y: y + 0.16,
      w: 0.62,
      h: 0.5,
      rectRadius: 0.05,
      fill: { color: index % 2 === 0 ? C.primary : C.secondary },
      line: { color: index % 2 === 0 ? C.primary : C.secondary, width: 0.75 },
    });
    addText(slide, tier.id, {
      x: L.mx + 0.14,
      y: y + 0.16,
      w: 0.62,
      h: 0.5,
      fontSize: 12,
      fontFace: FONT_STRONG,
      color: C.white,
      align: "center",
      valign: "middle",
    });
    addText(slide, tier.title, {
      x: L.mx + 0.92,
      y: y + 0.12,
      w: 3.3,
      h: 0.26,
      fontSize: 11.5,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, tier.body, {
      x: L.mx + 0.92,
      y: y + 0.4,
      w: 4.6,
      h: 0.32,
      fontSize: 9,
      color: C.muted,
      valign: "middle",
    });

    const widths = tier.tags.map((tag) => Math.max(0.6, 0.18 + tag.length * 0.075));
    const total = widths.reduce((sum, w) => sum + w, 0) + 0.1 * (widths.length - 1);
    let tagX = L.w - L.mx - 0.16 - total;
    tier.tags.forEach((tag, tagIndex) => {
      chip(slide, tagX, y + 0.26, widths[tagIndex], 0.3, tag, {
        fill: C.tint,
        color: C.primary,
        fontSize: 8,
        bold: false,
      });
      tagX += widths[tagIndex] + 0.1;
    });
  });

  addNotes(
    slide,
    "Trường",
    "Pipeline gồm bốn tầng nối tiếp: tiền xử lý, tách sọ, phân đoạn và tầng đo lường - đánh giá. Mỗi tầng là một module độc lập trong src, có unit test riêng, nhờ vậy có thể thay thuật toán ở tầng 3 mà không ảnh hưởng các tầng còn lại."
  );
}

// ---------------------------------------------------------------------------
// 7. Slide 5 — Skull stripping 6 bước
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "04  ·  TIỀN XỬ LÝ",
    "Tách sọ não (Skull Stripping) — 6 bước hình thái học",
    5,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const steps = [
    ["Ảnh xám", "Chuẩn hóa ảnh MRI về Grayscale uint8 [0, 255]"],
    ["Ngưỡng Otsu", "Nhị phân hóa tự động tách đầu khỏi nền đen"],
    ["Opening", "Cắt cầu nối mô giữa màng não và xương sọ"],
    ["LCC", "Giữ thành phần liên thông lớn nhất (nhu mô não)"],
    ["Fill Holes", "Lấp lỗ hổng não thất bằng bù nhị phân"],
    ["Bitwise-AND", "Nhân mặt nạ não với ảnh gốc"],
  ];

  steps.forEach(([title, body], index) => {
    const y = 1.36 + index * 0.58;
    slide.addShape(pptx.ShapeType.ellipse, {
      x: L.mx,
      y: y + 0.06,
      w: 0.3,
      h: 0.3,
      fill: { color: index === 5 ? C.accent : C.primary },
      line: { color: index === 5 ? C.accent : C.primary, width: 0.75 },
    });
    addText(slide, String(index + 1), {
      x: L.mx,
      y: y + 0.06,
      w: 0.3,
      h: 0.3,
      fontSize: 9.5,
      fontFace: FONT_STRONG,
      color: C.white,
      align: "center",
      valign: "middle",
    });
    addText(slide, title, {
      x: L.mx + 0.42,
      y: y,
      w: 3.6,
      h: 0.22,
      fontSize: 10.5,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, body, {
      x: L.mx + 0.42,
      y: y + 0.22,
      w: 3.7,
      h: 0.22,
      fontSize: 8.5,
      color: C.muted,
      valign: "middle",
    });
  });

  addCard(slide, L.mx, 4.82, 4.1, 0.3, { fill: C.tint, line: C.border });
  addText(slide, "Kết quả: Brain Mask khép kín, không còn xương sọ và mô mềm", {
    x: L.mx + 0.14,
    y: 4.82,
    w: 3.85,
    h: 0.3,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.primary,
    valign: "middle",
  });

  const imgW = 4.37;
  slide.addImage({
    path: figure("skull_stripping_steps.png"),
    x: 5.08,
    y: 1.34,
    w: imgW,
    h: imgW / 1.537,
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 5.08,
    y: 1.34,
    w: imgW,
    h: imgW / 1.537,
    fill: { color: C.white, transparency: 100 },
    line: { color: C.border, width: 0.75 },
  });
  figureCaption(slide, "Hình 4.1: Sáu giai đoạn tách sọ não trên ca mẫu TCGA-LGG", 5.08, 4.22, imgW);

  addNotes(
    slide,
    "Trường",
    "Tầng tách sọ gồm sáu bước: Otsu, phép mở để cắt cầu nối mô, giữ thành phần liên thông lớn nhất, lấp lỗ hổng não thất và nhân logic với ảnh gốc. Hình bên phải là kết quả thật của cả sáu giai đoạn, cho thấy xương sọ và mô mềm đã bị loại bỏ hoàn toàn."
  );
}

// ---------------------------------------------------------------------------
// 8. Slide 6 — Watershed
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "05  ·  PHƯƠNG PHÁP A",
    "Marker-controlled Watershed — Baseline chính",
    6,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const steps = [
    "Lọc vùng não đã tách sọ, chuẩn hóa cường độ",
    "Ngưỡng hóa phân vị 85 tạo mặt nạ ứng viên u",
    "Phép mở hình thái học loại đảo nhiễu nhỏ",
    "Biến đổi khoảng cách Euclidean EDT (chuẩn L2)",
    "Xác định Sure Foreground & Sure Background",
    "Ngập lụt Watershed có ràng buộc marker, chặn tràn cạnh",
    "Lọc đảo nhỏ theo ngưỡng min_tumor_area",
  ];

  steps.forEach((step, index) => {
    const y = 1.36 + index * 0.42;
    addCard(slide, L.mx, y, 4.75, 0.36, { fill: C.white, line: C.border });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: L.mx + 0.12,
      y: y + 0.09,
      w: 0.18,
      h: 0.18,
      fill: { color: C.primary },
      line: { color: C.primary, width: 0.5 },
    });
    addText(slide, step, {
      x: L.mx + 0.4,
      y,
      w: 4.2,
      h: 0.36,
      fontSize: 9.5,
      color: C.ink,
      valign: "middle",
    });
  });

  formulaCard(slide, 5.55, 1.36, 3.9, 1.34, {
    tag: "BIẾN ĐỔI KHOẢNG CÁCH",
    formula: "D(x, y) = min ‖ (x, y) − b ‖₂",
    caption: "b là pixel nền gần nhất; đỉnh cực đại của D chính là tâm khối u.",
  });

  formulaCard(slide, 5.55, 2.8, 3.9, 1.34, {
    tag: "NGƯỠNG HẠT GIỐNG",
    formula: "M = { p | D(p) > 0.4 · max D }",
    caption: "Marker = Sure Foreground; vùng nền chắc chắn làm biên chặn ngập lụt.",
  });

  addCard(slide, 5.55, 4.24, 3.9, 0.88, { fill: C.primary, line: C.primary, shadow: true });
  addText(slide, "Ưu điểm", {
    x: 5.75,
    y: 4.32,
    w: 3.5,
    h: 0.2,
    fontSize: 9,
    fontFace: FONT_STRONG,
    color: "9FE8DC",
    charSpacing: 1.2,
    valign: "middle",
  });
  addText(slide, "Tách xuất sắc khối u nhiều tâm hoặc cụm u tiếp giáp nhờ neo hạt giống tại đỉnh EDT.", {
    x: 5.75,
    y: 4.54,
    w: 3.5,
    h: 0.52,
    fontSize: 9,
    color: C.white,
    lineSpacingMultiple: 1.15,
    valign: "top",
  });

  addNotes(
    slide,
    "Trường",
    "Phương án A là Marker-controlled Watershed. Điểm mấu chốt là biến đổi khoảng cách Euclidean: đỉnh của bản đồ khoảng cách cho ta tâm khối u, từ đó sinh marker và chạy Watershed có ràng buộc để chặn hiện tượng tràn biên. Thuật toán rất mạnh với khối u nhiều tâm."
  );
}

// ---------------------------------------------------------------------------
// 9. Slide 7 — Region Growing
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "06  ·  PHƯƠNG PHÁP B",
    "Seeded Region Growing 8 láng giềng (BFS) — Đối chứng",
    7,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  formulaCard(slide, L.mx, 1.36, 3.9, 1.34, {
    tag: "HẠT GIỐNG TỰ ĐỘNG",
    formula: "s = argmax I(p),  p ∈ Brain",
    caption: "Chọn pixel sáng nhất trong nhu mô não đã tách sọ làm điểm hạt giống.",
  });

  formulaCard(slide, L.mx, 2.8, 3.9, 1.34, {
    tag: "ĐIỀU KIỆN LAN TRUYỀN",
    formula: "| I(p) − I(s) | ≤ τ,  τ = 15",
    caption: "Duyệt hàng đợi BFS 8 hướng, kết nạp láng giềng thỏa ngưỡng dung sai cường độ.",
  });

  addCard(slide, L.mx, 4.26, 3.9, 0.72, { fill: C.cardAlt, line: C.border });
  addText(slide, "Hậu xử lý: lấp lỗ hổng + lọc đảo u ngoài khoảng [50, 25.000] pixel", {
    x: L.mx + 0.16,
    y: 4.26,
    w: 3.6,
    h: 0.72,
    fontSize: 8.5,
    color: C.ink,
    lineSpacingMultiple: 1.15,
    valign: "middle",
  });

  const steps = [
    ["Tìm hạt giống", "Cực đại cường độ trong vùng não"],
    ["Lan truyền BFS", "Hàng đợi FIFO, 8 láng giềng liên thông"],
    ["Kiểm tra dung sai", "Chênh lệch cường độ so với hạt giống"],
    ["Kết nạp pixel", "Đánh dấu thuộc vùng u, đẩy vào hàng đợi"],
    ["Lặp đến khi rỗng", "Vùng u khép kín, không vỡ vụn"],
    ["Hậu xử lý", "Lấp lỗ hổng mô hoại tử bên trong u"],
  ];
  steps.forEach(([title, body], index) => {
    const y = 1.36 + index * 0.56;
    addCard(slide, 4.6, y, 4.85, 0.48, { fill: C.white, shadow: false });
    addText(slide, `${index + 1}. ${title}`, {
      x: 4.74,
      y: y + 0.06,
      w: 2.1,
      h: 0.18,
      fontSize: 9.5,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, body, {
      x: 4.74,
      y: y + 0.24,
      w: 4.55,
      h: 0.18,
      fontSize: 8.5,
      color: C.muted,
      valign: "middle",
    });
  });

  addCard(slide, 4.6, 4.78, 4.85, 0.34, { fill: C.primary, line: C.primary });
  addText(slide, "Ưu điểm: ~12 ms/lát, mặt nạ u liền mạch", {
    x: 4.74,
    y: 4.78,
    w: 4.6,
    h: 0.34,
    fontSize: 9,
    fontFace: FONT_STRONG,
    color: C.white,
    valign: "middle",
  });

  addNotes(
    slide,
    "Trường",
    "Phương án B là Seeded Region Growing. Hạt giống lấy tại pixel sáng nhất trong não, sau đó lan truyền BFS 8 hướng với dung sai cường độ 15. Thuật toán rất nhanh và cho mặt nạ liền mạch, nhưng phụ thuộc hoàn toàn vào chất lượng hạt giống - đây là điểm yếu sẽ thấy rõ trong phần kết quả."
  );
}

// ---------------------------------------------------------------------------
// 10. Slide 8 — Tập dữ liệu
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "07  ·  DỮ LIỆU",
    "Tập dữ liệu TCGA-LGG và quy trình chuẩn hóa",
    8,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const kpis = [
    { value: "3.929", label: "lát cắt MRI 2D" },
    { value: "110", label: "bệnh nhân ung thư não cấp thấp" },
    { value: "256 × 256", label: "pixel, thang xám uint8" },
  ];
  kpis.forEach((kpi, index) => {
    kpiCard(slide, L.mx + index * 3.06, 1.36, 2.86, 0.96, kpi.value, kpi.label);
  });

  addCard(slide, L.mx, 2.5, L.cw, 0.92, { fill: C.white, shadow: true });
  addText(slide, "CHUẨN HÓA DỮ LIỆU", {
    x: L.mx + 0.24,
    y: 2.62,
    w: 2.2,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });
  addText(
    slide,
    "Chuỗi xung FLAIR / T1-weighted, kích thước đồng nhất 256 × 256, mặt nạ Ground Truth nhị phân {0, 255} do chuyên gia y tế gắn nhãn.",
    {
      x: L.mx + 2.4,
      y: 2.62,
      w: 6.3,
      h: 0.66,
      fontSize: 9.5,
      color: C.ink,
      lineSpacingMultiple: 1.15,
      valign: "middle",
    }
  );

  addText(slide, "PHÂN NHÓM ĐỘ KHÓ THEO DIỆN TÍCH U", {
    x: L.mx,
    y: 3.56,
    w: 6,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });

  const groups = [
    { title: "U lớn, rõ nét", value: "> 5%", body: "Biên u rõ, độ tương phản cao" },
    { title: "U trung bình", value: "1,5 – 5%", body: "Bờ u tương đối rõ, có phù nề nhẹ" },
    { title: "U nhỏ, bờ mờ", value: "< 1,5%", body: "Thách thức: dễ mất đỉnh EDT" },
  ];
  groups.forEach((group, index) => {
    const x = L.mx + index * 3.06;
    addCard(slide, x, 3.8, 2.86, 1.12, { fill: C.card, line: C.border });
    addText(slide, group.value, {
      x: x + 0.2,
      y: 3.9,
      w: 2.46,
      h: 0.34,
      fontSize: 17,
      fontFace: FONT_STRONG,
      color: index === 2 ? C.warn : C.primary,
      valign: "middle",
    });
    addText(slide, group.title, {
      x: x + 0.2,
      y: 4.24,
      w: 2.46,
      h: 0.22,
      fontSize: 9.5,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, group.body, {
      x: x + 0.2,
      y: 4.46,
      w: 2.46,
      h: 0.36,
      fontSize: 8.5,
      color: C.muted,
      lineSpacingMultiple: 1.1,
      valign: "top",
    });
  });

  addNotes(
    slide,
    "Trí",
    "Bộ dữ liệu gồm 3.929 lát cắt của 110 bệnh nhân TCGA-LGG, trong đó 1.373 lát có u. Toàn bộ đã chuẩn hóa về 256 nhân 256, thang xám, kèm mặt nạ ground truth do chuyên gia gắn nhãn. Nhóm chia ba mức độ khó theo diện tích u để kiểm thử tính bền vững."
  );
}

// ---------------------------------------------------------------------------
// 11. Slide 9 — Đặc trưng hình học
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "08  ·  ĐO LƯỜNG",
    "Rút trích đặc trưng hình học khối u",
    9,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const cards = [
    {
      tag: "TỶ LỆ CHIẾM DỤNG MÔ NÃO",
      label: "Tỷ lệ =",
      numerator: [
        { text: "S", options: { italic: true, fontSize: 13, color: C.ink } },
        { text: "tumor", options: { italic: true, subscript: true, fontSize: 13, color: C.ink } },
      ],
      denominator: [
        { text: "S", options: { italic: true, fontSize: 13, color: C.ink } },
        { text: "brain", options: { italic: true, subscript: true, fontSize: 13, color: C.ink } },
      ],
      suffix: "× 100%",
      caption: "Chỉ số định lượng mức độ chiếm dụng mô não, theo dõi tiến triển giữa các lần chụp.",
    },
    {
      tag: "ĐỘ TRÒN (CIRCULARITY)",
      label: "C =",
      numerator: "4π · A",
      denominator: "P²",
      caption: "A là diện tích, P là chu vi contour; C tiến về 1 khi bờ u tròn đều.",
    },
  ];

  cards.forEach((card, index) => {
    const x = L.mx + index * 4.56;
    addCard(slide, x, 1.36, 4.34, 1.58, { fill: C.white, shadow: true });
    addText(slide, card.tag, {
      x: x + 0.22,
      y: 1.48,
      w: 3.9,
      h: 0.22,
      fontSize: 8.5,
      fontFace: FONT_STRONG,
      color: C.secondary,
      charSpacing: 1.1,
      valign: "middle",
    });
    fractionBlock(slide, {
      x: x + 0.26,
      y: 1.76,
      w: 3.82,
      h: 0.66,
      label: card.label,
      numerator: card.numerator,
      denominator: card.denominator,
      suffix: card.suffix,
      fontSize: 13,
      labelW: index === 0 ? 0.95 : 0.6,
    });
    addText(slide, card.caption, {
      x: x + 0.22,
      y: 2.48,
      w: 3.9,
      h: 0.38,
      fontSize: 8.5,
      color: C.muted,
      lineSpacingMultiple: 1.12,
      valign: "top",
    });
  });

  addCard(slide, L.mx, 3.06, L.cw, 0.92, { fill: C.white, shadow: true });
  addText(slide, "DIỆN TÍCH KHỐI U", {
    x: L.mx + 0.24,
    y: 3.18,
    w: 3,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });
  slide.addText(
    [
      { text: "S", options: { italic: true, fontSize: 14, color: C.dark } },
      { text: "tumor", options: { italic: true, subscript: true, fontSize: 14, color: C.dark } },
      { text: " = Σ P(x, y)", options: { italic: true, fontSize: 14, color: C.dark } },
    ],
    {
      x: L.mx + 0.24,
      y: 3.42,
      w: 3.2,
      h: 0.4,
      fontFace: FONT,
      align: "left",
      valign: "middle",
      margin: 0,
    }
  );
  addText(slide, "Đếm pixel dương tính của mặt nạ u; quy đổi mm² theo pixel spacing của thiết bị chụp.", {
    x: L.mx + 3.7,
    y: 3.3,
    w: 4.9,
    h: 0.5,
    fontSize: 9,
    color: C.muted,
    lineSpacingMultiple: 1.15,
    valign: "middle",
  });

  addText(slide, "Ý NGHĨA CHẨN ĐOÁN", {
    x: L.mx,
    y: 4.08,
    w: 3,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });

  const meaning = [
    ["C ≈ 1", "Bờ u tròn đều, gợi ý u lành tính có vỏ bọc (Meningioma).", C.primary],
    ["C ≪ 1", "Bờ gồ ghề, xâm lấn mô xung quanh, cảnh báo ác tính (Glioma).", C.warn],
    ["Tỷ lệ", "Mức chiếm dụng mô não theo từng lát cắt của bệnh nhân.", C.primary],
  ];
  meaning.forEach(([label, body, color], index) => {
    const x = L.mx + index * 3.06;
    addCard(slide, x, 4.32, 2.86, 0.66, { fill: C.card, line: C.border });
    addText(slide, label, {
      x: x + 0.18,
      y: 4.4,
      w: 1.1,
      h: 0.22,
      fontSize: 10,
      fontFace: FONT_STRONG,
      italic: true,
      color,
      valign: "middle",
    });
    addText(slide, body, {
      x: x + 0.18,
      y: 4.62,
      w: 2.5,
      h: 0.3,
      fontSize: 8,
      color: C.muted,
      lineSpacingMultiple: 1.05,
      valign: "top",
    });
  });

  addNotes(
    slide,
    "Trí",
    "Nhóm rút trích ba đặc trưng: diện tích, tỷ lệ u trên não và độ tròn. Độ tròn là chỉ số có ý nghĩa lâm sàng rõ nhất: gần 1 là bờ tròn đều, càng nhỏ càng gợi ý bờ xâm lấn. Ngoài ra hệ thống còn xuất bounding box để bác sĩ định vị nhanh."
  );
}

// ---------------------------------------------------------------------------
// 12. Slide 10 — Chỉ số đánh giá
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "09  ·  ĐÁNH GIÁ ĐỊNH LƯỢNG",
    "Bốn thước đo vàng trong đánh giá phân đoạn y khoa",
    10,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const metrics = [
    {
      tag: "DICE SIMILARITY (DSC)",
      label: "DSC =",
      numerator: "2|A ∩ B|",
      denominator: "|A| + |B|",
      caption: "Mức độ tương đồng toàn diện giữa dự đoán A và ground truth B.",
    },
    {
      tag: "INTERSECTION OVER UNION",
      label: "IoU =",
      numerator: "|A ∩ B|",
      denominator: "|A ∪ B|",
      caption: "Chỉ số Jaccard, phạt nặng các vùng dự đoán thừa.",
    },
    {
      tag: "ĐỘ NHẠY (SENSITIVITY)",
      label: "Sens =",
      numerator: "TP",
      denominator: "TP + FN",
      caption: "Khả năng không bỏ sót tế bào ung thư — ưu tiên hàng đầu.",
    },
    {
      tag: "ĐỘ ĐẶC HIỆU (SPECIFICITY)",
      label: "Spec =",
      numerator: "TN",
      denominator: "TN + FP",
      caption: "Khả năng tránh báo động giả trên mô lành.",
    },
  ];

  metrics.forEach((metric, index) => {
    const x = L.mx + (index % 2) * 4.56;
    const y = 1.36 + Math.floor(index / 2) * 1.62;
    addCard(slide, x, y, 4.34, 1.5, { fill: C.white, shadow: true });
    addText(slide, metric.tag, {
      x: x + 0.22,
      y: y + 0.12,
      w: 3.9,
      h: 0.2,
      fontSize: 8.5,
      fontFace: FONT_STRONG,
      color: C.secondary,
      charSpacing: 1.1,
      valign: "middle",
    });
    fractionBlock(slide, {
      x: x + 0.26,
      y: y + 0.36,
      w: 3.82,
      h: 0.64,
      label: metric.label,
      numerator: metric.numerator,
      denominator: metric.denominator,
      fontSize: 13,
      labelW: 0.86,
    });
    addText(slide, metric.caption, {
      x: x + 0.22,
      y: y + 1.06,
      w: 3.9,
      h: 0.38,
      fontSize: 8.5,
      color: C.muted,
      lineSpacingMultiple: 1.12,
      valign: "top",
    });
  });

  addText(
    slide,
    "Đánh giá trên 1.373 lát cắt có u và kiểm chứng dương tính giả trên 2.556 lát não lành.",
    {
      x: L.mx,
      y: 4.62,
      w: L.cw,
      h: 0.24,
      fontSize: 9,
      italic: true,
      color: C.secondary,
      valign: "middle",
    }
  );

  addNotes(
    slide,
    "Trí",
    "Bốn chỉ số chuẩn y khoa: Dice và IoU đo mức tương đồng, Sensitivity đo khả năng không bỏ sót u, Specificity đo khả năng tránh báo động giả. Nhóm đánh giá trên 1.373 lát có u và kiểm tra dương tính giả trên 2.556 lát não lành."
  );
}

// ---------------------------------------------------------------------------
// 13. Slide 11 — Bảng kết quả
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "10  ·  KẾT QUẢ THỰC NGHIỆM",
    "So sánh định lượng trên 3.929 lát cắt TCGA-LGG",
    11,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const head = (text, align) => ({
    text,
    options: {
      bold: true,
      color: C.white,
      fill: { color: C.primary },
      align: align || "center",
      fontSize: 9.5,
      fontFace: FONT_STRONG,
    },
  });
  const cell = (text, opts = {}) => ({
    text,
    options: {
      color: opts.color || C.ink,
      bold: opts.bold || false,
      align: opts.align || "center",
      fill: { color: opts.fill || C.white },
      fontSize: 9.5,
    },
  });

  const rows = [
    [head("Chỉ số (Mean ± Std)"), head("Watershed (Baseline)"), head("Region Growing (Đối chứng)"), head("Chênh lệch")],
    [
      cell("Dice (DSC / F1)", { align: "left", bold: true }),
      cell("0,4446 ± 0,3014", { bold: true, color: C.primary }),
      cell("0,1990 ± 0,2682"),
      cell("+123%", { color: C.accent, bold: true }),
    ],
    [
      cell("IoU (Jaccard)", { align: "left", bold: true }),
      cell("0,3368 ± 0,2677", { bold: true, color: C.primary }),
      cell("0,1416 ± 0,2119"),
      cell("+138%", { color: C.accent, bold: true }),
    ],
    [
      cell("Sensitivity", { align: "left", bold: true }),
      cell("0,4436 ± 0,3170", { bold: true, color: C.primary }),
      cell("0,2226 ± 0,3221"),
      cell("+99%", { color: C.accent, bold: true }),
    ],
    [
      cell("Specificity", { align: "left", bold: true }),
      cell("0,9915 ± 0,0107", { bold: true, color: C.primary }),
      cell("0,9851 ± 0,0432"),
      cell("+0,6%", { color: C.accent, bold: true }),
    ],
    [
      cell("Độ trễ / lát cắt", { align: "left", bold: true }),
      cell("6,13 ± 3,32 ms", { bold: true, color: C.primary }),
      cell("12,13 ± 22,83 ms"),
      cell("nhanh gấp 2", { color: C.accent, bold: true }),
    ],
  ];

  slide.addTable(rows, {
    x: L.mx,
    y: 1.36,
    w: L.cw,
    colW: [2.45, 2.35, 2.55, 1.55],
    rowH: [0.36, 0.38, 0.38, 0.38, 0.38, 0.38],
    border: { type: "solid", pt: 0.75, color: C.border },
    fontFace: FONT,
    valign: "middle",
    margin: 0.06,
  });

  figureCaption(slide, "Bảng 6.1: Kết quả trên 1.373 lát cắt có u (Mean ± Std) — số liệu trích từ báo cáo đồ án", L.mx, 3.72, L.cw);

  const insights = [
    { value: "2,23×", label: "Dice của Watershed so với Region Growing" },
    { value: "0,9915", label: "Specificity — gần như không báo động giả" },
    { value: "2.556", label: "lát não lành kiểm chứng dương tính giả" },
  ];
  insights.forEach((item, index) => {
    const x = L.mx + index * 3.06;
    addCard(slide, x, 4.06, 2.86, 0.9, { fill: C.primary, line: C.primary });
    addText(slide, item.value, {
      x: x + 0.2,
      y: 4.16,
      w: 2.4,
      h: 0.34,
      fontSize: 17,
      fontFace: FONT_STRONG,
      color: C.white,
      valign: "middle",
    });
    addText(slide, item.label, {
      x: x + 0.2,
      y: 4.48,
      w: 2.46,
      h: 0.36,
      fontSize: 8,
      color: "CBE8EF",
      lineSpacingMultiple: 1.1,
      valign: "top",
    });
  });

  addNotes(
    slide,
    "Trí",
    "Đây là bảng kết quả trung tâm của đồ án. Watershed đạt Dice 0,4446, gấp 2,23 lần Region Growing, và nhanh gấp đôi. Cả hai đều giữ Specificity trên 98,5 phần trăm, nghĩa là bước tách sọ đã triệt tiêu dương tính giả rất tốt."
  );
}

// ---------------------------------------------------------------------------
// 14. Slide 12 — Biểu đồ
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "11  ·  PHÂN TÍCH ĐỊNH LƯỢNG",
    "Phân bố chỉ số và đối sánh trực quan",
    12,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const notes = [
    ["Trung vị Dice", "0,41 (Watershed) so với 0,14 (Region Growing)"],
    ["Độ phân tán", "Hộp của Watershed tập trung hơn, ít ngoại lai suy giảm"],
    ["Điểm sụp", "Region Growing về 0 ở nhiều ca u nhỏ do lệch hạt giống"],
  ];
  notes.forEach(([title, body], index) => {
    const y = 1.36 + index * 1.02;
    addCard(slide, L.mx, y, 4.42, 0.88, { fill: C.white, shadow: true });
    addText(slide, title, {
      x: L.mx + 0.2,
      y: y + 0.12,
      w: 4.0,
      h: 0.22,
      fontSize: 10,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, body, {
      x: L.mx + 0.2,
      y: y + 0.36,
      w: 4.02,
      h: 0.42,
      fontSize: 8.5,
      color: C.muted,
      lineSpacingMultiple: 1.15,
      valign: "top",
    });
  });

  addCard(slide, L.mx, 4.44, 4.42, 0.62, { fill: C.tint, line: C.border });
  addText(slide, "Kết luận: Watershed ổn định hơn khi mở rộng quy mô dữ liệu.", {
    x: L.mx + 0.2,
    y: 4.44,
    w: 4.05,
    h: 0.62,
    fontSize: 9,
    fontFace: FONT_STRONG,
    color: C.primary,
    valign: "middle",
  });

  const imgX = 5.28;
  const imgW = 4.18;
  slide.addImage({
    path: figure("benchmark_metrics_comparison.png"),
    x: imgX,
    y: 1.36,
    w: imgW,
    h: imgW / 2.705,
  });
  figureCaption(slide, "Hình 6.1: Phân bố Dice, IoU, Sensitivity và so sánh trên 20 ca tiêu biểu", imgX, 2.94, imgW);

  slide.addImage({
    path: figure("benchmark_distribution.png"),
    x: imgX,
    y: 3.24,
    w: imgW,
    h: imgW / 3.877,
  });
  figureCaption(slide, "Hình 6.2: Bốn ca thất bại điển hình — Dice = 0 ở cả hai phương pháp", imgX, 4.4, imgW);

  addNotes(
    slide,
    "Trí",
    "Hai biểu đồ này giải thích vì sao Watershed thắng: hộp phân phối Dice của Watershed nằm cao hơn và ổn định hơn, trong khi Region Growing lao dốc về 0 ở nhiều ca. Biểu đồ cột bên phải cho thấy Watershed vượt trội ở gần như mọi ca tiêu biểu."
  );
}

// ---------------------------------------------------------------------------
// 15. Slide 13 — Khảo sát siêu tham số
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "12  ·  TỐI ƯU SIÊU THAM SỐ",
    "Khảo sát độ nhạy tham số phân đoạn Watershed",
    13,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const imgW = 5.12;
  slide.addImage({
    path: figure("watershed_param_sensitivity.png"),
    x: L.mx,
    y: 1.42,
    w: imgW,
    h: imgW / 2.555,
  });
  figureCaption(slide, "Hình 5.1: Khảo sát dist_thresh_ratio trên 30 lát cắt có u", L.mx, 3.66, imgW);

  addCard(slide, L.mx, 3.98, imgW, 1.06, { fill: C.white, shadow: true });
  addText(slide, "NHẬN XÉT", {
    x: L.mx + 0.22,
    y: 4.08,
    w: 2,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.1,
    valign: "middle",
  });
  addText(
    slide,
    "Dice đạt cực đại tại 0,4 và giảm nhẹ ở hai biên; Specificity giữ gần 1,0 trên toàn dải khảo sát.",
    {
      x: L.mx + 0.22,
      y: 4.3,
      w: imgW - 0.44,
      h: 0.62,
      fontSize: 8.5,
      color: C.ink,
      lineSpacingMultiple: 1.15,
      valign: "top",
    }
  );

  const params = [
    {
      tag: "dist_thresh_ratio",
      value: "0,2 → 0,6",
      body: "Khảo sát 5 mốc; ngưỡng càng cao thì hạt giống càng thưa, u nhỏ dễ mất đỉnh EDT.",
    },
    {
      tag: "min_tumor_area",
      value: "20 → 100 px",
      body: "Ngưỡng lọc đảo nhiễu; quá lớn sẽ cắt tỉa cả u nhỏ dưới 1,5% diện tích não.",
    },
  ];
  params.forEach((param, index) => {
    const y = 1.42 + index * 1.18;
    addCard(slide, 5.9, y, 3.55, 1.02, { fill: C.white, shadow: true });
    addText(slide, param.tag, {
      x: 6.06,
      y: y + 0.1,
      w: 3.2,
      h: 0.2,
      fontSize: 8.5,
      fontFace: FONT_MONO,
      color: C.secondary,
      valign: "middle",
    });
    addText(slide, param.value, {
      x: 6.06,
      y: y + 0.3,
      w: 3.2,
      h: 0.26,
      fontSize: 12,
      fontFace: FONT_STRONG,
      color: C.primary,
      valign: "middle",
    });
    addText(slide, param.body, {
      x: 6.06,
      y: y + 0.58,
      w: 3.2,
      h: 0.4,
      fontSize: 8,
      color: C.muted,
      lineSpacingMultiple: 1.1,
      valign: "top",
    });
  });

  addCard(slide, 5.9, 3.78, 3.55, 1.26, { fill: C.primary, line: C.primary, shadow: true });
  addText(slide, "ĐIỂM NGỌT TỐI ƯU", {
    x: 6.06,
    y: 3.88,
    w: 3.2,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: "9FE8DC",
    charSpacing: 1.2,
    valign: "middle",
  });
  addText(slide, "dist_thresh_ratio = 0,4", {
    x: 6.06,
    y: 4.10,
    w: 3.2,
    h: 0.26,
    fontSize: 14,
    fontFace: FONT_STRONG,
    color: C.white,
    valign: "middle",
  });
  addText(slide, "min_tumor_area = 50 px", {
    x: 6.06,
    y: 4.36,
    w: 3.2,
    h: 0.26,
    fontSize: 14,
    fontFace: FONT_STRONG,
    color: C.white,
    valign: "middle",
  });
  addText(slide, "Trùng khớp giá trị mặc định của hệ thống.", {
    x: 6.06,
    y: 4.64,
    w: 3.2,
    h: 0.3,
    fontSize: 8.5,
    color: "CBE8EF",
    valign: "middle",
  });

  addNotes(
    slide,
    "Trường",
    "Nhóm khảo sát dist_thresh_ratio từ 0,2 đến 0,6 trên 30 lát cắt có u. Dice đạt cực đại tại 0,4, đúng bằng giá trị mặc định đang dùng; đây là bằng chứng thực nghiệm cho việc chọn siêu tham số. min_tumor_area được giữ ở 50 pixel để cân bằng giữa lọc nhiễu và bảo toàn u nhỏ."
  );
}

// ---------------------------------------------------------------------------
// 16. Slide 14 — Failure cases
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "13  ·  GIỚI HẠN PHƯƠNG PHÁP",
    "Phân tích ca thất bại và biện pháp khắc phục",
    14,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const cases = [
    {
      tag: "CA 1  ·  U VI THỂ",
      title: "Khối u nhỏ dưới 1,5% diện tích sọ",
      body: "Bộ lọc diện tích cắt tỉa nhầm, hoặc biến đổi khoảng cách EDT không hình thành đỉnh cực đại nên không sinh được hạt giống.",
    },
    {
      tag: "CA 2  ·  PHÙ NỀO LAN RỘNG",
      title: "Vasogenic Edema bao quanh u",
      body: "Gradient ranh giới mờ khiến Watershed under-segmentation, hoặc hạt giống rò rỉ sang vùng phù nề (leakage).",
    },
  ];

  cases.forEach((item, index) => {
    const y = 1.36 + index * 1.36;
    addCard(slide, L.mx, y, 4.4, 1.2, { fill: C.warnBg, line: "F0D9B5", shadow: true });
    addText(slide, item.tag, {
      x: L.mx + 0.22,
      y: y + 0.12,
      w: 3.9,
      h: 0.2,
      fontSize: 8,
      fontFace: FONT_STRONG,
      color: C.warn,
      charSpacing: 1.1,
      valign: "middle",
    });
    addText(slide, item.title, {
      x: L.mx + 0.22,
      y: y + 0.34,
      w: 3.96,
      h: 0.24,
      fontSize: 10.5,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, item.body, {
      x: L.mx + 0.22,
      y: y + 0.6,
      w: 3.96,
      h: 0.52,
      fontSize: 8.5,
      color: C.ink,
      lineSpacingMultiple: 1.15,
      valign: "top",
    });
  });

  addCard(slide, 5.2, 1.36, 4.25, 2.56, { fill: C.white, shadow: true });
  addText(slide, "BIỆN PHÁP ĐÃ ÁP DỤNG", {
    x: 5.42,
    y: 1.48,
    w: 3.8,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });

  const fixes = [
    "Bilateral Filter bảo toàn độ dốc biên, tránh nhòe ranh giới u",
    "Điều chỉnh dung sai phân vị thích ứng theo phân bố cường độ",
    "Lọc đảo nhiễu theo ngưỡng diện tích thay vì diện tích tuyệt đối",
  ];
  bullets(slide, fixes, { x: 5.42, y: 1.78, w: 3.82, h: 1.4, fontSize: 9.5, gap: 8 });

  addCard(slide, 5.2, 4.06, 4.25, 0.98, { fill: C.card, line: C.border });
  addText(slide, "Định hướng khắc phục triệt để", {
    x: 5.42,
    y: 4.16,
    w: 3.8,
    h: 0.22,
    fontSize: 9.5,
    fontFace: FONT_STRONG,
    color: C.primary,
    valign: "middle",
  });
  addText(slide, "Bổ sung đặc trưng kết cấu GLCM hoặc ngưỡng thích ứng cục bộ cho vùng u mờ.", {
    x: 5.42,
    y: 4.4,
    w: 3.82,
    h: 0.52,
    fontSize: 8.5,
    color: C.muted,
    lineSpacingMultiple: 1.15,
    valign: "top",
  });

  addNotes(
    slide,
    "Trường",
    "Nhóm phân tích hai nhóm ca thất bại điển hình: u vi thể dưới 1,5% diện tích sọ và u có phù nề lan rộng. Nguyên nhân đều nằm ở bước sinh hạt giống. Nhóm đã áp dụng ba biện pháp: bảo toàn biên bằng bilateral, dung sai thích ứng và lọc đảo nhiễu theo ngưỡng diện tích."
  );
}

// ---------------------------------------------------------------------------
// 17. Slide 15 — Web Demo
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "14  ·  ỨNG DỤNG DEMO",
    "Web Demo tương tác Streamlit cho bác sĩ X-quang",
    15,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  // Mock giao diện
  addCard(slide, L.mx, 1.34, 5.3, 3.62, { fill: C.white, shadow: true });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: L.mx + 0.02,
    y: 1.36,
    w: 5.26,
    h: 0.34,
    rectRadius: 0.04,
    fill: { color: C.dark },
    line: { color: C.dark, width: 0.75 },
  });
  [0.18, 0.36, 0.54].forEach((offset, index) => {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: L.mx + offset,
      y: 1.46,
      w: 0.12,
      h: 0.12,
      fill: { color: index === 0 ? "E26D6D" : index === 1 ? "E3B341" : "57B894" },
      line: { color: index === 0 ? "E26D6D" : index === 1 ? "E3B341" : "57B894", width: 0.5 },
    });
  });
  addText(slide, "Brain Tumor MRI Segmentation  ·  Streamlit", {
    x: L.mx + 0.76,
    y: 1.36,
    w: 4.2,
    h: 0.34,
    fontSize: 8,
    color: "CBE8EF",
    valign: "middle",
  });

  // Sidebar điều khiển
  slide.addShape(pptx.ShapeType.rect, {
    x: L.mx + 0.02,
    y: 1.7,
    w: 1.55,
    h: 3.24,
    fill: { color: C.card },
    line: { color: C.border, width: 0.75 },
  });
  addText(slide, "TẢI ẢNH", {
    x: L.mx + 0.16,
    y: 1.8,
    w: 1.25,
    h: 0.18,
    fontSize: 7,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1,
    valign: "middle",
  });
  chip(slide, L.mx + 0.13, 2.0, 1.33, 0.32, "Chọn tệp MRI", {
    fill: C.white,
    color: C.primary,
    fontSize: 7.5,
  });
  addText(slide, "THUẬT TOÁN", {
    x: L.mx + 0.16,
    y: 2.44,
    w: 1.25,
    h: 0.18,
    fontSize: 7,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1,
    valign: "middle",
  });
  chip(slide, L.mx + 0.13, 2.64, 1.33, 0.3, "Watershed", { fill: C.primary, color: C.white, fontSize: 7.5 });
  chip(slide, L.mx + 0.13, 2.98, 1.33, 0.3, "Region Growing", { fill: C.white, color: C.muted, fontSize: 7.5 });
  addText(slide, "NGUỒN DỮ LIỆU", {
    x: L.mx + 0.16,
    y: 3.4,
    w: 1.25,
    h: 0.18,
    fontSize: 7,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1,
    valign: "middle",
  });
  chip(slide, L.mx + 0.13, 3.6, 1.33, 0.3, "TCGA-LGG", { fill: C.white, color: C.muted, fontSize: 7.5 });
  addText(slide, "Light theme  ·  Tiếng Việt", {
    x: L.mx + 0.16,
    y: 4.5,
    w: 1.3,
    h: 0.18,
    fontSize: 6.5,
    color: C.muted,
    valign: "middle",
  });

  // Vùng hiển thị 4 khung
  addText(slide, "VÙNG HIỂN THỊ 4 KHUNG SO SÁNH", {
    x: L.mx + 1.72,
    y: 1.78,
    w: 3.5,
    h: 0.18,
    fontSize: 6.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 0.9,
    valign: "middle",
  });

  const panes = [
    ["Ảnh gốc", "256 × 256 · FLAIR", 1.59, 2.02],
    ["Não tách sọ", "Brain Mask", 3.43, 2.02],
    ["Mặt nạ u", "Mặt nạ nhị phân", 1.59, 3.24],
    ["Bounding Box", "Tâm khối u", 3.43, 3.24],
  ];
  panes.forEach(([label, detail, x, y]) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: L.mx + x,
      y,
      w: 1.76,
      h: 1.1,
      rectRadius: 0.04,
      fill: { color: C.cardAlt },
      line: { color: C.border, width: 0.75 },
    });
    addText(slide, label, {
      x: L.mx + x,
      y: y + 0.34,
      w: 1.76,
      h: 0.26,
      fontSize: 7.5,
      fontFace: FONT_STRONG,
      color: C.ink,
      align: "center",
      valign: "middle",
    });
    addText(slide, detail, {
      x: L.mx + x,
      y: y + 0.6,
      w: 1.76,
      h: 0.22,
      fontSize: 6.5,
      color: C.muted,
      align: "center",
      valign: "middle",
    });
  });

  addCard(slide, L.mx + 1.59, 4.5, 3.6, 0.3, { fill: C.tint, line: C.border });
  addText(slide, "KPI: Diện tích  ·  Độ tròn  ·  Thời gian xử lý", {
    x: L.mx + 1.69,
    y: 4.5,
    w: 3.4,
    h: 0.3,
    fontSize: 7,
    fontFace: FONT_STRONG,
    color: C.primary,
    align: "center",
    valign: "middle",
  });

  // Cột tính năng
  const features = [
    ["Giao diện sáng, tiếng Việt", "Light theme trang nhã, font tiếng Việt có dấu 100%."],
    ["Tải ảnh tùy ý", "Hỗ trợ upload MRI hoặc chọn ca có sẵn trong TCGA-LGG."],
    ["Chuyển thuật toán tức thì", "Toggle giữa Watershed và Region Growing ngay trên sidebar."],
    ["Xuất kết quả", "Tải ảnh phân đoạn và bảng chỉ số phục vụ hồ sơ bệnh án."],
  ];
  features.forEach(([title, body], index) => {
    const y = 1.34 + index * 0.94;
    addCard(slide, 6.06, y, 3.39, 0.82, { fill: C.white, shadow: true });
    addText(slide, title, {
      x: 6.22,
      y: y + 0.1,
      w: 3.06,
      h: 0.22,
      fontSize: 10,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, body, {
      x: 6.22,
      y: y + 0.34,
      w: 3.06,
      h: 0.4,
      fontSize: 8.5,
      color: C.muted,
      lineSpacingMultiple: 1.15,
      valign: "top",
    });
  });

  addNotes(
    slide,
    "Trí",
    "Web Demo viết bằng Streamlit, chạy trực tiếp trên trình duyệt. Bác sĩ có thể tải ảnh bất kỳ hoặc chọn ca trong bộ dữ liệu, chuyển đổi giữa hai thuật toán bằng một cú nhấp, và nhận về bốn khung so sánh kèm bảng chỉ số. Giao diện dùng light theme, tiếng Việt có dấu đầy đủ."
  );
}

// ---------------------------------------------------------------------------
// 18. Slide 16 — Quy trình lâm sàng & Comparison Quad
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "15  ·  TRỰC QUAN LÂM SÀNG",
    "Quy trình khám và bộ bốn khung nhìn chẩn đoán",
    16,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const quadW = 2.92;
  slide.addImage({
    path: figure("demo_comparison_quad.png"),
    x: L.mx,
    y: 1.36,
    w: quadW,
    h: quadW,
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: L.mx,
    y: 1.36,
    w: quadW,
    h: quadW,
    fill: { color: C.white, transparency: 100 },
    line: { color: C.border, width: 0.75 },
  });
  figureCaption(slide, "Ca minh họa TCGA_DU_6404_19850629_40", L.mx, 4.36, quadW);

  addCard(slide, L.mx, 4.62, quadW, 0.42, { fill: C.accent, line: C.accent });
  addText(slide, "KẾT LUẬN: DƯƠNG TÍNH — PHÁT HIỆN KHỐI U", {
    x: L.mx + 0.1,
    y: 4.62,
    w: quadW - 0.2,
    h: 0.42,
    fontSize: 8,
    fontFace: FONT_STRONG,
    color: C.white,
    align: "center",
    valign: "middle",
  });

  const kpis = [
    { value: "835 px", label: "Diện tích khối u" },
    { value: "8,25%", label: "Tỷ lệ u / diện tích não" },
    { value: "0,689", label: "Độ tròn Circularity" },
    { value: "5,1 ms", label: "Thời gian xử lý" },
  ];
  kpis.forEach((kpi, index) => {
    const x = 3.72 + (index % 2) * 2.66;
    const y = 1.36 + Math.floor(index / 2) * 1.16;
    kpiCard(slide, x, y, 2.5, 1.0, kpi.value, kpi.label, { valueSize: 18 });
  });

  addCard(slide, 3.72, 3.7, 5.16, 0.86, { fill: C.white, shadow: true });
  addText(slide, "Chất lượng phân đoạn so với Ground Truth", {
    x: 3.92,
    y: 3.8,
    w: 4.8,
    h: 0.22,
    fontSize: 9,
    fontFace: FONT_STRONG,
    color: C.dark,
    valign: "middle",
  });
  const runs = [
    { text: "Dice = ", options: { fontSize: 11, color: C.primary } },
    { text: "0,9195", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "    ·    IoU = ", options: { fontSize: 11, color: C.primary } },
    { text: "0,8510", options: { fontSize: 13, bold: true, color: C.primary } },
  ];
  slide.addText(runs, {
    x: 3.92,
    y: 4.06,
    w: 4.8,
    h: 0.34,
    fontFace: FONT,
    margin: 0,
    valign: "middle",
  });

  addCard(slide, 3.72, 4.64, 5.16, 0.46, { fill: C.tint, line: C.border });
  addText(slide, "Bốn khung: ảnh gốc → não tách sọ → mặt nạ u → bounding box và tâm khối u.", {
    x: 3.92,
    y: 4.64,
    w: 4.76,
    h: 0.46,
    fontSize: 8.5,
    color: C.primary,
    valign: "middle",
  });

  addNotes(
    slide,
    "Trí",
    "Đây là màn hình kết quả thực tế của ca minh họa. Bốn khung lần lượt là ảnh gốc, não sau tách sọ, mặt nạ u và ảnh có bounding box. Thẻ KPI tự động cảnh báo dương tính, kèm diện tích 835 pixel, độ tròn 0,689 và thời gian xử lý 5,1 mili-giây. Dice của ca này đạt 0,92 so với ground truth."
  );
}

// ---------------------------------------------------------------------------
// 19. Slide 17 — Kết luận
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "16  ·  KẾT LUẬN",
    "Tổng kết thành tựu sprint 7 ngày",
    17,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const kpis = [
    { value: "0,4446", label: "Dice trung bình — gấp 2,23× đối chứng" },
    { value: "6,13 ms", label: "Độ trễ trung bình mỗi lát cắt" },
    { value: "26 / 26", label: "Unit test PASSED (100%)" },
  ];
  kpis.forEach((kpi, index) => {
    const x = L.mx + index * 3.06;
    kpiCard(slide, x, 1.36, 2.86, 1.0, kpi.value, kpi.label, { valueSize: 24 });
  });

  addCard(slide, L.mx, 2.58, L.cw, 1.98, { fill: C.white, shadow: true });
  addText(slide, "KẾT QUẢ ĐẠT ĐƯỢC", {
    x: L.mx + 0.26,
    y: 2.72,
    w: 3,
    h: 0.22,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });

  const achievements = [
    "Pipeline DIP hoàn chỉnh, xử lý thời gian thực dưới 20 ms/ảnh trên CPU.",
    "Watershed vượt trội Region Growing về Dice, IoU và độ ổn định trên 3.929 lát cắt.",
    "Đặc hiệu trên 99% nhờ tầng tách sọ loại bỏ hoàn toàn tín hiệu ngoài sọ.",
    "Kiến trúc module hóa chuẩn PEP8, 26/26 unit test xanh, Web Demo bàn giao được.",
  ];
  bullets(slide, achievements, { x: L.mx + 0.26, y: 3.02, w: 8.3, h: 1.6, fontSize: 10.5, gap: 9 });

  addText(slide, "Hạn chế: độ chính xác còn thấp ở u nhỏ và u có phù nề lan rộng — đã phân tích ở slide 14.", {
    x: L.mx,
    y: 4.76,
    w: L.cw,
    h: 0.22,
    fontSize: 8.5,
    italic: true,
    color: C.muted,
    valign: "middle",
  });

  addNotes(
    slide,
    "Trường",
    "Sau bảy ngày, nhóm hoàn thành toàn bộ mục tiêu: pipeline chạy dưới 20 mili-giây mỗi lát, 26 trên 26 unit test xanh, và Web Demo bàn giao được. Điểm cần nói thẳng là độ chính xác còn thấp ở u nhỏ và u phù nề, đã phân tích nguyên nhân ở slide trước."
  );
}

// ---------------------------------------------------------------------------
// 20. Slide 18 — Hướng phát triển
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "17  ·  HƯỚNG PHÁT TRIỂN",
    "Ba hướng nâng cấp chiến lược",
    18,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI"
  );

  const futures = [
    {
      tag: "01",
      title: "Tái tạo thể tích 3D",
      body: "Dựng bề mặt khối u từ chuỗi lát cắt MRI đa nhát, hỗ trợ đánh giá thể tích thật (mm³) trước phẫu thuật.",
      tags: ["Marching Cubes", "3D Render"],
    },
    {
      tag: "02",
      title: "Pipeline lai Hybrid",
      body: "Watershed lọc vùng quan tâm ROI, sau đó mạng học sâu nhẹ Mobile-UNet tinh chỉnh biên u.",
      tags: ["Mobile-UNet", "ROI"],
    },
    {
      tag: "03",
      title: "Chuẩn DICOM / PACS",
      body: "Tích hợp trực tiếp chuẩn truyền tải ảnh y tế bệnh viện, đọc metadata và trả kết quả về hệ thống lưu trữ.",
      tags: ["DICOM", "PACS"],
    },
  ];

  futures.forEach((item, index) => {
    const x = L.mx + index * 3.06;
    addCard(slide, x, 1.4, 2.86, 2.56, { fill: C.white, shadow: true });
    addText(slide, item.tag, {
      x: x + 0.22,
      y: 1.54,
      w: 1.2,
      h: 0.4,
      fontSize: 20,
      fontFace: FONT_STRONG,
      color: C.border,
      valign: "middle",
    });
    addText(slide, item.title, {
      x: x + 0.22,
      y: 2.0,
      w: 2.44,
      h: 0.3,
      fontSize: 11.5,
      fontFace: FONT_STRONG,
      color: C.dark,
      valign: "middle",
    });
    addText(slide, item.body, {
      x: x + 0.22,
      y: 2.36,
      w: 2.44,
      h: 0.96,
      fontSize: 8.5,
      color: C.muted,
      lineSpacingMultiple: 1.2,
      valign: "top",
    });
    let tagX = x + 0.22;
    item.tags.forEach((tag) => {
      const tagW = Math.max(0.6, 0.16 + tag.length * 0.072);
      chip(slide, tagX, 3.4, tagW, 0.3, tag, { fill: C.tint, color: C.primary, fontSize: 7.5 });
      tagX += tagW + 0.08;
    });
  });

  addText(slide, "Ưu tiên: mở rộng đánh giá trên tập đa trung tâm (multi-center) trước khi tích hợp bệnh viện.", {
    x: L.mx,
    y: 4.42,
    w: L.cw,
    h: 0.22,
    fontSize: 9,
    italic: true,
    color: C.secondary,
    valign: "middle",
  });

  addNotes(
    slide,
    "Trường và Trí",
    "Nhóm đề xuất ba hướng: tái tạo thể tích 3D để đo thể tích thật, pipeline lai giữa Watershed và mạng học sâu nhẹ, và tích hợp chuẩn DICOM/PACS để đưa vào bệnh viện. Trước khi tích hợp thực tế, cần đánh giá trên dữ liệu đa trung tâm."
  );
}

// ---------------------------------------------------------------------------
// 21. Slide 19 — Phụ lục kỹ thuật
// ---------------------------------------------------------------------------
{
  const slide = contentSlide(
    "18  ·  PHỤ LỤC KỸ THUẬT",
    "Phụ lục Kỹ thuật: Cấu trúc Module & Kiểm thử Đơn vị (Unit Tests)",
    19,
    "Xử lý ảnh số  ·  Phân đoạn khối u não MRI",
    { titleSize: 19.5, titleY: 0.56, titleH: 0.72 }
  );

  addCard(slide, L.mx, 1.36, 4.62, 3.62, { fill: C.white, shadow: true });
  addText(slide, "SƠ ĐỒ MODULE", {
    x: L.mx + 0.22,
    y: 1.48,
    w: 3,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });

  const tree = [
    ["src/", true, 0],
    ["pipeline.py", false, 1],
    ["preprocessing/", true, 1],
    ["filters.py", false, 2],
    ["skull_strip.py", false, 2],
    ["segmentation/", true, 1],
    ["watershed.py", false, 2],
    ["region_growing.py", false, 2],
    ["base.py", false, 2],
    ["measurement/", true, 1],
    ["features.py", false, 2],
    ["visualization.py", false, 2],
    ["evaluation/", true, 1],
    ["metrics.py", false, 2],
    ["benchmark.py", false, 2],
  ];
  const treeRuns = tree.map(([name, isFolder, level], index) => ({
    text: `${"    ".repeat(level)}${name}`,
    options: {
      bold: isFolder,
      color: isFolder ? C.primary : C.ink,
      breakLine: index < tree.length - 1,
      paraSpaceAfter: 1,
    },
  }));
  slide.addText(treeRuns, {
    x: L.mx + 0.26,
    y: 1.74,
    w: 4.1,
    h: 3.1,
    fontFace: FONT_MONO,
    fontSize: 9.5,
    lineSpacingMultiple: 1.18,
    margin: 0,
    valign: "top",
  });

  addCard(slide, 5.4, 1.36, 4.05, 3.62, { fill: C.white, shadow: true });
  addText(slide, "KIỂM THỬ ĐƠN VỊ", {
    x: 5.6,
    y: 1.48,
    w: 3,
    h: 0.2,
    fontSize: 8.5,
    fontFace: FONT_STRONG,
    color: C.secondary,
    charSpacing: 1.2,
    valign: "middle",
  });
  addText(slide, "26/26", {
    x: 5.6,
    y: 1.72,
    w: 1.85,
    h: 0.52,
    fontSize: 30,
    fontFace: FONT_STRONG,
    color: C.accent,
    valign: "middle",
  });
  addText(slide, "test cases PASSED", {
    x: 7.5,
    y: 1.76,
    w: 1.8,
    h: 0.24,
    fontSize: 9,
    color: C.muted,
    valign: "middle",
  });
  addText(slide, "Không hồi quy · Bảo toàn 7 bất biến dữ liệu I1–I7", {
    x: 7.5,
    y: 2.0,
    w: 1.8,
    h: 0.3,
    fontSize: 8,
    color: C.muted,
    lineSpacingMultiple: 1.1,
    valign: "top",
  });

  const suites = [
    ["metrics", 7],
    ["segmentation", 6],
    ["pipeline", 6],
    ["preprocessing", 4],
    ["measurement", 3],
  ];
  suites.forEach(([name, count], index) => {
    const y = 2.44 + index * 0.46;
    addText(slide, name, {
      x: 5.6,
      y,
      w: 1.35,
      h: 0.22,
      fontSize: 8.5,
      color: C.ink,
      valign: "middle",
    });
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 6.95,
      y: y + 0.04,
      w: 1.6,
      h: 0.16,
      rectRadius: 0.03,
      fill: { color: C.cardAlt },
      line: { color: C.cardAlt, width: 0.5 },
    });
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 6.95,
      y: y + 0.04,
      w: 1.6 * (count / 7),
      h: 0.16,
      rectRadius: 0.03,
      fill: { color: index === 0 ? C.primary : C.secondary },
      line: { color: index === 0 ? C.primary : C.secondary, width: 0.5 },
    });
    addText(slide, `${count}`, {
      x: 8.65,
      y,
      w: 0.55,
      h: 0.22,
      fontSize: 8.5,
      fontFace: FONT_STRONG,
      color: C.primary,
      align: "right",
      valign: "middle",
    });
  });

  addText(slide, "Bộ kiểm thử đơn vị: tests/  ·  pytest -v  ·  Bảo toàn 7 bất biến dữ liệu I1–I7", {
    x: L.mx,
    y: 4.98,
    w: L.cw,
    h: 0.22,
    fontSize: 8.5,
    italic: true,
    color: C.muted,
    valign: "middle",
  });

  addNotes(
    slide,
    "Trường",
    "Về mặt kỹ thuật, mã nguồn chia thành bốn package tương ứng bốn tầng xử lý. Toàn bộ 26 unit test đều đạt, không có hồi quy, và bảy bất biến dữ liệu I1 đến I7 trong đặc tả vẫn được bảo toàn sau mọi thay đổi."
  );
}

// ---------------------------------------------------------------------------
// 22. Slide 20 — Lời cảm ơn & Q&A
// ---------------------------------------------------------------------------
{
  const slide = pptx.addSlide();
  slide.background = { color: C.primaryDeep };

  addText(slide, "LỜI CẢM ƠN & THẢO LUẬN", {
    x: L.mx,
    y: 1.0,
    w: L.cw,
    h: 0.24,
    fontSize: 9,
    fontFace: FONT_STRONG,
    color: "9FE8DC",
    charSpacing: 2,
    align: "center",
    valign: "middle",
  });

  addText(slide, "TRÂN TRỌNG CẢM ƠN THẦY THS. ĐỖ TRUNG DŨNG VÀ CÁC BẠN SINH VIÊN!", {
    x: 0.7,
    y: 1.34,
    w: 8.6,
    h: 1.0,
    fontSize: 25,
    fontFace: FONT_STRONG,
    color: C.white,
    align: "center",
    lineSpacingMultiple: 1.12,
    valign: "middle",
  });

  addText(
    slide,
    "Buổi báo cáo kết thúc môn học Xử lý ảnh số — Ngành Khoa học Dữ liệu — Bộ môn Xử lý ảnh số — Khoa CNTT, HUIT",
    {
      x: 1.2,
      y: 2.4,
      w: 7.6,
      h: 0.44,
      fontSize: 10.5,
      color: "CBE8EF",
      align: "center",
      lineSpacingMultiple: 1.2,
      valign: "middle",
    }
  );

  addCard(slide, 2.35, 3.0, 5.3, 0.6, { fill: C.secondary, line: C.secondary });
  addText(slide, "SẴN SÀNG TRAO ĐỔI VÀ TRẢ LỜI CÂU HỎI PHẢN BIỆN", {
    x: 2.5,
    y: 3.0,
    w: 5.0,
    h: 0.6,
    fontSize: 9.5,
    fontFace: FONT_STRONG,
    color: C.white,
    align: "center",
    valign: "middle",
  });

  const contacts = [
    { name: "Hà Mạnh Trường", mssv: "2045240326", role: "Nhóm trưởng" },
    { name: "Huỳnh Tâm Trí", mssv: "2045240315", role: "Thành viên" },
  ];
  contacts.forEach((person, index) => {
    const x = 2.35 + index * 2.75;
    addCard(slide, x, 3.82, 2.55, 0.92, { fill: "0B4A6B", line: "1C6A8C" });
    addText(slide, person.name, {
      x: x + 0.2,
      y: 3.94,
      w: 2.15,
      h: 0.24,
      fontSize: 11,
      fontFace: FONT_STRONG,
      color: C.white,
      align: "center",
      valign: "middle",
    });
    addText(slide, `${person.mssv}  ·  ${person.role}`, {
      x: x + 0.2,
      y: 4.2,
      w: 2.15,
      h: 0.2,
      fontSize: 8.5,
      color: "CBE8EF",
      align: "center",
      valign: "middle",
    });
    addText(slide, "Khoa CNTT — HUIT", {
      x: x + 0.2,
      y: 4.4,
      w: 2.15,
      h: 0.2,
      fontSize: 8,
      color: "8FC5D4",
      align: "center",
      valign: "middle",
    });
  });

  addText(slide, "TP. Hồ Chí Minh, Năm 2026", {
    x: L.mx,
    y: 4.98,
    w: L.cw,
    h: 0.22,
    fontSize: 9,
    color: "8FC5D4",
    align: "center",
    valign: "middle",
  });

  addNotes(
    slide,
    "Cả hai",
    "Thay mặt nhóm, em xin trân trọng cảm ơn Thầy ThS. Đỗ Hùng Dũng và các bạn sinh viên đã lắng nghe phần trình bày. Nhóm sẵn sàng trao đổi và trả lời các câu hỏi phản biện. Trường phụ trách phần quy trình xử lý và thuật toán, Trí phụ trách dữ liệu, đánh giá định lượng và demo."
  );
}

// ---------------------------------------------------------------------------
// 23. Xuất tệp
// ---------------------------------------------------------------------------
pptx.writeFile({ fileName: OUT_FILE }).then((file) => {
  const count = pptx.slides.length;
  console.log(`Đã sinh ${count} slide: ${file}`);
  if (count !== 20) {
    console.error(`Cảnh báo: số slide là ${count}, yêu cầu 20.`);
    process.exitCode = 1;
  }
});
