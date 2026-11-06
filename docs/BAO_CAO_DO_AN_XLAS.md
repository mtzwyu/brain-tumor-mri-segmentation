# TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH (HUIT)
## KHOA CÔNG NGHỆ THÔNG TIN — NGÀNH KHOA HỌC DỮ LIỆU — BỘ MÔN XỬ LÝ ẢNH SỐ

---

# BÁO CÁO ĐỒ ÁN HỌC PHẦN: XỬ LÝ ẢNH SỐ
### MÃ HỌC PHẦN: 0101006276 — NĂM HỌC: 2026 – 2027

## ĐỀ TÀI:
# PHÂN ĐOẠN VÀ PHÁT HIỆN TỔN THƯƠNG TRÊN ẢNH Y TẾ
### (NGHIÊN CỨU TRỌNG TÂM: PHÂN ĐOẠN VÀ PHÁT HIỆN KHỐI U NÃO TRÊN ẢNH CỘNG HƯỞNG TỪ MRI — TCGA-LGG)

---

### DANH SÁCH THÀNH VIÊN VÀ PHÂN CÔNG NHIỆM VỤ (SPRINT 7 NGÀY)
| STT | Họ và Tên Sinh Viên | Mã Số Sinh Viên | Lớp Sinh Hoạt | Vai Trò | Trách Nhiệm Trọng Tâm (Sprint 7 Ngày) | Tỷ Lệ Đóng Góp (%) |
| :---: | :--- | :---: | :---: | :---: | :--- | :---: |
| 1 | **Hà Mạnh Trường** | **2045240326** | 15DHKHDL03 | **Nhóm trưởng** | Quản lý tiến độ Sprint 7 ngày, đặc tả kiến trúc `SPEC_PIPELINE_MRI.md`, Pipeline tiền xử lý & Tách sọ (Skull Stripping 6 bước), Thuật toán phân đoạn u Baseline (Watershed) & Đối chứng (Region Growing), Báo cáo kỹ thuật (Chương 2, 4, 5, 6 kỹ thuật). | **50%** |
| 2 | **Huỳnh Tâm Trí** | **2045240315** | 15DHKHDL03 | **Thành viên** | Thu thập & quản lý dữ liệu 3,929 lát TCGA-LGG, Rút trích đặc trưng hình học (Area, Circularity, Bounding Box), Bộ đo định lượng y khoa (Dice, IoU, Sens, Spec), Giao diện Streamlit GUI, Báo cáo tổng quan (Chương 1, 3, 6 số liệu, 7, 8), Slide & Video demo. | **50%** |

**GIẢNG VIÊN HƯỚNG DẪN:** ThS. Đỗ Hùng Dũng  
*TP. Hồ Chí Minh, Năm học 2026 – 2027*

---

# LỜI MỞ ĐẦU

Trong kỷ nguyên số hóa y tế hiện đại, việc ứng dụng các kỹ thuật Xử lý ảnh số (Digital Image Processing - DIP) vào công tác hỗ trợ chẩn đoán lâm sàng đang trở thành xu hướng mũi nhọn của ngành Khoa học Dữ liệu. Đặc biệt, đối với các bệnh lý thần kinh đe dọa trực tiếp tính mạng con người như khối u não, việc hỗ trợ khoanh vùng khối u trên ảnh cộng hưởng từ (Magnetic Resonance Imaging - MRI) không chỉ giảm tải áp lực cực lớn cho các bác sĩ chuyên khoa mà còn mang lại tính nhất quán, khách quan và độ tin cậy toán học cao.

Đề tài «Phân đoạn và phát hiện tổn thương trên ảnh y tế» (nghiên cứu trọng tâm chuyên sâu vào bài toán phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI) được nhóm sinh viên thực hiện trong khuôn khổ học phần Xử lý ảnh số tại Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT). Toàn bộ phương pháp trong nghiên cứu này được thiết kế theo nguyên tắc giải trình minh bạch của xử lý ảnh cổ điển: từ kỹ thuật khử nhiễu song phương, thuật toán bóc sọ não hình thái học 6 bước, đến việc đối chứng định lượng độc lập giữa hai giải thuật Marker-controlled Watershed và Seeded Region Growing trên toàn bộ 3,929 lát cắt chuẩn quốc tế TCGA-LGG.

Nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc và chân thành nhất đến Thầy ThS. Đỗ Hùng Dũng cùng các Thầy, Cô trong Bộ môn Xử lý ảnh số — Ngành Khoa học Dữ liệu — Khoa Công nghệ Thông tin, Trường Đại học Công Thương TP. Hồ Chí Minh đã tận tình giảng dạy, truyền đạt nền tảng lý thuyết vững chắc và định hướng phương pháp nghiên cứu khoa học chuẩn mực cho chúng em trong suốt học kỳ qua.

---

# TÓM TẮT ĐỒ ÁN

Báo cáo này trình bày quá trình nhóm nghiên cứu tìm hiểu, thiết kế và xây dựng hệ thống phần mềm xử lý ảnh số hỗ trợ chẩn đoán khối u não trên ảnh cộng hưởng từ MRI. Hệ thống giải quyết 3 bài toán kỹ thuật cốt lõi:
1. **Khử nhiễu Rician và bảo toàn ranh giới mô u:** Sử dụng bộ lọc Bilateral kết hợp cân bằng tương phản thích nghi CLAHE.
2. **Thuật toán Tách sọ não (Skull Stripping) 6 bước:** Kết hợp hình thái học toán học và thành phần liên thông lớn nhất (LCC), loại bỏ xương sọ và da đầu ra khỏi ảnh.
3. **Cài đặt và thực nghiệm đối chứng 02 phương án phân đoạn u não độc lập:** Marker-controlled Watershed (dựa trên biến đổi khoảng cách Euclidean EDT) và Seeded Region Growing (phát triển vùng từ hạt giống cực đại cường độ).

