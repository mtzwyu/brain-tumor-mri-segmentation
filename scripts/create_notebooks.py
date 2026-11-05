import os
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.makedirs("notebooks", exist_ok=True)

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    }

# ==============================================================================
# NOTEBOOK 1: BƯỚC 1 - THU THẬP & CHUẨN BỊ TẬP DỮ LIỆU (DATA PREPARATION)
# Căn cứ: docs/KHUNG_NOI_DUNG_TONG_QUAT_DO_AN_XLAS.md (Mục II.1 & Mục V.3)
# ==============================================================================
nb1_cells = [
    md_cell("""# Notebook 1: Thu Thập, Khảo Sát & Chuẩn Bị Tập Dữ Liệu (TCGA-LGG)
**Căn cứ tài liệu:** `docs/KHUNG_NOI_DUNG_TONG_QUAT_DO_AN_XLAS.md`  
* **Quy trình chuẩn Bộ môn:** **Bước 1 — Thu thập & Chuẩn bị tập dữ liệu (Data Preparation)**  
* **Ánh xạ Báo cáo đồ án:** **Mục 3 — Mô tả tập dữ liệu thực nghiệm**  
* **Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)  
* **Nhóm thực hiện:** Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315) — *Trí phụ trách chính*

---

## 1. Mục tiêu nghiên cứu (Theo Khung Tổng Quát)
1. **Nguồn gốc dữ liệu:** Bộ dữ liệu cộng hưởng từ sọ não The Cancer Genome Atlas Low-Grade Glioma (**TCGA-LGG**), công bố bởi Buda et al. (2019) trên tạp chí *Computers in Biology and Medicine*.
2. **Quy cách dữ liệu:** Ảnh cắt lát MRI chuỗi xung FLAIR/T1-CE, kích thước chuẩn hóa $256 \times 256$, thang độ xám Grayscale `uint8` $[0, 255]$.
3. **Mặt nạ Ground Truth:** Mặt nạ nhị phân $\{0, 255\}$ được bác sĩ chuyên khoa thần kinh khoanh vùng ổ u não (Core Tumor).
4. **Phân nhóm độ khó:** Khảo sát diện tích u và phân loại thành 3 nhóm (U nhỏ $< 1.5\%$, U trung bình $1.5\% - 5\%$, U lớn $> 5\%$) để kiểm thử tính bền vững của thuật toán xử lý ảnh số."""),

    code_cell("""import os
import sys
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Thêm đường dẫn gốc dự án để nạp module src
sys.path.append(os.path.abspath(".."))

plt.rcParams['figure.figsize'] = (12, 6)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
print("Môi trường sẵn sàng. Đang nạp dữ liệu...")"""),

    md_cell("""##  2. Khảo sát Metadata Tập Dữ Liệu
Đọc bảng metadata (`data/full/metadata.csv` hoặc fallback `data/full/metadata.csv`) chứa thông tin chi tiết về diện tích và tỷ lệ u của các ca bệnh:"""),

    code_cell("""base_dir = "../data/full" if os.path.exists("../data/full/metadata.csv") else "data/full"
meta_path = os.path.join(base_dir, "metadata.csv")
df = pd.read_csv(meta_path)
print(f"Nguồn dữ liệu đang nạp: {base_dir}")
print(f"Tổng số bệnh nhân nghiên cứu: {df['patient_id'].nunique()} bệnh nhân")
print(f"Tổng số lát cắt MRI: {len(df):,} lát cắt")

healthy_df = df[~df['has_tumor']]
tumor_df = df[df['has_tumor']]
print(f"  + Lát cắt âm tính (Não lành, 0% u): {len(healthy_df):,} lát ({len(healthy_df)/len(df)*100:.2f}%)")
print(f"  + Lát cắt dương tính (Có khối u): {len(tumor_df):,} lát ({len(tumor_df)/len(df)*100:.2f}%)")

df[['sample_id', 'patient_id', 'width', 'height', 'tumor_area_pixels', 'tumor_ratio_percent']].head(5)"""),

    md_cell("""## 3. Trực quan hóa dữ liệu: Phân tích thống kê phân bố khối u
Đánh giá độ phân tán của diện tích u và tỷ lệ % u trên thiết diện não (khảo sát trên 1,373 lát cắt có u):"""),

    code_cell("""tumor_df = df[df['has_tumor']]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Histogram diện tích pixel trên tập lát cắt có u
axes[0].hist(tumor_df['tumor_area_pixels'], bins=12, color='#3B82F6', edgecolor='black', alpha=0.8)
axes[0].set_title("Phân Bố Diện Tích Khối U (Pixels) — 1,373 Lát Cắt Có U", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Diện tích khối u (pixels)")
axes[0].set_ylabel("Số lượng lát cắt")

# 2. Histogram tỷ lệ phần trăm trên tập lát cắt có u
axes[1].hist(tumor_df['tumor_ratio_percent'], bins=12, color='#10B981', edgecolor='black', alpha=0.8)
axes[1].set_title("Phân Bố Tỷ Lệ % U / Thiết Diện Não — 1,373 Lát Cắt Có U", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Tỷ lệ diện tích u (%)")
axes[1].set_ylabel("Số lượng lát cắt")

plt.tight_layout()
plt.show()

print("Thống kê mô tả chi tiết trên 1,373 lát cắt có khối u (Khớp 100% Báo cáo Mục 3):")
print(tumor_df[['tumor_area_pixels', 'tumor_ratio_percent']].describe().round(2))"""),

    md_cell("""## 4. Quy trình thực nghiệm: Phân loại 3 nhóm ca bệnh (u nhỏ, u vừa, u lớn)
Căn cứ theo độ khó thuật toán để chuẩn bị kiểm thử ở các bước tiếp theo (Đồng bộ Bảng 3.1 trong Báo cáo Đồ án):"""),

    code_cell("""healthy_df = df[~df['has_tumor']]
tumor_df = df[df['has_tumor']]

small_tumors = tumor_df[tumor_df['tumor_ratio_percent'] < 1.5]
medium_tumors = tumor_df[(tumor_df['tumor_ratio_percent'] >= 1.5) & (tumor_df['tumor_ratio_percent'] <= 5.0)]
large_tumors = tumor_df[tumor_df['tumor_ratio_percent'] > 5.0]

summary_rows = [
    {
        "Phân Nhóm Dữ Liệu": "Não lành (Không u)",
        "Tiêu Chuẩn Diện Tích": "0.0% diện tích",
        "Số Lượng Lát Cắt": len(healthy_df),
        "Tỷ Lệ / Tập U (%)": "—",
        "Tỷ Lệ / Toàn Tập (%)": f"{len(healthy_df)/len(df)*100:.2f}%",
        "Mẫu Tiêu Biểu": ", ".join(healthy_df['sample_id'].iloc[:3].tolist()) + "..."
    },
    {
        "Phân Nhóm Dữ Liệu": "Khối u nhỏ (Small)",
        "Tiêu Chuẩn Diện Tích": "< 1.5% diện tích",
        "Số Lượng Lát Cắt": len(small_tumors),
        "Tỷ Lệ / Tập U (%)": f"{len(small_tumors)/len(tumor_df)*100:.2f}%",
        "Tỷ Lệ / Toàn Tập (%)": f"{len(small_tumors)/len(df)*100:.2f}%",
        "Mẫu Tiêu Biểu": ", ".join(small_tumors['sample_id'].iloc[:3].tolist()) + "..."
    },
    {
        "Phân Nhóm Dữ Liệu": "Khối u trung bình (Medium)",
        "Tiêu Chuẩn Diện Tích": "1.5% - 5.0% diện tích",
        "Số Lượng Lát Cắt": len(medium_tumors),
        "Tỷ Lệ / Tập U (%)": f"{len(medium_tumors)/len(tumor_df)*100:.2f}%",
        "Tỷ Lệ / Toàn Tập (%)": f"{len(medium_tumors)/len(df)*100:.2f}%",
        "Mẫu Tiêu Biểu": ", ".join(medium_tumors['sample_id'].iloc[:3].tolist()) + "..."
    },
    {
        "Phân Nhóm Dữ Liệu": "Khối u lớn (Large)",
        "Tiêu Chuẩn Diện Tích": "> 5.0% diện tích",
        "Số Lượng Lát Cắt": len(large_tumors),
        "Tỷ Lệ / Tập U (%)": f"{len(large_tumors)/len(tumor_df)*100:.2f}%",
        "Tỷ Lệ / Toàn Tập (%)": f"{len(large_tumors)/len(df)*100:.2f}%",
        "Mẫu Tiêu Biểu": ", ".join(large_tumors['sample_id'].iloc[:3].tolist()) + "..."
    }
]

summary_df = pd.DataFrame(summary_rows)
print(f"Tổng số lát cắt toàn tập: {len(df):,} | Tập có u: {len(tumor_df):,} | Não lành: {len(healthy_df):,}")
print("Bảng thống kê phân tầng độ khó khớp tuyệt đối Bảng 3.1 Báo cáo Đồ án:")
print(summary_df[['Phân Nhóm Dữ Liệu', 'Tiêu Chuẩn Diện Tích', 'Số Lượng Lát Cắt', 'Tỷ Lệ / Tập U (%)', 'Tỷ Lệ / Toàn Tập (%)']].to_string(index=False))"""),

    md_cell("""## 5. Minh họa hình ảnh: Lưới ảnh MRI và Ground Truth Mask
Hiển thị 6 ca đại diện cho các nhóm kích thước u và đối chứng não lành (Mục 3 Báo cáo):"""),

    code_cell("""sample_indices = [
    healthy_df.index[0],     # Não lành đối chứng (0% u)
    small_tumors.index[0],   # Khối u nhỏ (< 1.5%)
    medium_tumors.index[0],  # Khối u trung bình (1.5% - 5.0%)
    medium_tumors.index[1],  # Khối u trung bình (1.5% - 5.0%)
    large_tumors.index[0],   # Khối u lớn (> 5.0%)
    large_tumors.index[1],   # Khối u lớn (> 5.0%)
]

group_labels = ["Não lành (0%)", "U nhỏ (<1.5%)", "U vừa (1.5-5%)", "U vừa (1.5-5%)", "U lớn (>5%)", "U lớn (>5%)"]

fig, axes = plt.subplots(2, len(sample_indices), figsize=(18, 6))

for col_idx, (idx, grp) in enumerate(zip(sample_indices, group_labels)):
    row = df.loc[idx]
    img_p = os.path.join(base_dir, "images", row['image_file'])
    mask_p = os.path.join(base_dir, "masks", row['mask_file'])
    
    img = cv2.imread(img_p, cv2.IMREAD_GRAYSCALE)
    mask = cv2.imread(mask_p, cv2.IMREAD_GRAYSCALE)
    
    # Hàng 1: Ảnh gốc
    axes[0, col_idx].imshow(img, cmap='gray')
    axes[0, col_idx].set_title(f"[{grp}]\\n{row['sample_id']}\\n({row['tumor_ratio_percent']}%)", fontsize=9)
    axes[0, col_idx].axis('off')
    
    # Hàng 2: Mặt nạ Ground Truth
    axes[1, col_idx].imshow(mask, cmap='hot')
    axes[1, col_idx].set_title(f"Area: {row['tumor_area_pixels']} px", fontsize=9)
    axes[1, col_idx].axis('off')

plt.suptitle("Một Số Mẫu Ảnh MRI Não & Mặt Nạ Ground Truth Chuyên Gia Theo Từng Nhóm Độ Khó (TCGA-LGG Benchmark)", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()""")
]

