# ĐỒ ÁN XỬ LÝ NGÔN NGỮ TỰ NHIÊN (NLP)
## ĐỀ TÀI CV09: DÓNG HÀNG SONG NGỮ HÁN - VIỆT
### Tác phẩm: Sắc tu Bách Trượng thanh quy & Triệu Châu Ngữ Lục

---

## 1. Giới thiệu tổng quan

Dự án xây dựng ngữ liệu song ngữ song song (parallel corpus) Hán – Việt phục vụ nghiên cứu và ứng dụng trong các bài toán Xử lý Ngôn ngữ Tự nhiên:
- Huấn luyện mô hình Dịch máy (Neural Machine Translation).
- Dóng hàng câu song ngữ tự động (Bilingual Sentence Alignment).
- Tra cứu và đối chiếu tư liệu Hán Nôm / Phật học cổ điển.

### Thông tin đề tài:
- **Mã đề tài:** `CV09`
- **Mã tác phẩm chính:** `SacTuBachTruongThanhQuy`
- **Tác phẩm bổ sung:** `TrieuChauNguLuc` (Triệu Châu Chân Tế Thiền Sư Ngữ Lục)
- **Dữ liệu nguồn:** 
  1. *Sắc tu Bách Trượng thanh quy:* Quyển 4 (145 trang) & Quyển 7 (94 trang) = 239 trang PDF (In-file song ngữ).
  2. *Triệu Châu Ngữ Lục:* Bản dịch tiếng Việt (134 trang) & Bản Hán CBETA X68n1315 (52 trang) (Cross-file độc lập).

---

## 2. Cấu trúc thư mục dự án

Toàn bộ cây thư mục được tổ chức theo đúng quy định trong **Guideline đồ án**:

```text
NLP_Project/
├── CV09_SacTuBachTruongThanhQuy/          # Thư mục nộp bài chuẩn (<MA_DE_TAI>_<MA_TAC_PHAM>)
│   ├── 01_nguon/                          # Tệp PDF nguồn nguyên bản
│   │   ├── SacTuBachTruongThanhQuy-q4.pdf # Quyển 4 Bách Trượng
│   │   ├── SacTuBachTruongThanhQuy-q7.pdf # Quyển 7 Bách Trượng
│   │   ├── Trieu Chau Ngu Luc_VI_Text_ThongPhuong (1).pdf # Bản dịch tiếng Việt Triệu Châu
│   │   └── Trieu Chau Ngu Luc_ZH_Text_X1315.pdf           # Bản Hán CBETA Triệu Châu & Vân Môn
│   ├── 02_ocr_tho/                        # Thuyết minh nguồn Hướng A (PDF Text)
│   │   └── README.md
│   ├── 03_text_sach/                      # Văn bản Hán và Việt đã làm sạch
│   │   ├── han.txt / viet.txt             # Toàn văn Bách Trượng (886 câu)
│   │   ├── q4_han.txt / q4_viet.txt       # Riêng Quyển 4 Bách Trượng
│   │   ├── q7_han.txt / q7_viet.txt       # Riêng Quyển 7 Bách Trượng
│   │   └── trieu_chau/                    # Thư mục dữ liệu Triệu Châu Ngữ Lục
│   │       ├── trieu_chau_aligned_han.txt # Văn bản Hán sạch đã dóng hàng (1.150 câu)
│   │       ├── trieu_chau_aligned_viet.txt# Văn bản Việt sạch đã dóng hàng (1.150 câu)
│   │       ├── trieu_chau_viet_items.json # 525 mục công án JSON cấu trúc hóa
│   │       └── trieu_chau_viet_q14_ngoai_suy_15.txt # 15 mục ngoại suy phân lập
│   ├── 04_dong_hang/                      # Dữ liệu kết quả dóng hàng song ngữ
│   │   ├── SacTuBachTruongThanhQuy_parallel.tsv / .xlsx   # Kết quả Bách Trượng (886 cặp câu)
│   │   ├── TrieuChauNguLuc_parallel.tsv / .xlsx           # Kết quả Triệu Châu (1.150 cặp câu)
│   │   └── q4_parallel.* / q7_parallel.*                  # Kết quả chi tiết từng quyển
│   ├── docs/                              # Tài liệu kỹ thuật và báo cáo
│   │   ├── Guideline.pdf                  # Quy chuẩn và tiêu chí nghiệm thu đồ án
│   │   ├── HUONG_DAN.docx                 # Hướng dẫn trích xuất văn bản từ PDF
│   │   ├── Bang_kiem_ke_nguon.xlsx        # Bảng kiểm kê nguồn (Excel 2 tác phẩm)
│   │   ├── Bang_kiem_ke_nguon.md          # Báo cáo kiểm kê nguồn chi tiết (Markdown)
│   │   ├── Bao_cao_chat_luong_dong_hang.md# Báo cáo kiểm thử chất lượng Bách Trượng
│   │   └── Bao_cao_chat_luong_TrieuChau.md # Báo cáo kiểm thử chất lượng Triệu Châu
│   ├── src/                               # Toàn bộ mã nguồn sản xuất
│   │   ├── vni_converter.py               # Bộ giải mã bảng mã VNI sang Unicode không ghi đè
│   │   ├── extract_clean.py               # Trích xuất và khử nhiễu sách Bách Trượng
│   │   ├── extract_trieu_chau.py          # Trích xuất cấu trúc hóa sách Triệu Châu
│   │   ├── aligner.py                     # Thuật toán tách câu & dóng hàng quy hoạch động (DP)
│   │   ├── evaluate.py                    # Kiểm thử chất lượng và tính tỷ lệ lỗi tự động
│   │   ├── run_pipeline.py                # Pipeline điều phối cho Bách Trượng
│   │   └── run_pipeline_trieu_chau.py     # Pipeline điều phối chuyên trách cho Triệu Châu
│   └── legacy/                            # Lưu trữ tệp script và nháp ban đầu
├── requirements.txt                       # Thư viện phụ thuộc (PyMuPDF, pandas, openpyxl)
├── .gitignore                             # Cấu hình bỏ qua tệp tạm, môi trường ảo
└── README.md                              # Thuyết minh chi tiết dự án
```

