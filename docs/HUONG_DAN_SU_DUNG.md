# HƯỚNG DẪN SỬ DỤNG VÀ VẬN HÀNH HỆ THỐNG
## Phân Đoạn & Phát Hiện Khối U Não Trên Ảnh Cộng Hưởng Từ MRI (TCGA-LGG)
**Học phần:** Xử lý ảnh số — Khoa Công nghệ Thông tin — Trường Đại học Công Thương TP.HCM (HUIT)  
**Nhóm sinh viên thực hiện:** Hà Mạnh Trường & Huỳnh Tâm Trí  
**Phiên bản:** v1.0.0 (Tháng 11/2026)

---

## MỤC LỤC
1. [Tổng quan Hệ thống & Kiến trúc Vận hành](#1-tổng-quan-hệ-thống--kiến-trúc-vận-hành)
2. [Kịch bản Nghiệm thu Nhanh trong 5 Phút (Dành cho Giảng viên & Hội đồng)](#2-kịch-bản-nghiệm-thu-nhanh-trong-5-phút-dành-cho-giảng-viên--hội-đồng)
3. [Yêu cầu Môi trường & Hướng dẫn Cài đặt Chuẩn](#3-yêu-cầu-môi-trường--hướng-dẫn-cài-đặt-chuẩn)
4. [Cẩm nang Vận hành Trạm Làm việc Y khoa NeuroScan PACS (Streamlit App)](#4-cẩm-nang-vận-hành-trạm-làm-việc-y-khoa-neuroscan-pacs-streamlit-app)
5. [Hướng dẫn Thực thi & Khảo sát 4 Jupyter Notebooks](#5-hướng-dẫn-thực-thi--khảo-sát-4-jupyter-notebooks)
6. [Hướng dẫn Chạy Benchmark Đa tiến trình Toàn bộ Dữ liệu](#6-hướng-dẫn-chạy-benchmark-đa-tiến-trình-toàn-bộ-dữ-liệu)
7. [Hướng dẫn Chạy Bộ Kiểm thử Tự động (Unit Tests)](#7-hướng-dẫn-chạy-bộ-kiểm-thử-tự-động-unit-tests)
8. [Hướng dẫn Lập trình viên Tích hợp Lõi Pipeline Python API](#8-hướng-dẫn-lập-trình-viên-tích-hợp-lõi-pipeline-python-api)
9. [Cẩm nang Xử lý Sự cố & Câu hỏi Thường gặp (FAQ & Troubleshooting)](#9-cẩm-nang-xử-lý-sự-cố--câu-hỏi-thường-gặp-faq--troubleshooting)

---

## 1. Tổng quan Hệ thống & Kiến trúc Vận hành

Hệ thống được thiết kế theo mô hình **Định hướng Xử lý Ảnh số Cổ điển (Classical Digital Image Processing - DIP)** kết hợp công nghệ trạm làm việc chẩn đoán hình ảnh y tế **NeuroScan PACS Workstation**, giải quyết triệt để bài toán phân đoạn và đo đạc định lượng khối u não trên chuỗi xung MRI FLAIR thuộc bộ dữ liệu chuẩn quốc tế **TCGA-LGG (3.929 lát cắt)** mà không phụ thuộc vào GPU hay các mô hình hộp đen Deep Learning.

```
       [Ảnh MRI FLAIR 256x256 uint8]
                     │
                     ▼
  ┌─────────────────────────────────────┐
  │ TẦNG 1: Tiền Xử Lý & Làm Trơn       │ ──> Lọc Median 3x3 khử nhiễu đốm Rician
  └─────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────┐
  │ TẦNG 2: Tách Sọ Não Hình Thái Học   │ ──> Otsu + Morphological Opening + LCC + Hole Filling
  └─────────────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────┐
  │ TẦNG 3: Cổng Kiểm Soát Dị Thường    │ ──> Anomaly Gate: Phân loại ca lành / u
  └─────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
  [Watershed EDT]       [Region Growing]
  Marker-controlled     Seeded Multi-seed
         └───────────┬───────────┘
                     │
                     ▼
  ┌─────────────────────────────────────┐
  │ TẦNG 4: Đo Đạc Y Sinh & Báo Cáo     │ ──> BBox, Diện tích, Độ tròn, Dice/IoU, Xuất Quad View
  └─────────────────────────────────────┘
```

---

## 2. Kịch bản Nghiệm thu Nhanh trong 5 Phút (Dành cho Giảng viên & Hội đồng)

Kịch bản này được thiết kế để Quý Thầy/Cô hoặc Ban Giám khảo có thể **nghiệm thu toàn bộ tính năng cốt lõi và kiểm chứng tính trung thực khoa học của đồ án trong vòng 5 phút**:

| Thời gian | Bước thao tác | Lệnh / Hành động thực hiện | Kết quả kỳ vọng hiển thị |
| :---: | :--- | :--- | :--- |
| **Phút 1** | Khởi động Trạm Web Demo | Chạy lệnh `streamlit run demo/app.py` trong terminal. | Trình duyệt tự động mở `http://localhost:8501`, giao diện PACS Workstation màu tối chuyên dụng hiển thị đầy đủ thanh công cụ. |
| **Phút 2** | Thử nghiệm **Ca có khối u rõ nét** | Tại mục *Nguồn Dữ Liệu*, chọn `Ca lâm sàng tiêu biểu (Phân loại)`. Chọn ca `TCGA_CS_4941_19960909_13` (Khối u rõ). | Hệ thống phát hiện u trong **~6 ms**. Hiển thị mặt nạ phân đoạn màu xanh neon, Bounding Box đỏ bao quanh khối u, Dice đạt **~92% - 94%**, tính toán diện tích u và độ tròn chính xác. |
| **Phút 3** | Thử nghiệm **Ca não lành tính (Không u)** | Vẫn ở mục ca tiêu biểu, chọn ca `TCGA_CS_4941_19960909_01` (Lát đỉnh sọ, hoàn toàn không có u). | Hệ thống kích hoạt **Clinical Anomaly Gate**, hiển thị thông báo huy hiệu xanh: *"Lát cắt não lành tính - Không phát hiện tổn thương khối u"*. Độ đặc hiệu đạt **100%**, loại bỏ hoàn toàn hiện tượng báo động giả. |
| **Phút 4** | Kiểm tra **Tính Giải Thích (Explainability)** | Mở hộp kiểm `Hiển thị chi tiết 8 bước ảnh trung gian`. Đổi thuật toán sang `Seeded Region Growing`. | Hiển thị ma trận 8 bước: Ảnh gốc $\rightarrow$ Lọc nhiễu $\rightarrow$ Nhị phân Otsu $\rightarrow$ Mặt nạ sọ não $\rightarrow$ Bản đồ khoảng cách EDT / Hạt giống $\rightarrow$ Mặt nạ phân đoạn $\rightarrow$ Ground Truth đối chứng $\rightarrow$ Ảnh Quad View. |
| **Phút 5** | Xác thực **Độ tin cậy mã nguồn (Unit Tests)** | Mở một tab terminal mới và gõ lệnh: `pytest -v`. | Toàn bộ **27 bài test** bao phủ 5 module (`measurement`, `metrics`, `pipeline`, `preprocessing`, `segmentation`) đều hiển thị trạng thái `PASSED` trong **< 2 giây**. |

---

## 3. Yêu cầu Môi trường & Hướng dẫn Cài đặt Chuẩn

### 3.1. Yêu cầu Hệ thống
* **Hệ điều hành:** Windows 10/11, macOS, hoặc Linux (Ubuntu 20.04+).
* **Python:** Phiên bản **Python 3.10** hoặc **3.11 / 3.12** (đã được kiểm thử tương thích tuyệt đối).
* **Bộ nhớ RAM:** Tối thiểu 4 GB (Khuyến nghị 8 GB để chạy benchmark đa tiến trình).
* **Phần cứng:** Chạy trên CPU tiêu chuẩn (Intel Core i3/i5 hoặc Apple Silicon), **không yêu cầu GPU**.

### 3.2. Cài đặt Môi trường trong 3 Bước

#### Bước 1: Mở Terminal tại thư mục gốc dự án
```bash
cd brain-tumor-mri-segmentation
```

#### Bước 2: Khởi tạo và Kích hoạt Môi trường ảo Python
* **Trên hệ điều hành Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(Nếu gặp lỗi script execution policy trên PowerShell, chạy trước lệnh: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

* **Trên hệ điều hành Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### Bước 3: Cài đặt các thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

> [!NOTE]
> Tệp `requirements.txt` đã được tối ưu hóa chuẩn mực, bao gồm: `numpy`, `scipy`, `opencv-python-headless`, `scikit-image`, `scikit-learn`, `pandas`, `pillow`, `matplotlib`, `seaborn`, `streamlit`, `huggingface_hub`, `ipykernel`, `nbformat`, `nbconvert`, `pytest`, `pyyaml`.

---

## 4. Cẩm nang Vận hành Trạm Làm việc Y khoa NeuroScan PACS (Streamlit App)

### 4.1. Khởi động Ứng dụng
```bash
streamlit run demo/app.py
```
Ứng dụng sẽ tự động khởi tạo máy chủ cục bộ và mở đường dẫn `http://localhost:8501` trên trình duyệt mặc định.

---

### 4.2. Chế độ Giao diện: Sáng & Tối (Light & Dark Theme)
* Trên góc phải thanh bên (Sidebar), chọn nút chuyển chế độ:
  - **Dark Mode (Mặc định chuẩn PACS Y khoa):** Nền đen xám y khoa (`#0e1117`), tăng độ tương phản của ảnh cộng hưởng từ, bảo vệ mắt bác sĩ chẩn đoán.
  - **Light Mode (Chế độ Trình chiếu & In ấn):** Nền trắng xám chuẩn văn phòng, thích hợp khi chiếu trên máy chiếu giảng đường hoặc in tài liệu.

---

### 4.3. Ba Nguồn Nạp Ảnh Lâm Sàng (Data Ingestion Modes)
Tại menu chọn **"Nguồn Dữ Liệu"** trên Sidebar, bạn có 3 lựa chọn linh hoạt:

1. **Nguồn 1: Tải ảnh từ máy tính (Upload ảnh cá nhân):**
   - Hỗ trợ định dạng `.png`, `.jpg`, `.jpeg`.
   - Cho phép nạp thêm tệp mặt nạ Ground Truth (tùy chọn) để tự động tính điểm Dice và IoU.
2. **Nguồn 2: Danh mục ca lâm sàng tiêu biểu (Phân loại bệnh học):**
   - Nhóm tác giả đã tuyển chọn sẵn các ca bệnh điển hình theo 4 phân nhóm y sinh:
     * *Khối u lớn, rõ nét:* Ca `TCGA_CS_4941_19960909_13` (U chiếm ~8% diện tích não).
     * *Khối u nhỏ ($< 1.5\%$ diện tích):* Ca `TCGA_DU_6404_19991206_14`.
     * *Khối u có bờ viền mờ nhạt, độ tương phản thấp:* Ca `TCGA_FG_5964_20010511_18`.
     * *Lát cắt não lành tính (Không u):* Ca `TCGA_CS_4941_19960909_01`.
3. **Nguồn 3: Kho dữ liệu đầy đủ TCGA-LGG (3.929 lát cắt):**
   - Cho phép duyệt cây thư mục theo từng bệnh nhân (110 mã bệnh nhân).
   - Chọn số thứ tự lát cắt để phân tích lát cắt giải phẫu dọc trục sọ não.

---

### 4.4. Chọn Phương pháp Phân đoạn & Tinh chỉnh Siêu tham số
Bạn có thể lựa chọn 1 trong 2 thuật toán lõi đối chứng:

#### A. Marker-controlled Watershed (Khuyến nghị chuẩn)
* **Cơ chế:** Biến đổi khoảng cách Euclidean (EDT) trên vùng não tách sọ $\rightarrow$ Xác định hạt giống tâm u $\rightarrow$ Lan tràn theo ranh giới gradient.
* **Các tham số tinh chỉnh:**
  - *Tỷ lệ ngưỡng khoảng cách (`dist_thresh_ratio`):* Mặc định `0.40`. Tăng lên nếu muốn tâm u thu nhỏ chính xác hơn; giảm xuống nếu u kích thước nhỏ.
  - *Hệ số giãn nở nền (`bg_dilate_kernel`):* Mặc định `3`. Kiểm soát vùng không xác định (Unknown boundary band).

#### B. Seeded Region Growing
* **Cơ chế:** Tự động tìm hạt giống tại vị trí có cường độ sáng cực đại sau lọc $\rightarrow$ Lan vùng kết nạp các điểm lân cận thỏa mãn dung sai cường độ.
* **Các tham số tinh chỉnh:**
  - *Dung sai cường độ (`intensity_tolerance`):* Mặc định `15` mức xám. Cho phép lan tỏa trong phạm vi $|I(p) - I(seed)| \le \text{tolerance}$.
  - *Ngưỡng diện tích tối thiểu/tối đa:* Lọc bỏ các đốm nhiễu nhỏ hơn 50 pixel hoặc vùng tràn quá 25.000 pixel.

---

### 4.5. Cơ chế Kiểm soát Dị thường (Clinical Anomaly Gate)
* **Công tắc trên Sidebar:** `Kích hoạt Cổng kiểm soát dị thường (Anomaly Gate)`.
* **Nguyên lý:** Phân tích biểu đồ phân bố cường độ xám của vùng nhu mô não sau tách sọ. Nếu tỷ lệ pixel tăng quang vượt ngưỡng $2.2 \times \sigma$ dưới $0.5\%$, hệ thống coi lát cắt là mô não lành tính và tự động ngắt thuật toán phân đoạn.
* **Ý nghĩa thực tế:** Giúp hệ thống đạt **độ đặc hiệu $99.04\%$**, ngăn chặn hoàn toàn việc nhận nhầm mô não lành thành khối u.

---

### 4.6. Đọc và Phiên giải Các Chỉ số Đo đạc Y sinh

Khi phát hiện khối u, hệ thống xuất bảng thông số định lượng chuẩn y khoa:

| Chỉ số hiển thị | Đơn vị | Ý nghĩa lâm sàng |
| :--- | :---: | :--- |
| **Trạng thái phát hiện** | Nhãn | `TUMOR DETECTED` (Có u) hoặc `HEALTHY BRAIN TISSUE` (Não lành). |
| **Tọa độ Bounding Box** | $(x, y, w, h)$ | Vị trí góc trên bên trái và chiều rộng, chiều cao của hình hộp bao quanh khối u (pixel). |
| **Diện tích khối u** | Pixels & $\text{mm}^2$ | Số lượng điểm ảnh của tổn thương và diện tích quy đổi thực tế (dựa trên độ phân giải quét). |
| **Tỷ lệ diện tích tổn thương** | $\%$ | Tỷ lệ phần trăm diện tích khối u so với toàn bộ diện tích nhu mô não sọ. |
| **Độ tròn bờ viền (Circularity)** | $[0.0, 1.0]$ | Công thức $C = \frac{4\pi A}{P^2}$. Khối u hình cầu đều có $C \approx 0.8 - 0.9$; khối u thâm nhiễm phân nhánh có $C < 0.5$. |
| **Chỉ số tương đồng Dice** | $[0.0, 1.0]$ | Đo mức độ trùng khớp giữa vùng phân đoạn và bác sĩ dán nhãn ($DSC \ge 0.70$ là mức chấp nhận y khoa xuất sắc). |
| **Chỉ số IoU (Jaccard Index)** | $[0.0, 1.0]$ | Đo tỷ lệ diện tích giao trên diện tích hợp ($IoU = \frac{Dice}{2 - Dice}$). |
| **Thời gian xử lý** | Mili-giây (ms) | Thời gian thực thi toàn bộ pipeline trên một lát cắt (trung bình ~6.13 ms). |

---

### 4.7. Xuất Kết quả & Lưu Trữ Báo cáo
* **Tải ảnh Quad View (2x2):** Nhấn nút `Tải ảnh Quad View chẩn đoán (PNG)` để lưu bức ảnh tổng hợp 4 ô gồm: Ảnh gốc, Mặt nạ tách sọ, Mặt nạ phân đoạn u, và Ảnh chẩn đoán phủ màu (Overlay).
* **Xuất Báo cáo Lâm sàng JSON:** Nhấn `Tải Báo cáo Lâm sàng (JSON)` để lưu toàn bộ số liệu đo đạc phục vụ tích hợp hồ sơ bệnh án điện tử (EMR).

---

## 5. Hướng dẫn Thực thi & Khảo sát 4 Jupyter Notebooks

Nhóm tác giả đã biên soạn 4 cuốn sổ tay Jupyter Notebook bao quát toàn bộ lộ trình nghiên cứu thực nghiệm từ thăm dò dữ liệu đến kiểm định thống kê:

```
notebooks/
├── 01_data_exploration.ipynb               # Khảo sát dữ liệu & phân tích thống kê 3.929 lát cắt
├── 02_preprocessing_and_skull_stripping.ipynb # Thử nghiệm các bộ lọc nhiễu & quy trình tách sọ não
├── 03_tumor_segmentation_comparison.ipynb  # Đối chứng trực quan & định lượng Watershed vs Region Growing
└── 04_quantitative_evaluation.ipynb        # Đánh giá toàn diện trên 3.929 ảnh, bảng số liệu & ROC/PR
```

### 5.1. Khởi chạy Notebook trong Môi trường Tương tác
Mở terminal và gõ:
```bash
jupyter lab
# hoặc mở trực tiếp trên VS Code bằng cách chọn kernel Python trong venv
```

### 5.2. Xem Báo cáo HTML Kết xuất Sẵn
Nếu không muốn chạy lại toàn bộ mã nguồn tính toán, Quý Thầy/Cô có thể nhấp đúp chuột để mở trực tiếp các bản báo cáo HTML đã xuất sẵn đầy đủ biểu đồ trong thư mục `reports/notebooks/`:
* `reports/notebooks/01_data_exploration.html`
* `reports/notebooks/02_preprocessing_and_skull_stripping.html`
* `reports/notebooks/03_tumor_segmentation_comparison.html`
* `reports/notebooks/04_quantitative_evaluation.html`

---

## 6. Hướng dẫn Chạy Benchmark Đa tiến trình Toàn bộ Dữ liệu

Tập lệnh benchmark cho phép quét và đánh giá tự động trên toàn bộ **3.929 lát cắt MRI** của 110 bệnh nhân, tận dụng cơ chế đa xử lý (multiprocessing) trên toàn bộ nhân CPU:

```bash
python scripts/run_all_experiments.py
```

### Kết quả đầu ra:
* Thời gian hoàn thành: Chỉ mất **~20 - 25 giây** trên CPU 8 nhân.
* Bảng tổng hợp được lưu tại: [docs/BENCHMARK_RESULTS.csv](file:///C:/Users/xpaga/Documents/xlas/docs/BENCHMARK_RESULTS.csv).
* Chi tiết từng ảnh được lưu tại: [docs/BENCHMARK_RESULTS_FULL.csv](file:///C:/Users/xpaga/Documents/xlas/docs/BENCHMARK_RESULTS_FULL.csv).

---

## 7. Hướng dẫn Chạy Bộ Kiểm thử Tự động (Unit Tests)

Dự án tuân thủ nghiêm ngặt chuẩn mực công nghệ phần mềm và kiểm thử hướng chất lượng (TDD). Toàn bộ 27 test cases bao quát:
- Kiểm tra độ tròn vòng tròn lý tưởng ($C = 1.0$).
- Kiểm tra tính bất biến của các chỉ số Dice/IoU khi khớp hoàn toàn hoặc không giao nhau.
- Kiểm tra hành vi pipeline trên lát cắt não rỗng hoặc không u.
- Kiểm tra tính bảo toàn vùng sọ não của giải thuật tách sọ.

### Lệnh chạy kiểm thử:
```bash
pytest -v
```

### Kết quả kỳ vọng:
```
tests/test_measurement.py::test_circularity_perfect_circle PASSED
tests/test_measurement.py::test_extract_tumor_features PASSED
...
tests/test_segmentation.py::test_watershed_parameter_variation PASSED
============================= 27 passed in 1.59s =============================
```

---

## 8. Hướng dẫn Lập trình viên Tích hợp Lõi Pipeline Python API

Bạn có thể dễ dàng nhúng lớp `BrainTumorPipeline` vào bất kỳ hệ thống phần mềm quản lý bệnh viện hoặc ứng dụng trí tuệ nhân tạo nào chỉ với 5 dòng mã:

```python
import cv2
from src.pipeline import BrainTumorPipeline

# 1. Khởi tạo pipeline (chọn method 'watershed' hoặc 'region_growing')
pipeline = BrainTumorPipeline(
    method="watershed",
    params={"dist_thresh_ratio": 0.40, "enable_presence_gate": True}
)

# 2. Đọc ảnh MRI sọ não chuỗi xung FLAIR (định dạng ảnh mức xám uint8)
image = cv2.imread("data/full/images/TCGA_CS_4941_19960909_13.png", cv2.IMREAD_GRAYSCALE)

# 3. Thực thi xử lý khép kín
result, intermediates = pipeline.process(image)

# 4. Truy xuất kết quả chẩn đoán
if result.tumor_detected:
    print(f"Phát hiện khối u não! Tọa độ BBox: {result.bbox}")
    print(f"Diện tích u: {result.tumor_area_px} px ({result.tumor_ratio_percent:.2f}% nhu mô não)")
    print(f"Độ tròn bờ viền: {result.circularity:.4f}")
else:
    print("Nhu mô não lành tính - Không phát hiện khối u.")

# 5. Lưu ảnh Quad View chẩn đoán phục vụ in ấn
cv2.imwrite("ket_qua_quad_view.png", intermediates["quad"])
```

---

## 9. Cẩm nang Xử lý Sự cố & Câu hỏi Thường gặp (FAQ & Troubleshooting)

### Q1: Cổng mạng 8501 của Streamlit báo lỗi đã bị chiếm dụng (`Port 8501 is already in use`)?
* **Nguyên nhân:** Có một tiến trình Streamlit cũ đang chạy ngầm hoặc phần mềm khác đang chiếm cổng 8501.
* **Cách khắc phục:** Khởi chạy Streamlit trên một cổng mạng khác bằng tham số `--server.port`:
  ```bash
  streamlit run demo/app.py --server.port 8502
  ```

---

### Q2: Ứng dụng báo lỗi không tìm thấy ảnh mẫu hoặc thư mục dữ liệu trống?
* **Nguyên nhân:** Dự án mới được clone và chưa tải kho dữ liệu đầy đủ 3.929 ảnh.
* **Cách khắc phục:** Chạy script tự động tải dữ liệu từ Hugging Face Hub:
  ```bash
  python scripts/download_full_dataset.py
  ```
  *(Dữ liệu sẽ được tự động giải nén vào `data/full/images/` và `data/full/masks/`)*

---

### Q3: Trên Windows PowerShell xuất hiện lỗi cấm chạy script (`Execution of scripts is disabled on this system`)?
* **Nguyên nhân:** Chính sách bảo mật ExecutionPolicy mặc định của Windows chặn chạy file activate ảo.
* **Cách khắc phục:** Mở PowerShell và gõ lệnh sau trước khi kích hoạt môi trường:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\venv\Scripts\Activate.ps1
  ```

---

### Q4: Watershed và Region Growing cho kết quả khác nhau trên cùng một khối u, nên tin tưởng thuật toán nào?
* **Giải thích chuyên môn:**
  - **Watershed EDT:** Có tính ổn định cao hơn, ranh giới bờ u tách bạch tốt ngay cả khi u có độ sáng không đồng nhất. Đây là giải thuật **khuyến nghị dùng làm cơ sở chẩn đoán chính** ($Dice \approx 0.730$).
  - **Region Growing:** Rất nhạy cảm với sự đồng nhất của mô u. Khi u có bờ mờ hoặc thâm nhiễm nhu mô lân cận, giải thuật có thể bị lan tràn hoặc co cụm ($Dice \approx 0.655$). Tuy nhiên, Region Growing giúp bác sĩ quan sát được vùng lõi tăng quang mạnh nhất của khối u.

---

### Q5: Báo cáo Word hoặc Slide thuyết trình nằm ở đâu trong thư mục dự án?
* Toàn văn báo cáo khoa học đồ án (chuẩn thể thức HUIT) nằm tại: [docs/BAO_CAO_DO_AN_XLAS.docx](file:///C:/Users/xpaga/Documents/xlas/docs/BAO_CAO_DO_AN_XLAS.docx) (và bản xem nhanh [docs/BAO_CAO_DO_AN_XLAS.md](file:///C:/Users/xpaga/Documents/xlas/docs/BAO_CAO_DO_AN_XLAS.md)).
* Bộ Slide thuyết trình 20 trang bảo vệ đồ án nằm tại: [reports/SLIDE_THUYET_TRINH_XLAS.pptx](file:///C:/Users/xpaga/Documents/xlas/reports/SLIDE_THUYET_TRINH_XLAS.pptx) và [reports/SLIDE_THUYET_TRINH_XLAS.pdf](file:///C:/Users/xpaga/Documents/xlas/reports/SLIDE_THUYET_TRINH_XLAS.pdf).