Hệ thống được kiểm thử thực nghiệm quy mô lớn trên toàn bộ kho dữ liệu chuẩn quốc tế TCGA-LGG gồm 3,929 lát cắt MRI từ 110 bệnh nhân (1,373 lát có u và 2,556 lát não lành). Kết quả cho thấy phương pháp Marker-controlled Watershed đạt chỉ số tương đồng Dice trung bình 0.4446 ± 0.3014, vượt trội gấp 2.23 lần so với Seeded Region Growing (0.1990 ± 0.2682) với độ trễ xử lý ổn định chỉ 6.13 ms/lát cắt. Đặc biệt, trên 2,556 lát não lành, cả hai giải thuật đều đạt độ đặc hiệu trên 97.6% (Watershed đạt 99.04%), chứng minh khả năng triệt tiêu hầu như hoàn toàn báo động giả ngoài sọ. Hệ thống được đóng gói với giao diện web Streamlit cho phép bác sĩ thao tác chẩn đoán tương tác thời gian thực.

**Từ khóa:** Xử lý ảnh số, Ảnh MRI sọ não, Tách sọ não (Skull Stripping), Phân thủy Marker-controlled Watershed, Phát triển vùng Seeded Region Growing, TCGA-LGG Benchmark, Đánh giá định lượng y sinh.

---

# MỤC LỤC BÁO CÁO

* **LỜI MỞ ĐẦU**
* **TÓM TẮT ĐỒ ÁN (ABSTRACT)**
* **BẢNG PHÂN CÔNG NHIỆM VỤ SINH VIÊN**
* **CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI**
  * 1.1. Bối cảnh thực tế & Tính cấp thiết của bài toán
  * 1.2. Mục tiêu nghiên cứu của đề tài
  * 1.3. Đối tượng và phạm vi nghiên cứu
* **CHƯƠNG 2: CƠ SỞ LÝ THUYẾT XỬ LÝ ẢNH SỐ**
  * 2.1. Phép lọc phi tuyến bảo toàn biên (Bilateral Filter)
  * 2.2. Phép toán hình thái học (Mathematical Morphology)
  * 2.3. Giải thuật phân thủy Marker-controlled Watershed
  * 2.4. Giải thuật phát triển vùng từ hạt giống (Seeded Region Growing)
  * 2.5. Các chỉ số đánh giá định lượng y sinh học chuẩn quốc tế
* **CHƯƠNG 3: MÔ TẢ TẬP DỮ LIỆU MRI TCGA-LGG**
  * 3.1. Nguồn gốc dữ liệu & Các liên kết công bố quốc tế
  * 3.2. Cấu trúc tổ chức dữ liệu thực nghiệm
  * 3.3. Phân bố dữ liệu và phân tầng kích thước u não
* **CHƯƠNG 4: TIỀN XỬ LÝ ẢNH VÀ TÁCH SỌ NÃO**
  * 4.1. Khử nhiễu Rician và Cân bằng tương phản mô mềm
  * 4.2. Quy trình 6 bước Tách sọ não (Skull Stripping Pipeline)
* **CHƯƠNG 5: PHƯƠNG PHÁP PHÂN ĐOẠN U NÃO VÀ PIPELINE**
  * 5.1. Sơ đồ luồng xử lý pipeline tổng thể 4 tầng
  * 5.2. Phương pháp phân đoạn A (Baseline): Marker-controlled Watershed
  * 5.3. Phương pháp phân đoạn B (Đối chứng): Seeded Region Growing
  * 5.4. Rút trích đặc trưng hình học khối u và cảnh báo thị giác
* **CHƯƠNG 6: KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG**
  * 6.1. Bảng số liệu so sánh định lượng trên 3,929 lát cắt TCGA-LGG
  * 6.2. Đồ thị đối chiếu chỉ số y sinh và phân bố hiệu năng
  * 6.3. Phân tích kết quả thực nghiệm và các ca thất bại (Failure Cases)
* **CHƯƠNG 7: XÂY DỰNG ỨNG DỤNG MINH HỌA DEMO WEB UI**
  * 7.1. Tổng quan trạm làm việc chẩn đoán NeuroScan PACS Workstation
  * 7.2. Cơ chế chuyển đổi giao diện kép (Clinical Light & Dark Mode)
  * 7.3. Ba phân hệ nạp dữ liệu lâm sàng độc lập
  * 7.4. Phân hệ Phân đoạn u & Tích hợp Cổng Anomaly Gate tiền lọc
  * 7.5. Khu vực Chẩn đoán đa chế độ & Trực quan hóa y sinh chuyên sâu
  * 7.6. Hướng dẫn cài đặt và vận hành hệ thống
* **CHƯƠNG 8: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN**
  * 8.1. Các kết quả chính đạt được của đề tài
  * 8.2. Hạn chế và hướng nghiên cứu mở rộng
* **TÀI LIỆU THAM KHẢO**
* **PHỤ LỤC**
  * Phụ lục A: Khung Rubric Đánh Giá Đồ Án Môn Học Của Khoa CNTT — HUIT
  * Phụ lục B: Bảng Tổng Hợp Phân Công Nhiệm Vụ Sprint Cấp Tốc 7 Ngày Chi Tiết
  * Phụ lục C: Hướng Dẫn Cài Đặt & Chạy Thử Toàn Bộ Hệ Thống

---

# CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI

### 1.1. Bối cảnh thực tế & Tính cấp thiết
Khối u não (Brain Tumor: u tế bào đệm - Glioma, u màng não - Meningioma, u tuyến yên - Pituitary) là một trong những bệnh lý thần kinh nguy hiểm hàng đầu đe dọa trực tiếp đến tính mạng con người. Việc phát hiện sớm, khoanh vùng chính xác vị trí và đo lường kích thước khối u đóng vai trò then chốt trong việc lập phác đồ xạ trị, phẫu thuật và theo dõi tiến triển bệnh. Ảnh cộng hưởng từ (Magnetic Resonance Imaging - MRI) là tiêu chuẩn vàng trong chẩn đoán nhờ khả năng tái tạo mô mềm với độ tương phản cao và không gây phơi nhiễm bức xạ ion hóa. Tuy nhiên, việc đọc và khoanh vùng khối u thủ công qua hàng trăm lát cắt mỗi ca chụp tốn rất nhiều thời gian và dễ sai lệch do chủ quan của bác sĩ.

### 1.2. Mục tiêu nghiên cứu của đề tài
* Xây dựng hệ thống phần mềm xử lý ảnh số hỗ trợ chẩn đoán khối u não trên ảnh MRI:
  * **Đầu vào:** Ảnh cắt lát MRI sọ não 2D định dạng Grayscale ($256 \times 256$) ở chuỗi xung FLAIR và T1-CE.
  * **Đầu ra:** Mặt nạ nhị phân phân đoạn khối u (Binary Mask), đường bao contour và Hộp giới hạn (Bounding Box) màu đỏ cảnh báo, cùng bảng số liệu định lượng (Diện tích, Tỷ lệ % u/não, Độ tròn bờ u Circularity, Chỉ số Dice/IoU).