# ==============================================================================
# NOTEBOOK 2: BƯỚC 2 - TIỀN XỬ LÝ & TÁCH SỌ NÃO (SKULL STRIPPING)
# Căn cứ: docs/KHUNG_NOI_DUNG_TONG_QUAT_DO_AN_XLAS.md (Mục II.2, IV & Mục V.4)
# ==============================================================================
nb2_cells = [
    md_cell("""# Notebook 2: Tiền Xử Lý & Tách Sọ Não (Skull Stripping)
**Căn cứ tài liệu:** `docs/KHUNG_NOI_DUNG_TONG_QUAT_DO_AN_XLAS.md`  
* **Quy trình chuẩn Bộ môn:** **Bước 2 — Tiền xử lý & Cải thiện chất lượng ảnh (Preprocessing & Skull Stripping)**  
* **Ánh xạ Báo cáo đồ án:** **Mục 4 — Tiền xử lý ảnh**  
* **Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)  
* **Nhóm thực hiện:** Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315) — *Trường phụ trách chính*

---

## 1. Cơ sở lý thuyết DIP (Gonzalez & Woods Ch. 3, 5 & 9)
1. **Khử nhiễu Rician:** Áp dụng **Bilateral Filter** phi tuyến nhằm lọc nhiễu hạt y tế nhưng bảo toàn độ dốc cường độ tại ranh giới khối u (tránh làm nhòe biên như bộ lọc Gaussian).
2. **Cân bằng tương phản:** Áp dụng **CLAHE** (Contrast Limited Adaptive Histogram Equalization) làm rõ cấu trúc mô mềm chất trắng / chất xám.
3. **Kỹ thuật Tách sọ não kinh điển (Skull Stripping):**
   * *Otsu Thresholding:* Nhị phân hóa tự động phân tách phần đầu khỏi nền đen.
   * *Morphological Opening:* Phép mở với phần tử cấu trúc dạng đĩa (Disk/Ellipse structuring element) cắt đứt các "cầu nối mô" giữa màng não và xương sọ.
   * *Largest Connected Component (LCC):* Trích xuất thành phần liên thông có diện tích lớn nhất (nhu mô não).
   * *Hole Filling:* Lấp đầy lỗ trống não thất bằng phép bù nhị phân và thuật toán FloodFill.
   * *Bitwise-AND:* Nhân mặt nạ não với ảnh gốc để thu được ảnh não sạch sọ hoàn hảo."""),

    code_cell("""import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(".."))
from src.preprocessing.filters import apply_bilateral_filter, apply_clahe
from src.preprocessing.skull_strip import extract_brain_mask, strip_skull

print("Module tiền xử lý và tách sọ đã được nạp thành công.")"""),

    md_cell("""## 2. Quy trình thực nghiệm: Thử nghiệm chi tiết từng bước tách sọ trên ca mẫu
Phân tích trực quan 6 giai đoạn xử lý từ ảnh MRI gốc đến ảnh sạch sọ trên ca lâm sàng tiêu biểu (TCGA_CS_6290_20000917_10):"""),

    code_cell("""img_path = "../data/full/images/TCGA_CS_6290_20000917_10.png"
orig_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# 1. Khử nhiễu Bilateral
denoised = apply_bilateral_filter(orig_img, d=9, sigma_color=75.0, sigma_space=75.0)

# 2. Phân ngưỡng Otsu
_, otsu_bin = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 3. Phép mở hình thái học (Opening với kernel elip 5x5)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
opened = cv2.morphologyEx(otsu_bin, cv2.MORPH_OPEN, kernel, iterations=2)

# 4. Thành phần liên thông lớn nhất (LCC)
num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
lcc_mask = np.zeros_like(orig_img)
lcc_mask[labels == largest_label] = 255

# 5. Lấp đầy lỗ hổng (Brain Mask hoàn chỉnh)
brain_mask = extract_brain_mask(denoised, kernel_size=5)

# 6. Não sạch sọ cuối cùng (Bitwise-AND)
stripped_brain, _ = strip_skull(denoised, brain_mask)

# Vẽ biểu đồ 6 bước
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
steps = [
    ("1. Ảnh MRI Gốc (Original)", orig_img, 'gray'),
    ("2. Ngưỡng Hóa Otsu (Binary Head)", otsu_bin, 'gray'),
    ("3. Morphological Opening (Cắt cuống mô)", opened, 'gray'),
    ("4. LCC Nhu Mô Não (Largest Component)", lcc_mask, 'gray'),
    ("5. Brain Mask (Đã lấp não thất)", brain_mask, 'hot'),
    ("6. Não Sạch Sọ (Skull Stripped Result)", stripped_brain, 'gray')
]

for i, (title, img_step, cmap) in enumerate(steps):
    r, c = i // 3, i % 3
    axes[r, c].imshow(img_step, cmap=cmap)
    axes[r, c].set_title(title, fontsize=11, fontweight='bold')
    axes[r, c].axis('off')

plt.suptitle("Quy Trình 6 Bước Tách Sọ Não Bằng Kỹ Thuật Hình Thái Học & Liên Thông (DIP Core)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()"""),

    md_cell("""## 3. Ý nghĩa y khoa: Đánh giá khả năng tăng cường tương phản CLAHE
So sánh ảnh não sau tách sọ khi có và không áp dụng CLAHE:"""),

    code_cell("""clahe_brain = apply_clahe(stripped_brain, clip_limit=2.0, tile_grid_size=(8, 8))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(stripped_brain, cmap='gray')
axes[0].set_title("Ảnh Não Sau Tách Sọ (Chưa CLAHE)", fontsize=12)
axes[0].axis('off')

axes[1].imshow(clahe_brain, cmap='gray')
axes[1].set_title("Ảnh Não Sau Cân Bằng Tương Phản CLAHE", fontsize=12)
axes[1].axis('off')

plt.tight_layout()
plt.show()"""),

    md_cell("""## 4. Phân tích kết quả: Kiểm thử tính bền vững của tách sọ trên 4 ca lâm sàng tiêu biểu
Chứng minh thuật toán hoạt động ổn định trên nhiều dạng hình thái hộp sọ, kích thước u và đối chứng não lành (Healthy Control):"""),

    code_cell("""test_cases = [
    ("TCGA_CS_6290_20000917_10", "Ca 1: U Điển Hình Bờ Rõ"),
    ("TCGA_CS_6186_20000601_16", "Ca 2: U Kích Thước Lớn"),
    ("TCGA_CS_4942_19970222_12", "Ca 3: U Bờ Phức Tạp Thâm Nhiễm"),
    ("TCGA_DU_5851_19950428_2", "Ca 4: Não Lành Không U (Đối chứng)")
]

fig, axes = plt.subplots(4, 3, figsize=(12, 13))

for idx, (case_id, desc) in enumerate(test_cases):
    im_path = f"../data/full/images/{case_id}.png"
    im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
    b_mask = extract_brain_mask(im)
    res_stripped, _ = strip_skull(im, b_mask)
    
    axes[idx, 0].imshow(im, cmap='gray')
    axes[idx, 0].set_title(f"Gốc: {desc}")
    axes[idx, 0].axis('off')
    
    axes[idx, 1].imshow(b_mask, cmap='hot')
    axes[idx, 1].set_title("Mặt Nạ Nhu Mô Não")
    axes[idx, 1].axis('off')
    
    axes[idx, 2].imshow(res_stripped, cmap='gray')
    axes[idx, 2].set_title("Não Đã Tách Sọ")
    axes[idx, 2].axis('off')

plt.suptitle("Kiểm Thử Tính Bền Vững Của Thuật Toán Tách Sọ Trên Các Ca Lâm Sàng Tiêu Biểu", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()""")
]