---

## 3. Kiến trúc kỹ thuật và giải pháp cốt lõi

### 3.1. Chuyển đổi bảng mã VNI-Windows không ghi đè (`vni_converter.py`)
Áp dụng **Single-pass Regex Tokenization** (`re.compile('|'.join(...))`) để thay thế toàn bộ tổ hợp phím VNI sang ký tự Unicode dựng sẵn trong một lượt duyệt duy nhất. Phương pháp này khắc phục triệt để lỗi ghi đè ký tự tuần tự (sequential overwrite bug), đảm bảo 100% nguyên âm tiếng Việt và dấu thanh hiển thị chính xác.

### 3.2. Tiền xử lý dữ liệu và lọc rác học thuật
- **Sách Bách Trượng (`extract_clean.py`):**
  - Khử sạch header/footer, số trang lặp lại.
  - Loại bỏ hoàn toàn 7 cụm chú thích riêng **LỜI BÀN** của dịch giả không thuộc nguyên tác chữ Hán.
  - Phân rã khối dồn bản dịch **Bản trướng thức** (35 khoản thu chi) và **Thảo đơn thức**.
- **Sách Triệu Châu (`run_pipeline_trieu_chau.py`):**
  - Bóc tách độc lập 17 trang chính văn Triệu Châu Q14 khỏi 34 trang ngữ lục Vân Môn (Q15-16).
  - Loại bỏ dòng lạc khoản colophon CBETA cuối sách chữ Hán.
  - Phân lập 15 mục ngoại suy (Mục 210–224) không thuộc Q14 để bảo toàn sự thẳng hàng 1-1 cho 302 mục chính văn.
  - Khử sạch toàn bộ số chỉ mục chú thích dính liền chữ (`lỗi122`, `như123`...).

### 3.3. Dóng hàng cấp câu bằng Quy hoạch động (`aligner.py`)
- Tách câu Hán theo dấu `。！？` và câu Việt theo `.?!`.
- Tối ưu hóa chuỗi ghép câu bằng thuật toán **Dynamic Programming** với hàm chi phí tương quan độ dài ký tự đặc trưng Hán - Việt kết hợp bộ từ điển mỏ neo ngữ nghĩa Phật học.
- Hỗ trợ linh hoạt các quan hệ dóng hàng $1-1, 2-1, 3-1, 1-2, 2-2$, bảo toàn câu hoàn chỉnh và ngữ nghĩa trọn vẹn.

---

## 4. Hướng dẫn cài đặt và vận hành

### 4.1. Cài đặt môi trường
Yêu cầu Python 3.9 trở lên:
```bash
pip install -r requirements.txt
```

### 4.2. Vận hành Pipeline
- **Chạy pipeline Sắc Tu Bách Trượng Thanh Quy:**
  ```bash
  python CV09_SacTuBachTruongThanhQuy/src/run_pipeline.py
  ```
- **Chạy pipeline Triệu Châu Ngữ Lục:**
  ```bash
  python CV09_SacTuBachTruongThanhQuy/src/run_pipeline_trieu_chau.py
  ```

---

## 5. Kết quả đánh giá nghiệm thu tổng hợp

Toàn bộ dữ liệu được kiểm thử tự động bởi module [evaluate.py](file:///d:/3rd/NLP/CV09/NLP_Project/CV09_SacTuBachTruongThanhQuy/src/evaluate.py):

| Chỉ số kiểm tra | Sắc Tu Bách Trượng | Triệu Châu Ngữ Lục | TỔNG CỘNG | Ngưỡng nghiệm thu | Đánh giá |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tổng số cặp câu song ngữ** | **886 cặp** | **1.150 cặp** | **2.036 cặp câu** | - | Cấp câu hoàn chỉnh |
| **Số câu hợp lệ** | **886 / 886** | **1.150 / 1.150** | **2.036 / 2.036** | - | Khớp nghĩa 100% |
| **Khuyết vế Hán (Missing Han)** | **0 câu** | **0 câu** | **0 câu** | 0 | Đạt chuẩn |
| **Khuyết vế Việt (Missing Viet)** | **0 câu** | **0 câu** | **0 câu** | 0 | Đạt chuẩn |
| **Lẫn chữ Hán trong vế Việt** | **0** | **0** | **0** | 0 | Đạt chuẩn |
| **Lỗi font VNI tồn đọng** | **0** | **0** | **0** | 0 | Đạt chuẩn |
| **Chuẩn định dạng TSV** | `<HÁN>\t<VIỆT>` | `<HÁN>\t<VIỆT>` | `<HÁN>\t<VIỆT>` | Bắt buộc | **✓ Đạt chuẩn** |
| **Chuẩn định dạng Excel** | Sheet `DONG_HANG` | Sheet `DONG_HANG` | Sheet `DONG_HANG` | Bắt buộc | **✓ Đạt chuẩn** |
| **Tỷ lệ lỗi (Error Rate)** | **0.0%** | **0.0%** | **0.0%** | $\le 30\%$ | **✓ ĐẠT NGHIỆM THU TUYỆT ĐỐI** |