* Cài đặt và đối chứng thực nghiệm **tối thiểu 02 phương án phân đoạn** (Marker-controlled Watershed vs. Seeded Region Growing) theo đúng quy định của Bộ môn.

### 1.3. Đối tượng và phạm vi nghiên cứu
* **Đối tượng nghiên cứu:** Các lát cắt MRI sọ não 2D mặt phẳng cắt ngang (Axial plane), thuộc chuỗi xung T1 có tiêm chất tương phản từ (T1-CE) hoặc chuỗi xung FLAIR, nơi khối u biểu hiện tăng cường độ sáng rõ nét.
* **Phạm vi và giới hạn kỹ thuật:** Ứng dụng hoàn toàn các kỹ thuật **Xử lý ảnh số truyền thống (DIP)** có thể giải trình minh bạch công thức, không dùng mô hình "hộp đen" Deep Learning làm lõi xử lý, tuân thủ nghiêm ngặt quy tắc của Bộ môn.

---

# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT XỬ LÝ ẢNH SỐ
*(Trích dẫn chuẩn mực theo giáo trình Digital Image Processing - Gonzalez & Woods, 4th Edition)*

### 2.1. Phép lọc phi tuyến bảo toàn biên (Bilateral Filter)
Để khử nhiễu Rician đặc trưng trên ảnh MRI mà không làm nhòe ranh giới mong manh giữa khối u và mô não lành, hệ thống sử dụng bộ lọc Bilateral kết hợp khoảng cách không gian và độ chênh lệch mức xám:
$$I^{\text{filtered}}(p) = \frac{1}{W_p} \sum_{q \in S} I(q) \cdot \exp\left(-\frac{\|p - q\|^2}{2\sigma_s^2}\right) \cdot \exp\left(-\frac{|I(p) - I(q)|^2}{2\sigma_r^2}\right)$$
Trong đó $\sigma_s = 75$ kiểm soát bán kính láng giềng, $\sigma_r = 75$ kiểm soát độ nhạy mức xám, $W_p$ là thừa số chuẩn hóa tổng trọng số bằng 1.

### 2.2. Phép toán hình thái học (Morphological Operations)
* **Phép mở (Opening):** $A \circ B = (A \ominus B) \oplus B$ (Co ảnh rồi Giãn ảnh) với phần tử cấu trúc đĩa elip ($5 \times 5$, 2 lần lặp), có tác dụng cắt đứt các cầu nối mô liên kết giữa hộp sọ và màng não, xóa các đốm nhiễu nhỏ ngoài sọ.
* **Phép đóng (Closing):** $A \bullet B = (A \oplus B) \ominus B$ (Giãn ảnh rồi Co ảnh) giúp lấp đầy các rãnh vỏ não và nối liền các đường nét đứt gãy.
* **Lấp đầy lỗ hổng (Hole Filling):** Sử dụng phép tái tạo hình thái học hoặc FloodFill để lấp đầy hệ thống não thất rỗng bên trong não.

### 2.3. Giải thuật phân thủy Marker-controlled Watershed
Để giải quyết triệt để hiện tượng phân đoạn quá mức (Over-segmentation) của thuật toán Watershed truyền thống, hệ thống áp dụng biến đổi khoảng cách Euclidean (EDT):
$$D(p) = \min_{q \in \text{Background}} \|p - q\|_2$$
Từ bản đồ khoảng cách, xác định vùng chắc chắn u (Sure Foreground) qua ngưỡng tỷ lệ $\text{Thresh} = 0.4 \times \max(D)$. Vùng chắc chắn nền (Sure Background) thu được bằng phép giãn nở hình thái học. Đánh dấu nhãn hạt giống (Markers) và cho lan truyền đường phân thủy theo gradient ảnh.

### 2.4. Giải thuật phát triển vùng từ hạt giống (Seeded Region Growing)
Thuật toán xác định điểm hạt giống $\text{Seed} = (y_0, x_0)$ là vị trí có cường độ sáng cực đại trong vùng não đã lọc sọ. Quá trình lan truyền duyệt láng giềng 8 điểm theo điều kiện:
$$|I(q) - I(\text{Seed})| \le \text{tolerance} \quad (\text{tolerance} = 15)$$
Kèm bộ lọc điều kiện diện tích khối u hợp lệ: $50 \le \text{Area} \le 25,000$ pixels.

### 2.5. Các chỉ số đánh giá định lượng y sinh học chuẩn quốc tế
* **Dice Similarity Coefficient (DSC / F1-Score):** $\text{Dice} = \frac{2|P \cap G|}{|P| + |G|} = \frac{2\text{TP}}{2\text{TP} + \text{FP} + \text{FN}}$
* **Jaccard Index (Intersection over Union - IoU):** $\text{IoU} = \frac{|P \cap G|}{|P \cup G|} = \frac{\text{Dice}}{2 - \text{Dice}}$
* **Sensitivity (Độ nhạy / Recall):** $\text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}$
* **Specificity (Độ đặc hiệu):** $\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$

---

# CHƯƠNG 3: MÔ TẢ TẬP DỮ LIỆU MRI TCGA-LGG

### 3.1. Nguồn gốc dữ liệu & Các liên kết công bố quốc tế
Dữ liệu thực nghiệm của đồ án được trích xuất từ bộ dữ liệu chuẩn quốc tế **TCGA-LGG** (The Cancer Genome Atlas Low-Grade Glioma), công bố bởi tác giả Mateusz Buda et al. (2019) trên tạp chí *Computers in Biology and Medicine*:
1. **Hugging Face Datasets (Nguồn chính của Đồ án):** [https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research](https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research) (Gồm 3,929 lát cắt MRI có mặt nạ u não Ground Truth).
2. **Kaggle Benchmark Dataset (Kho đối chứng / Dự phòng):** [https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation).
3. **Viện Y tế Quốc gia Hoa Kỳ TCIA (NIH/NCI):** [https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG](https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG).