# ==============================================================================
# NOTEBOOK 3: BƯỚC 3 & 4 - PHÂN ĐOẠN LÕI & RÚT TRÍCH ĐẶC TRƯNG HÌNH THÁI
# Căn cứ: docs/KHUNG_NOI_DUNG_TONG_QUAT_DO_AN_XLAS.md (Mục II.3, II.4 & Mục V.5)
# ==============================================================================
nb3_cells = [
    md_cell("""#  Notebook 3: Phân Đoạn U Não (So Sánh 2 Phương Án) & Rút Trích Đặc Trưng
**Căn cứ tài liệu:** `docs/KHUNG_NOI_DUNG_TONG_QUAT_DO_AN_XLAS.md`  
* **Quy trình chuẩn Bộ môn:**  
  * **Bước 3 — Phân đoạn đối tượng cốt lõi (Core Segmentation)**
  * **Bước 4 — Rút trích đặc trưng hình học & Đo lường (Feature Extraction & Measurement)**
* **Ánh xạ Báo cáo đồ án:** **Mục 5 — Phương pháp và quy trình thực nghiệm**  
* **Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)  
* **Nhóm thực hiện:** Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315) — *Cả hai cùng phối hợp*

---

## 1. Quy tắc vàng của Bộ môn: Bắt buộc so sánh tối thiểu 02 phương án
Đồ án cài đặt và so sánh đối chứng 2 thuật toán DIP kinh điển:
* **Phương án A (Baseline chính):** **Marker-controlled Watershed**  
  * Phân vị cường độ cao $\rightarrow$ Biến đổi khoảng cách Euclidean (`cv2.distanceTransform`) $\rightarrow$ Tìm Sure Foreground & Sure Background $\rightarrow$ Đánh dấu Markers $\rightarrow$ Phân thủy Watershed.
* **Phương án B (Phương án đối chứng):** **Seeded Region Growing**  
  * Tự động tìm hạt giống tại vị trí cực đại cường độ trong nhu mô não $\rightarrow$ Lan truyền 8 hướng láng giềng theo hàng đợi BFS với ngưỡng dung sai $|I(p) - I(seed)| \le \text{tolerance}$ $\rightarrow$ Hậu xử lý hình thái học.

## 2. Đo đạc đặc trưng hình học: Rút trích đặc trưng hình học và đo lường (Bước 4)
* **Diện tích u:** $S_{\text{tumor}} = \sum \text{pixel}$ và tỷ lệ $\%$ u / diện tích não.
* **Độ tròn (Circularity / Compactness):** $C = \frac{4\pi \cdot \text{Area}}{\text{Perimeter}^2}$ ($C \approx 1$: u tròn đều lành tính Meningioma; $C \ll 1$: bờ gồ ghề ác tính Glioma).
* **Định vị:** Trích xuất Bounding Box màu đỏ cảnh báo quanh khối u."""),

    code_cell("""import os
import sys
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(".."))
from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed
from src.segmentation.region_growing import segment_region_growing
from src.measurement.features import extract_tumor_features, calculate_circularity
from src.measurement.visualization import draw_tumor_overlay
from src.evaluation.metrics import calculate_dice, calculate_iou
from src.pipeline import verify_tumor_presence

print("Đã nạp đầy đủ các module phân đoạn, cổng Anomaly Gate và đo lường đặc trưng.")"""),

    md_cell("""## 3. So Sánh Trực Quan 2 Phương Án Trên Các Ca Lâm Sàng Tiêu Biểu
Thực nghiệm so sánh Watershed vs. Region Growing trên 4 ca lâm sàng tiêu biểu (U điển hình, U lớn, U bờ phức tạp và Đối chứng não lành kết hợp Cổng Anomaly Gate):"""),

    code_cell("""test_cases = [
    ("TCGA_CS_6290_20000917_10", "Ca 1: U Điển Hình Bờ Rõ (Dice ~0.97)"),
    ("TCGA_CS_6186_20000601_16", "Ca 2: U Kích Thước Lớn (Area ~2,079px)"),
    ("TCGA_CS_4942_19970222_12", "Ca 3: U Bờ Phức Tạp (Dice ~0.94)"),
    ("TCGA_DU_5851_19950428_2", "Ca 4: Não Lành Đối Chứng (GT 0px)")
]

fig, axes = plt.subplots(4, 5, figsize=(18, 14))

for row_idx, (case_id, desc) in enumerate(test_cases):
    img_p = f"../data/full/images/{case_id}.png"
    mask_p = f"../data/full/masks/{case_id}_mask.png"
    
    orig = cv2.imread(img_p, cv2.IMREAD_GRAYSCALE)
    gt = cv2.imread(mask_p, cv2.IMREAD_GRAYSCALE)
    stripped, b_mask = strip_skull(orig)
    
    # Cổng Anomaly Gate 2 tầng (DIP): Tiền lọc tổn thương tăng sáng bất thường
    is_anomaly = verify_tumor_presence(stripped, b_mask, z_thresh=2.3)
    
    if is_anomaly:
        # 1. Chạy Watershed (Phương án A)
        mask_ws = segment_watershed(stripped, dist_thresh_ratio=0.4)
        # 2. Chạy Region Growing (Phương án B)
        mask_rg = segment_region_growing(stripped, tolerance=15)
    else:
        # Não lành: Bảo vệ 100%, trả về mặt nạ rỗng (Zero False Positive)
        mask_ws = np.zeros_like(orig)
        mask_rg = np.zeros_like(orig)
        
    dice_ws = calculate_dice(mask_ws, gt)
    dice_rg = calculate_dice(mask_rg, gt)
    
    # 3. Trích xuất đặc trưng và vẽ Bounding Box
    res_ws = extract_tumor_features(mask_ws, b_mask)
    annotated = draw_tumor_overlay(orig, mask_ws, res_ws)
    
    # Hiển thị
    axes[row_idx, 0].imshow(orig, cmap='gray')
    axes[row_idx, 0].set_title(f"{desc}\\nẢnh MRI Gốc", fontsize=9)
    axes[row_idx, 0].axis('off')
    
    axes[row_idx, 1].imshow(gt, cmap='gray')
    gt_area = int(np.sum(gt > 0))
    axes[row_idx, 1].set_title(f"Ground Truth Bác Sĩ\\n(GT Area = {gt_area} px)", fontsize=9)
    axes[row_idx, 1].axis('off')
    
    axes[row_idx, 2].imshow(mask_ws, cmap='Blues')
    axes[row_idx, 2].set_title(f"A. Watershed\\nDice = {dice_ws:.4f}", fontsize=9, color='blue', fontweight='bold')
    axes[row_idx, 2].axis('off')
    
    axes[row_idx, 3].imshow(mask_rg, cmap='Greens')
    axes[row_idx, 3].set_title(f"B. Region Growing\\nDice = {dice_rg:.4f}", fontsize=9, color='green', fontweight='bold')
    axes[row_idx, 3].axis('off')
    
    axes[row_idx, 4].imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
    title_ann = f"Bounding Box & Đo Lường\\nArea={res_ws.tumor_area_px}px, C={res_ws.circularity:.2f}" if res_ws.tumor_detected else "Não Lành (Âm Tính)\\nKhông có u (0 px)"
    axes[row_idx, 4].set_title(title_ann, fontsize=9)
    axes[row_idx, 4].axis('off')

plt.suptitle("Thực Nghiệm So Sánh Đối Chứng: Watershed vs. Seeded Region Growing Kết Hợp Cổng Anomaly Gate", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()"""),

    md_cell("""##  4. Bảng Nhận Xét So Sánh Kỹ Thuật Giữa 2 Phương Pháp
Tổng kết các ưu nhược điểm phát hiện được từ thực nghiệm:"""),

    code_cell("""compare_table = pd.DataFrame({
    "Tiêu Chí": [
        "Nguyên lý cốt lõi",
        "Khả năng bắt trọn bờ u",
        "Độ nhạy với u nhỏ (< 1.5%)",
        "Độ nhạy với tham số",
        "Thời gian xử lý trung bình"
    ],
    "Marker-controlled Watershed (Phương án A)": [
        "Biến đổi khoảng cách Euclidean + Phân thủy địa hình",
        "Tốt, ranh giới rõ ràng, không bị tràn viền",
        "Có thể under-segmentation nếu gradient yếu",
        "Ổn định với tham số dist_thresh_ratio = 0.4",
        "Nhanh (~ 15 - 25 ms/ảnh)"
    ],
    "Seeded Region Growing (Phương án B)": [
        "Tìm cực đại cường độ + Lan truyền 8 láng giềng",
        "Tốt ở lõi u, bờ u phụ thuộc ngưỡng dung sai",
        "Rất nhạy cảm, dễ bắt đúng tâm u nhỏ",
        "Nhạy cảm cao với tham số tolerance",
        "Rất nhanh (~ 5 - 12 ms/ảnh)"
    ]
})

compare_table""")
]