### 3.2. Cấu trúc tổ chức dữ liệu thực nghiệm
Toàn bộ dữ liệu thực nghiệm của đồ án được lưu trữ tập trung tại thư mục `data/full/`:
* Toàn bộ **3,929 lát cắt chuẩn TCGA-LGG từ 110 bệnh nhân**, gồm ảnh PNG $256 \times 256$, mặt nạ nhị phân Ground Truth và bảng `metadata.csv` chi tiết.
* Dữ liệu được tải và chuẩn hóa bằng kịch bản `python scripts/download_full_dataset.py`.

### 3.3. Phân bố dữ liệu và phân tầng kích thước u não
* **Tổng số lát cắt:** 3,929 lát cắt (110 bệnh nhân).
* **Lát cắt có khối u (Positive):** 1,373 lát cắt (34.95%).
* **Lát cắt não lành (Healthy / Negative):** 2,556 lát cắt (65.05%).

*Bảng 3.1: Thống kê phân bố phân nhóm kích thước u não trên tập benchmark 3,929 lát cắt*
| Phân Nhóm Dữ Liệu | Tiêu Chuẩn Diện Tích | Số Lượng Lát Cắt | Tỷ Lệ / Tập U (1,373 lát) | Tỷ Lệ / Toàn Tập (3,929 lát) |
| :--- | :---: | :---: | :---: | :---: |
| Não lành (Không có u) | $0.0\%$ diện tích | 2,556 lát cắt | — | 65.05% |
| Khối u nhỏ (Small Tumors) | $< 1.5\%$ diện tích não | 463 lát cắt | 33.72% | 11.78% |
| Khối u trung bình (Medium Tumors) | $1.5\% - 5.0\%$ diện tích não | 667 lát cắt | 48.58% | 16.98% |
| Khối u lớn (Large Tumors) | $> 5.0\%$ diện tích não | 243 lát cắt | 17.70% | 6.19% |
| **Tổng cộng toàn bộ** | **Toàn dải dữ liệu** | **3,929 lát cắt** | **100.0%** (1,373 u) | **100.0%** |

---

# CHƯƠNG 4: TIỀN XỬ LÝ ẢNH VÀ TÁCH SỌ NÃO

### 4.1. Khử nhiễu Rician và Cân bằng tương phản mô mềm
1. **Khử nhiễu Rician:** Áp dụng bộ lọc Bilateral ($d=9, \sigma_c=75, \sigma_s=75$) trên ảnh xám chuẩn hóa $256 \times 256$, bảo toàn sắc nét đường ranh giới u.
2. **Cân bằng tương phản thích nghi:** Áp dụng thuật toán CLAHE với giới hạn tương phản `clip_limit=2.0` và kích thước khối `tile_grid_size=(8, 8)`.

### 4.2. Quy trình 6 bước Tách sọ não (Skull Stripping Pipeline)
* **Bước 1 — Phân ngưỡng Otsu:** Tìm ngưỡng tối ưu phân tách toàn bộ vùng đầu khỏi nền đen.
* **Bước 2 — Morphological Opening:** Sử dụng phần tử đĩa elip ($5 \times 5$, 2 lần lặp) để cắt đứt cầu nối mô giữa xương sọ và nhu mô não.
* **Bước 3 — Trích xuất thành phần liên thông lớn nhất (LCC):** Giữ lại duy nhất vùng nhu mô não trung tâm.
* **Bước 4 — Lấp đầy não thất (Hole Filling):** Sử dụng thuật toán FloodFill để lấp đầy hệ thống khoang não thất chứa dịch não tủy.
* **Bước 5 — Làm mịn mặt nạ não (Brain Mask):** Áp dụng phép Closing với kernel elip $7 \times 7$.
* **Bước 6 — Trích xuất ảnh não sạch sọ (Stripped Brain):** Thực hiện phép nhân Bitwise-AND giữa ảnh gốc và mặt nạ não để thu được ảnh nhu mô não không còn xương sọ và da đầu.

![Hình 4.1: Chi tiết 6 bước trong quy trình Tách sọ não Skull Stripping trên ảnh MRI](reports/figures/skull_stripping_steps.png)  
*Hình 4.1: Chi tiết 6 bước trong quy trình Tách sọ não Skull Stripping trên ảnh MRI*

---

# CHƯƠNG 5: PHƯƠNG PHÁP PHÂN ĐOẠN U NÃO VÀ PIPELINE

### 5.1. Sơ đồ luồng xử lý pipeline tổng thể 4 tầng
```
[Ảnh MRI Gốc (FLAIR/T1-CE)] 
          │
          ▼
1. Tầng 1: Chuẩn hóa kích thước (256x256) & Lọc Bilateral khử nhiễu
          │
          ▼
2. Tầng 2: Tách sọ não (Skull Stripping) 6 bước bằng hình thái học & LCC
          │
          ▼
3. Tầng 3: Phân đoạn u não lõi (Chuyển đổi linh hoạt qua Strategy Pattern)
   ├── Phương án A (Baseline chính): Marker-controlled Watershed
   └── Phương án B (Đối chứng): Seeded Region Growing
          │
          ▼
4. Tầng 4: Rút trích đặc trưng hình học (Area, Circularity, Bounding Box)
          │
          ▼
5. Đánh giá định lượng (Dice, IoU, Sens, Spec) & Trực quan hóa Streamlit GUI
```

### 5.2. Phương pháp phân đoạn A (Baseline): Marker-controlled Watershed
Áp dụng biến đổi khoảng cách Euclidean (EDT) trên mặt nạ vùng sáng sơ bộ. Ngưỡng hóa khoảng cách tại tỷ lệ tối ưu `dist_thresh_ratio = 0.4` để sinh mầm chắc chắn là u (Sure Foreground). Phép giãn nở tạo vùng chắc chắn là nền (Sure Background). Giải thuật Watershed mở rộng ranh giới phân thủy chính xác.

![Hình 5.1: Đồ thị khảo sát độ nhạy của siêu tham số dist_thresh_ratio](reports/figures/watershed_param_sensitivity.png)  
*Hình 5.1: Đồ thị khảo sát độ nhạy của siêu tham số dist_thresh_ratio trong giải thuật Marker-controlled Watershed*

### 5.3. Phương pháp phân đoạn B (Đối chứng): Seeded Region Growing
Thuật toán xác định tọa độ điểm pixel có cường độ sáng cực đại bên trong nhu mô não đã bóc sọ để làm hạt giống ban đầu. Lan truyền theo hàng đợi BFS với 8 láng giềng liên thông theo ngưỡng dung sai cường độ `tolerance = 15`. Lọc bỏ các đảo u có diện tích ngoài khoảng $[50, 25000]$ pixels.

### 5.4. Rút trích đặc trưng hình học khối u và cảnh báo thị giác
* **Diện tích u ($S_{\text{tumor}}$):** Tổng số pixel dương tính trong mặt nạ u.
* **Tỷ lệ % u/não:** $\text{Ratio} = (S_{\text{tumor}} / S_{\text{brain}}) \times 100\%$.
* **Độ tròn Circularity ($C$):** $C = \frac{4\pi \cdot \text{Area}}{\text{Perimeter}^2}$. $C \to 1.0$ thể hiện bờ u tròn đều; $C < 0.5$ thể hiện u ác tính xâm lấn.
* **Hộp giới hạn (Bounding Box):** Hình chữ nhật $[x, y, w, h]$ viền đỏ cảnh báo trực quan vị trí u não.

---

# CHƯƠNG 6: KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG

### 6.1. Bảng số liệu so sánh định lượng trên 3,929 lát cắt TCGA-LGG (Mean ± Std)

*Bảng 6.1: So sánh hiệu năng định lượng giữa Watershed và Region Growing trên 3,929 lát cắt TCGA-LGG (Mean ± Std)*
| Nhóm Dữ Liệu | Thuật Toán Phân Đoạn | Dice (DSC / F1) | IoU (Jaccard) | Sensitivity | Specificity | Độ Trễ / Ảnh |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Lát cắt có u (1,373 lát)** | **Marker-controlled Watershed** | **0.4446 ± 0.3014** | **0.3368 ± 0.2677** | **0.4436 ± 0.3170** | **0.9915 ± 0.0107** | **6.13 ± 3.32 ms** |
| | Seeded Region Growing | 0.1990 ± 0.2682 | 0.1416 ± 0.2119 | 0.2226 ± 0.3221 | 0.9851 ± 0.0432 | 12.13 ± 22.83 ms |
| **Lát não lành (2,556 lát)** | **Marker-controlled Watershed** | N/A (Không u) | N/A | N/A | **0.9904 ± 0.0100** | **6.15 ± 3.40 ms** |
| | Seeded Region Growing | N/A (Không u) | N/A | N/A | 0.9760 ± 0.0480 | 12.05 ± 21.50 ms |

### 6.2. Đồ thị đối chiếu chỉ số y sinh và phân bố hiệu năng

![Hình 6.1: Biểu đồ cột so sánh hiệu năng Dice, IoU, Sensitivity, Specificity](reports/figures/benchmark_metrics_comparison.png)  
*Hình 6.1: Biểu đồ cột so sánh hiệu năng Dice, IoU, Sensitivity, Specificity giữa Watershed và Region Growing trên 3,929 lát cắt*

### 6.3. Phân tích kết quả thực nghiệm và các ca thất bại (Failure Cases)
1. **Ưu thế vượt trội của Marker-controlled Watershed:** Nhờ cơ chế gieo mầm dựa trên biến đổi khoảng cách Euclidean (EDT), Watershed đạt chỉ số Dice trung bình 0.4446 (gấp 2.23 lần Region Growing: 0.1990) và thời gian thực thi ổn định chỉ ~6.13 ms/lát cắt. Thuật toán neo hạt giống vững chắc ở tâm u ngay cả khi biên u có độ dốc mức xám yếu.
2. **Hạn chế của Seeded Region Growing khi mở rộng quy mô:** Việc tìm hạt giống bằng giá trị cực đại cường độ đơn lẻ rất nhạy cảm với các tàn dư mạch máu hoặc vùng chất xám tăng quang. Ở các ca u nhỏ ($< 1.5\%$ diện tích não), hạt giống dễ bị lệch ra ngoài ổ u dẫn đến độ tương đồng thấp ($Dice \approx 0$).
3. **Khả năng triệt tiêu dương tính giả xuất sắc:** Trên toàn bộ 2,556 lát não lành, cả hai thuật toán đều đạt độ đặc hiệu $> 97.6\%$ (Watershed đạt $99.04\%$). Điều này chứng minh thuật toán Tách sọ não (Skull Stripping) đã loại bỏ triệt để tín hiệu xương sọ và mô mềm ngoài sọ, không gây báo động giả trên người khỏe mạnh.

---

# CHƯƠNG 7: XÂY DỰNG ỨNG DỤNG MINH HỌA DEMO WEB UI

### 7.1. Tổng quan trạm làm việc chẩn đoán NeuroScan PACS Workstation
Nhằm đưa các thuật toán xử lý ảnh số kinh điển từ lý thuyết thực nghiệm vào môi trường ứng dụng lâm sàng trực quan, đề tài đã xây dựng hoàn chỉnh trạm làm việc chẩn đoán hình ảnh thần kinh mang tên **NeuroScan PACS Workstation**. Ứng dụng được phát triển trên nền tảng **Streamlit** kết hợp bộ thư viện tính toán hiệu năng cao **NumPy** và **OpenCV**, đáp ứng tiêu chuẩn phản hồi thời gian thực với độ trễ xử lý cực thấp ($< 15\text{ ms}$ cho một chu trình chẩn đoán hoàn chỉnh).

Hệ thống tuân thủ kiến trúc phân tầng module hóa nghiêm ngặt:
* **Tầng lõi thuật toán (`src/`):** Chứa các pipeline xử lý tiền xử lý, tách sọ não, phân đoạn Watershed/Region Growing, tính toán chỉ số hình học và bộ đo tương quan y sinh.
* **Tầng trợ năng giao diện (`demo/utils.py`):** Đảm nhiệm các chức năng đọc nạp ảnh xám Unicode, trực quan hóa bản đồ sai số y sinh (Clinical Error Map), và quản lý danh mục ca bệnh chuẩn.
* **Tầng điều phối trạm làm việc (`demo/app.py`):** Quản lý trạng thái phiên làm việc (Session State), chuyển đổi theme giao diện, điều hướng 3 phân hệ dữ liệu và kết xuất dữ liệu lâm sàng.