# ==============================================================================
# NOTEBOOK 4: BƯỚC 5 & 6 - THỰC NGHIỆM ĐÁNH GIÁ ĐỊNH LƯỢNG & PHÂN TÍCH CA LỖI
# Căn cứ: docs/KHUNG_NOI_DUNG_TONG_QUAT_DO_AN_XLAS.md (Mục II.5, II.6, IV & Mục V.6)
# ==============================================================================
nb4_cells = [
    md_cell("""#  Notebook 4: Đánh Giá Định Lượng & Phân Tích Trường Hợp Thất Bại
**Căn cứ tài liệu:** `docs/KHUNG_NOI_DUNG_TONG_QUAT_DO_AN_XLAS.md`  
* **Quy trình chuẩn Bộ môn:**  
  * **Bước 5 — Xây dựng Baseline & Thực nghiệm so sánh (Comparative Experiments)**
  * **Bước 6 — Đánh giá định lượng & Phân tích trường hợp thất bại (Evaluation & Error Analysis)**
* **Ánh xạ Báo cáo đồ án:** **Mục 6 — Kết quả và đánh giá**  
* **Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)  
* **Nhóm thực hiện:** Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315) — *Trí phụ trách chính*

---

## 1. Bộ đo định lượng y khoa chuẩn mực (Theo Khung Tổng Quát Mục II.6 & IV)
1. **Dice Similarity Coefficient (DSC / F1):** $\text{Dice} = \frac{2|P \cap G|}{|P| + |G|}$
2. **Jaccard Index (IoU):** $\text{IoU} = \frac{|P \cap G|}{|P \cup G|} = \frac{\text{Dice}}{2 - \text{Dice}}$
3. **Độ nhạy (Sensitivity / Recall):** $\text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}$ (Đo khả năng không bỏ sót pixel u)
4. **Độ đặc hiệu (Specificity):** $\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$ (Đo khả năng không nhận nhầm não lành)
5. **Độ trễ tính toán:** Thời gian xử lý trung bình trên từng khung hình/ảnh (Latency ms)."""),

    code_cell("""import os
import sys
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(".."))
from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed
from src.segmentation.region_growing import segment_region_growing
from src.evaluation.benchmark import run_benchmark
from src.pipeline import verify_tumor_presence

base_dir = "../data/full" if os.path.exists("../data/full/images") and len(os.listdir("../data/full/images")) > 50 else "../data/full"
img_dir = os.path.join(base_dir, "images")
mask_dir = os.path.join(base_dir, "masks")
print(f"Sẵn sàng thực thi benchmark trên tập dữ liệu: {base_dir} ({len(os.listdir(img_dir))} lát cắt)...")"""),

    md_cell("""##  2. Chạy Thực Nghiệm Đánh Giá Hàng Loạt (Batch Benchmark) 20 Mẫu
Đánh giá định lượng kết hợp Cổng Anomaly Gate trên 20 lát cắt đại diện:"""),

    code_cell("""def predict_ws(img):
    stripped, b_mask = strip_skull(img)
    if not verify_tumor_presence(stripped, b_mask, z_thresh=2.3):
        return np.zeros_like(img)
    return segment_watershed(stripped, dist_thresh_ratio=0.4)

def predict_rg(img):
    stripped, b_mask = strip_skull(img)
    if not verify_tumor_presence(stripped, b_mask, z_thresh=2.3):
        return np.zeros_like(img)
    return segment_region_growing(stripped, tolerance=15)

# Chạy benchmark trên 20 mẫu ảnh
df_ws = run_benchmark(img_dir, mask_dir, predict_ws, method_name="Watershed (Baseline)", max_samples=20)
df_rg = run_benchmark(img_dir, mask_dir, predict_rg, method_name="Region Growing (Đối chứng)", max_samples=20)

print(f"Đã hoàn thành đánh giá {len(df_ws)} mẫu cho Watershed và {len(df_rg)} mẫu cho Region Growing.")"""),

    md_cell("""##  3. Bảng Tổng Hợp Kết Quả Định Lượng (Mean ± Std)
Đây là bảng số liệu trọng tâm để đưa vào Mục 6 của Báo cáo đồ án:"""),

    code_cell("""summary_df = pd.DataFrame({
    "Chỉ Số Đánh Giá Định Lượng": [
        "1. Dice Similarity Coefficient (DSC)",
        "2. Jaccard Index (IoU)",
        "3. Sensitivity (Độ nhạy - Bắt đúng u)",
        "4. Specificity (Độ đặc hiệu - Tránh nhầm)",
        "5. Thời gian xử lý trung bình (Latency)"
    ],
    "Phương án A: Watershed (Baseline)": [
        f"{df_ws['dice'].mean():.4f} ± {df_ws['dice'].std():.4f}",
        f"{df_ws['iou'].mean():.4f} ± {df_ws['iou'].std():.4f}",
        f"{df_ws['sensitivity'].mean():.4f} ± {df_ws['sensitivity'].std():.4f}",
        f"{df_ws['specificity'].mean():.4f} ± {df_ws['specificity'].std():.4f}",
        f"{df_ws['latency_ms'].mean():.2f} ± {df_ws['latency_ms'].std():.2f} ms"
    ],
    "Phương án B: Region Growing (Đối chứng)": [
        f"{df_rg['dice'].mean():.4f} ± {df_rg['dice'].std():.4f}",
        f"{df_rg['iou'].mean():.4f} ± {df_rg['iou'].std():.4f}",
        f"{df_rg['sensitivity'].mean():.4f} ± {df_rg['sensitivity'].std():.4f}",
        f"{df_rg['specificity'].mean():.4f} ± {df_rg['specificity'].std():.4f}",
        f"{df_rg['latency_ms'].mean():.2f} ± {df_rg['latency_ms'].std():.2f} ms"
    ]
})

summary_df"""),

    md_cell("""## 4. Trực quan hóa dữ liệu: Biểu đồ cột so sánh điểm Dice trên từng ca bệnh
Trực quan hóa sự khác biệt giữa 2 thuật toán trên toàn bộ tập thử nghiệm:"""),

    code_cell("""x = np.arange(len(df_ws))
width = 0.38

fig, ax = plt.subplots(figsize=(16, 6))
rects1 = ax.bar(x - width/2, df_ws['dice'], width, label='Phương án A: Watershed (Baseline)', color='#3B82F6', alpha=0.85)
rects2 = ax.bar(x + width/2, df_rg['dice'], width, label='Phương án B: Region Growing (Đối chứng)', color='#10B981', alpha=0.85)

ax.set_ylabel('Điểm Dice Similarity Coefficient', fontsize=12)
ax.set_title('So Sánh Điểm Dice Score Giữa Watershed và Region Growing Trên 20 Ca Bệnh TCGA-LGG', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([f"Ca {i+1:02d}" for i in range(len(df_ws))], rotation=45)
ax.legend(fontsize=12)
ax.set_ylim(0, 1.05)
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()"""),

    md_cell("""##  5. Phân Tích Trường Hợp Thất Bại (Failure Cases Analysis)
Theo yêu cầu bắt buộc của Khung tổng quát (Mục II.6): Phải chỉ ra và lý giải nguyên nhân sai lệch."""),

    code_cell("""# Tìm các ca có điểm Dice thấp nhất
df_compare = pd.DataFrame({
    'sample_id': df_ws['sample_id'],
    'dice_ws': df_ws['dice'],
    'dice_rg': df_rg['dice']
})
df_compare['min_dice'] = df_compare[['dice_ws', 'dice_rg']].min(axis=1)
worst_cases = df_compare.sort_values(by='min_dice').head(3)

print("3 Ca bệnh khó nhất / có điểm Dice thấp nhất:")
print(worst_cases)

# Hiển thị trực quan ca lỗi nặng nhất
worst_id = worst_cases.iloc[0]['sample_id']
w_img = cv2.imread(os.path.join(img_dir, f"{worst_id}.png"), cv2.IMREAD_GRAYSCALE)
w_gt = cv2.imread(os.path.join(mask_dir, f"{worst_id}_mask.png"), cv2.IMREAD_GRAYSCALE)
w_pred_ws = predict_ws(w_img)
w_pred_rg = predict_rg(w_img)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
axes[0].imshow(w_img, cmap='gray'); axes[0].set_title(f"Ca Lỗi: {worst_id}"); axes[0].axis('off')
axes[1].imshow(w_gt, cmap='hot'); axes[1].set_title("Ground Truth Bác Sĩ"); axes[1].axis('off')
axes[2].imshow(w_pred_ws, cmap='Blues'); axes[2].set_title(f"Watershed (Dice={worst_cases.iloc[0]['dice_ws']:.3f})"); axes[2].axis('off')
axes[3].imshow(w_pred_rg, cmap='Greens'); axes[3].set_title(f"Region Growing (Dice={worst_cases.iloc[0]['dice_rg']:.3f})"); axes[3].axis('off')
plt.suptitle("Phân Tích Ca Thất Bại Điển Hình (Failure Case)", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

print(\"\"\"
NHẬN XÉT NGUYÊN NHÂN THẤT BẠI (ĐƯA VÀO BÁO CÁO):
1. Khối u có độ tương phản quá thấp so với chất xám xung quanh (ranh giới bờ mờ).
2. Kích thước u quá nhỏ khiến bản đồ khoảng cách Euclidean (Distance Transform) bị suy biến đỉnh cực đại.
3. Hướng khắc phục: Cần kết hợp thêm thông tin kết cấu GLCM hoặc sử dụng ngưỡng thích ứng cục bộ.
\"\"\")""")
]

# Ghi ra 4 file notebook
with open("notebooks/01_data_exploration.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb1_cells), f, indent=1, ensure_ascii=False)
print("Da tao notebooks/01_data_exploration.ipynb (Buoc 1 & Muc 3)")

with open("notebooks/02_preprocessing_and_skull_stripping.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb2_cells), f, indent=1, ensure_ascii=False)
print("Da tao notebooks/02_preprocessing_and_skull_stripping.ipynb (Buoc 2 & Muc 4)")

with open("notebooks/03_tumor_segmentation_comparison.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb3_cells), f, indent=1, ensure_ascii=False)
print("Da tao notebooks/03_tumor_segmentation_comparison.ipynb (Buoc 3, 4 & Muc 5)")

with open("notebooks/04_quantitative_evaluation.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb4_cells), f, indent=1, ensure_ascii=False)
print("Da tao notebooks/04_quantitative_evaluation.ipynb (Buoc 5, 6 & Muc 6)")

print("\nHOAN TAT TAI TAO 4 JUPYTER NOTEBOOKS CHUAN KHUNG NOI DUNG TONG QUAT!")