### 7.2. Cơ chế chuyển đổi giao diện kép (Clinical Light & Dark Mode)
Một trong những yêu cầu đặc thù của môi trường y tế là sự biến thiên về điều kiện ánh sáng làm việc giữa phòng khám ban ngày và phòng đọc ảnh chuyên biệt (Reading Room). NeuroScan PACS Workstation được tích hợp cơ chế chuyển đổi giao diện Kép (Dual Theme Engine) dựa trên hệ thống biến CSS toàn cục:
1. **Chế độ Sáng (Clinical Light Mode):** Sử dụng tông nền xám trắng trang nhã (`#f8fafc`), độ tương phản cao, tối ưu cho việc in ấn bệnh án, trình chiếu giảng dạy hoặc hội chẩn trong điều kiện ánh sáng tự nhiên.
2. **Chế độ Tối (Clinical Dark Mode):** Được thiết kế chuyên biệt cho phòng đọc ảnh chẩn đoán của bác sĩ X-quang/MRI. Giao diện sử dụng nền xanh đen sâu (`#0d1322`, `#111827`) đạt chuẩn chống mỏi thị giác (Eye-strain Reduction) khi làm việc liên tục trong thời gian dài. Toàn bộ các thành phần tương tác (khung chọn lát cắt, thanh cuộn, thanh trượt tinh chỉnh tham số, khung nạp tệp và mã lát cắt dạng Cyan Badge `rgba(14, 165, 233, 0.15)`) đều được tối ưu hóa độ tương phản và tự động đảo màu chữ, triệt tiêu hoàn toàn hiện tượng chói mắt hoặc mất chữ.

### 7.3. Ba phân hệ nạp dữ liệu lâm sàng độc lập
Để tạo sự thuận tiện tối đa cho bác sĩ và hội đồng đánh giá, bảng điều khiển (Sidebar) của trạm làm việc được quy hoạch thành 3 phân hệ nạp dữ liệu tách biệt rõ ràng:
1. **Phân hệ 1: 4 Ca lâm sàng tiêu biểu (Benchmark Presets):** Tuyển chọn 4 trường hợp kinh điển từ tập dữ liệu TCGA-LGG nhằm minh họa tức thì các tình huống chẩn đoán:
   * *Ca 1 (`TCGA_CS_6290_20000917_10`):* Khối u điển hình, bờ rõ ràng, độ tương phản cao (Đạt chỉ số Dice $0.971$).
   * *Ca 2 (`TCGA_CS_6186_20000601_16`):* Khối u kích thước lớn ($2,079\text{ px}$), chiếm tỷ lệ lớn khoang sọ não.
   * *Ca 3 (`TCGA_CS_4942_19970222_12`):* Khối u bờ phức tạp, ranh giới thâm nhiễm (Infiltrative border, Dice $0.943$).
   * *Ca 4 (`TCGA_DU_5851_19950428_2`):* Lát cắt não lành hoàn toàn không có u ($0\text{ px}$ u), đóng vai trò ca đối chứng âm tính.
2. **Phân hệ 2: Kho chuẩn TCGA-LGG (3,929 lát cắt):** Cho phép truy xuất toàn bộ kho dữ liệu thực nghiệm. Bác sĩ có thể lọc dữ liệu theo từng bệnh nhân trong số 110 bệnh nhân hoặc duyệt theo toàn bộ danh mục lát cắt. Khi chọn bất kỳ lát cắt nào, hệ thống tự động tải mặt nạ đối chứng Ground Truth chuyên gia tương ứng.
3. **Phân hệ 3: Tải ảnh từ máy tính (Custom Clinical Upload):** Hỗ trợ bác sĩ tải lên tệp ảnh MRI mới ngoài tập dữ liệu (.png, .jpg, .tif) kèm tùy chọn tải thêm mặt nạ Ground Truth chuyên gia để kiểm thử tính tương thích tổng quát của pipeline trên dữ liệu ngoại vi.

### 7.4. Phân hệ Phân đoạn u & Tích hợp Cổng Anomaly Gate tiền lọc
Trạm làm việc cho phép linh hoạt cấu hình giải thuật phân đoạn cốt lõi và các tham số vận hành:
* **Lựa chọn giải thuật:** Bác sĩ có thể chuyển đổi tức thì giữa **Marker-controlled Watershed** (Phương án khuyến nghị chính) và **Seeded Region Growing** (Phương án đối chứng) để so sánh hiệu năng trên cùng một lát cắt.
* **Bộ tinh chỉnh tham số thời gian thực (Interactive Parameter Tuning):** Bố trí trong khung mở rộng (Expander) bao gồm: Hệ số ngưỡng Otsu ($0.8 - 1.5$), Kích thước phần tử cấu trúc Morphological Kernel ($3 \times 3 - 7 \times 7$), và Bán kính làm mờ Gaussian.
* **Cổng kiểm tra tổn thương Anomaly Gate (Clinical Anomaly Gate):** Tích hợp thuật toán tiền lọc 2 tầng dựa trên phân tích phân bố cường độ mô não ($Z$-score $\ge 2.3$ và Độ tương phản cực đại $\ge 15\%$). Khi kích hoạt trên các lát cắt não lành (như Ca 4), hệ thống tự động phát hiện không có tổn thương tăng sáng bất thường, chặn hoàn toàn việc phân đoạn giả và trả về mặt nạ rỗng với độ đặc hiệu $100\%$ ($Dice = 1.0000$).

### 7.5. Khu vực Chẩn đoán đa chế độ & Trực quan hóa y sinh chuyên sâu
Khu vực trung tâm trạm làm việc cung cấp đầy đủ các góc nhìn khoa học hỗ trợ quyết định chẩn đoán:
* **Hệ thống 5 thẻ chỉ số chẩn đoán (KPI Metric Cards):**
  1. *Trạng thái chẩn đoán:* Báo động đỏ "PHÁT HIỆN KHỐI U" hoặc nhãn xanh "NÃO LÀNH (ÂM TÍNH)".
  2. *Diện tích khối u:* Đo đếm chính xác số lượng pixel và quy đổi diện tích thực tế.
  3. *Tỷ lệ chiếm chỗ:* Tỷ lệ phần trăm diện tích u trên tổng thiết diện nhu mô não sạch sọ.
  4. *Độ tròn bờ u (Circularity):* Định lượng độ gồ ghề của đường biên ($C \approx 1$ dạng tròn đều, $C \ll 1$ bờ thâm nhiễm).
  5. *Độ tương đồng y khoa:* Hiển thị điểm số Dice Similarity Coefficient và chỉ số Jaccard (IoU) đối chiếu với Ground Truth.
* **Chế độ Lưới hiển thị 4 ô (Quad View):** Hiển thị trực quan toàn bộ tiến trình biến đổi ảnh số qua 4 khung hình song song:
  $$[Ảnh\text{ MRI Gốc} \mid Ảnh\text{ Não Sạch Sọ} \mid Mặt\text{ Nạ Phân Đoạn U} \mid Khoanh\text{ Vùng Bounding Box Đỏ}]$$
* **Chế độ So sánh đối chứng trực tiếp (Dual Comparison View):** Đặt mặt nạ phân đoạn của thuật toán cạnh mặt nạ Ground Truth của bác sĩ để đối chiếu bờ khối u.
* **Bản đồ phân tích sai số y sinh (Clinical Error Map):** Mã hóa màu sai số trực quan trên nền ảnh MRI gốc giảm độ sáng ($40\%$ luminance):
  * *Màu Xanh lá cây (True Positive - TP):* Vùng thuật toán định vị và phân đoạn hoàn toàn trùng khớp với chuyên gia.
  * *Màu Đỏ tươi (False Positive - FP):* Vùng thuật toán nhận nhầm mô lành thành u (Báo động giả).
  * *Màu Vàng cam (False Negative - FN):* Vùng khối u thực tế bị thuật toán bỏ sót (Bỏ sót tổn thương).
* **Xuất báo cáo kết quả (CSV Export):** Cung cấp nút bấm tải xuống bảng dữ liệu tổng hợp các thông số chẩn đoán (ID ca bệnh, thuật toán, diện tích, tỷ lệ, độ tròn, điểm Dice/IoU, thời gian xử lý) phục vụ tích hợp trực tiếp vào Bệnh án điện tử (EMR/EHR).

![Hình 7.1: Giao diện trực quan hóa Quad View chẩn đoán và khoanh vùng Bounding Box đỏ](docs/images/pipeline_quad_sample.png)  
*Hình 7.1: Giao diện trực quan hóa Quad View chẩn đoán và khoanh vùng Bounding Box đỏ cảnh báo u não*

### 7.6. Hướng dẫn cài đặt và vận hành hệ thống
Để khởi chạy trạm làm việc, người dùng chỉ cần thực hiện câu lệnh duy nhất từ thư mục gốc của dự án:
```bash
streamlit run demo/app.py
```
Ứng dụng sẽ tự động mở trên trình duyệt mặc định tại địa chỉ `http://localhost:8501`. Hệ thống yêu cầu môi trường Python 3.10+ với các thư viện `streamlit`, `opencv-python`, `numpy`, `pandas`, `scipy` và sẵn sàng vận hành trên các máy trạm y tế chuẩn mà không đòi hỏi phần cứng GPU chuyên dụng.

---

# CHƯƠNG 8: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 8.1. Các kết quả chính đạt được
* Xây dựng thành công quy trình xử lý ảnh số khép kín, minh bạch toán học phục vụ phân đoạn u não MRI.
* Cài đặt thành công kỹ thuật Tách sọ não kinh điển bằng hình thái học và thuật toán LCC, đạt độ đặc hiệu $99.04\%$ trên não lành.
* Thực hiện so sánh đối chứng khoa học, khách quan trên toàn bộ 3,929 lát cắt dữ liệu TCGA-LGG giữa 2 thuật toán Watershed và Region Growing.
* Xây dựng giao diện Web Demo Streamlit trực quan, phản hồi thời gian thực dưới 15ms.

### 8.2. Hạn chế và hướng nghiên cứu mở rộng
* Mở rộng từ không gian 2D sang tái tạo không gian 3D thể tích khối u (3D Voxel Rendering).
* Nghiên cứu tích hợp đặc trưng kết cấu GLCM (Haralick Texture Features) để nâng cao độ nhạy trên các ca u nhỏ biên mờ.
* Nghiên cứu kết hợp bộ phân lớp học máy cổ điển (SVM / Random Forest) để hỗ trợ phân loại các dạng u khác nhau (Glioma, Meningioma, Pituitary).

---

# TÀI LIỆU THAM KHẢO

[1] R. C. Gonzalez and R. E. Woods, *Digital Image Processing*, 4th ed., New York, NY: Pearson Education, Inc., 2018.  
[2] M. Buda, A. Saha, and M. A. Mazurowski, "Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm," *Computers in Biology and Medicine*, vol. 109, pp. 218-225, 2019.  
[3] Bộ môn Khoa học Dữ liệu — Khoa CNTT, *Giáo trình Xử lý ảnh số (Mã HP: 0101006276)*, TP. Hồ Chí Minh: Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT), 2026.  
[4] Khoa Công nghệ Thông tin — HUIT, *Kế hoạch thực hiện Đồ án Xử lý ảnh số năm học 2026–2027 (Kèm Rubric chấm điểm đồ án)*, TP. Hồ Chí Minh: Trường Đại học Công Thương TP. Hồ Chí Minh, 2026.  
[5] G. Bradski, "The OpenCV Library," *Dr. Dobb's Journal of Software Tools*, vol. 25, no. 11, pp. 120-125, 2000.  
[6] C. Tomasi and R. Manduchi, "Bilateral filtering for gray and color images," in *Proc. 6th IEEE Int. Conf. Computer Vision (ICCV)*, 1998, pp. 839-846.  
[7] F. Meyer, "Topographic distance and watershed lines," *Signal Processing*, vol. 38, no. 1, pp. 113-125, 1994.  
[8] R. Adams and L. Bischof, "Seeded region growing," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 16, no. 6, pp. 641-647, 1994.

---

# PHỤ LỤC

### Phụ lục A: Khung Rubric Đánh Giá Đồ Án Môn Học Của Khoa CNTT — HUIT (Thang điểm 10)
*(Chiếm 100% phần thi cuối kỳ, tương đương 70% tổng điểm học phần)*

*Bảng Phụ lục A.1: Khung Rubric đánh giá đồ án học phần Xử lý ảnh số của Khoa CNTT - HUIT*
| STT | Tiêu chí đánh giá | Chuẩn đầu ra (PLO/CLO) | Trọng số | Điểm tối đa |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Phân tích và lựa chọn đúng phương pháp | PLO2 / CLO1 | 15% | 1.5 điểm |
| 2 | Áp dụng được các phương pháp xử lý *(Trọng tâm)* | PLO2 / CLO2 | 50% | 5.0 điểm |
| 3 | Đọc tài liệu, nghiên cứu giải quyết bài toán | PLO4 / CLO3 | 10% | 1.0 điểm |
| 4 | Trình bày báo cáo | PLO7 / CLO5 | 15% | 1.5 điểm |
| 5 | Phân công và phối hợp làm việc nhóm | PLO6 / CLO4 | 10% | 1.0 điểm |
| **TỔNG** | **ĐIỂM ĐÁNH GIÁ CUỐI KỲ** | **ĐẠT CHUẨN ĐẦU RA** | **100%** | **10.0 điểm** |

### Phụ lục B: Bảng Tổng Hợp Phân Công Nhiệm Vụ Sprint Cấp Tốc 7 Ngày Chi Tiết

*Bảng Phụ lục B.1: Tiến độ và phân công chi tiết Sprint cấp tốc 7 ngày giữa hai thành viên*
| Ngày | Nội dung công việc trọng tâm | Hà Mạnh Trường (Nhóm trưởng) | Huỳnh Tâm Trí (Thành viên) | Sản phẩm nghiệm thu |
| :---: | :--- | :--- | :--- | :--- |
| **Ngày 1** | Khởi động Sprint, Chuẩn hóa Dữ liệu & Đặc tả Kỹ thuật | Chủ trì lập kế hoạch Sprint 7 ngày, soạn thảo đặc tả `SPEC_PIPELINE_MRI.md` (13 signatures, 7 invariants) | Chuẩn hóa toàn bộ 3,929 lát cắt dữ liệu TCGA-LGG, chạy Notebook 01 EDA, xuất `DATA_EXPLORATION_REPORT.md` | `SPEC_PIPELINE_MRI.md`, Notebook 01, Báo cáo dữ liệu |
| **Ngày 2** | Tiền xử lý, Tách sọ não 6 bước & Bộ đo Y sinh | Cài đặt `filters.py` (Bilateral + CLAHE), `skull_strip.py` 6 bước kinh điển, hoàn thiện Notebook 02 | Cài đặt module `metrics.py` (Dice, IoU, Sens, Spec), xử lý an toàn mẫu rỗng $0/0$, viết test unit | `src/preprocessing/`, `src/evaluation/metrics.py`, Unit tests |
| **Ngày 3** | Phân đoạn Baseline Watershed & Đo Đặc trưng Hình học | Cài đặt `watershed.py` với biến đổi khoảng cách EDT, khảo sát ngưỡng `dist_thresh_ratio` | Cài đặt `features.py` (diện tích u, circularity, bounding box) và `visualization.py` (hộp đỏ, viền vàng, Quad view) | `src/segmentation/watershed.py`, `src/measurement/`, Unit tests |
| **Ngày 4** | Phân đoạn Đối chứng Region Growing & Ghép nối Pipeline | Cài đặt `region_growing.py` (tự tìm seed cực đại cường độ, BFS 8 láng giềng), tích hợp `BrainTumorPipeline` | Hoàn thiện Notebook 03 (so sánh song song Watershed vs Region Growing), xây dựng framework benchmark | `src/pipeline.py`, Notebook 03, Bảng nhận xét định tính |
| **Ngày 5** | Benchmark Quy mô lớn (3,929 lát cắt) & Web Demo GUI | Phân tích chuyên sâu các ca thất bại (Failure cases: u nhỏ <1.5%, u biên mờ, u chèn ép não thất) | Hoàn thiện Streamlit GUI (`demo/app.py`) Dual-mode, chạy benchmark đa tiến trình 3,929 lát cắt và Notebook 04 | `BENCHMARK_RESULTS.csv`, Notebook 04, Streamlit Web App |
| **Ngày 6** | Biên soạn Toàn văn Báo cáo Đồ án 12 Mục chuẩn HUIT | Soạn thảo 4 chương kỹ thuật (Chương 2, 4, 5, 6 kỹ thuật) | Soạn thảo 6 chương tổng quan (Chương 1, 3, 6 số liệu, 7, 8, Phụ lục) | `BAO_CAO_DO_AN_XLAS.md`, `BAO_CAO_DO_AN_XLAS.docx` (Word chuẩn lề 3-3-3-2 cm) |
| **Ngày 7** | Chuẩn hóa Mã nguồn, Slide Thuyết trình, Video Demo & Đóng gói | Rà soát toàn bộ code `src/`, bổ sung docstring tiếng Việt cho toàn bộ hàm, bảo đảm toàn bộ unit tests đạt | Thiết kế bộ Slide 20 trang (`SLIDE_THUYET_TRINH_OUTLINE.md`), quay Video demo 3 phút, đóng gói ZIP trọn bộ hồ sơ | Slide PPTX/PDF, Video Demo MP4, Bộ mã nguồn sạch, Hồ sơ nộp hoàn chỉnh |
| **Nghiệm thu** | BÁO CÁO ĐỒ ÁN TẠI LỚP HỌC PHẦN XỬ LÝ ẢNH SỐ | Thuyết trình phần kỹ thuật, giải thuật và phân tích ca lỗi | Thuyết trình phần dữ liệu, số liệu định lượng và trình diễn Demo GUI | Báo cáo thành công, đạt chuẩn đầu ra môn học |

### Phụ lục C: Hướng Dẫn Cài Đặt & Chạy Thử Toàn Bộ Hệ Thống
```bash
# 1. Clone mã nguồn đồ án
git clone https://github.com/mtzwyu/brain-tumor-mri-segmentation.git
cd brain-tumor-mri-segmentation

# 2. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt

# 3. Tải toàn bộ 3,929 lát cắt chuẩn TCGA-LGG (tùy chọn mở rộng)
python scripts/download_full_dataset.py

# 4. Chạy toàn bộ kiểm thử đơn vị (Unit Tests)
pytest tests/ -v

# 5. Chạy benchmark định lượng đa tiến trình
python scripts/run_all_experiments.py

# 6. Khởi chạy giao diện demo tương tác Web Streamlit
streamlit run demo/app.py
```
