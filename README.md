# ĐỒ ÁN XỬ LÝ NGÔN NGỮ TỰ NHIÊN (NLP)
## ĐỀ TÀI CV09: DÓNG HÀNG SONG NGỮ HÁN - VIỆT
### Tác phẩm: Sắc tu Bách Trượng thanh quy (勅修百丈清規) - Quyển 4 & Quyển 7

---

## 1. Giới thiệu tổng quan

Dự án xây dựng ngữ liệu song ngữ song song (parallel corpus) Hán – Việt phục vụ nghiên cứu và ứng dụng trong các bài toán Xử lý Ngôn ngữ Tự nhiên:
- Huấn luyện mô hình Dịch máy (Neural Machine Translation).
- Dóng hàng câu song ngữ tự động (Bilingual Sentence Alignment).
- Tra cứu và đối chiếu tư liệu Hán Nôm / Phật học cổ điển.

### Thông tin đề tài:
- **Mã đề tài:** `CV09`
- **Mã tác phẩm:** `SacTuBachTruongThanhQuy`
- **Dữ liệu nguồn:** 
  - Quyển 4: 145 trang (trang 408 đến 550)
  - Quyển 7: 94 trang (trang 276 đến 367)
  - Tổng số: **239 trang PDF** (định dạng PDF Text layer có sẵn).

---

## 2. Cấu trúc thư mục dự án

Toàn bộ cây thư mục được tổ chức theo đúng quy định trong **Guideline đồ án**:

```text
NLP_Project/
├── CV09_SacTuBachTruongThanhQuy/          # Thư mục nộp bài chuẩn (<MA_DE_TAI>_<MA_TAC_PHAM>)
│   ├── 01_nguon/                          # Tệp PDF nguồn nguyên bản
│   │   ├── SacTuBachTruongThanhQuy-q4.pdf # Quyển 4
│   │   └── SacTuBachTruongThanhQuy-q7.pdf # Quyển 7
│   ├── 02_ocr_tho/                        # Thư mục chuẩn cấu trúc bàn giao
│   │   └── README.md                      # Thuyết minh nguồn thuộc Hướng A (PDF Text)
│   ├── 03_text_sach/                      # Văn bản Hán và Việt đã làm sạch
│   │   ├── han.txt                        # Toàn văn chữ Hán (722 câu)
│   │   ├── viet.txt                       # Toàn văn tiếng Việt Unicode (722 câu)
│   │   ├── q4_han.txt / q4_viet.txt       # Văn bản riêng Quyển 4
│   │   └── q7_han.txt / q7_viet.txt       # Văn bản riêng Quyển 7
│   ├── 04_dong_hang/                      # Dữ liệu kết quả dóng hàng song ngữ
│   │   ├── SacTuBachTruongThanhQuy_parallel.tsv          # Kết quả cấp CÂU chuẩn Tab
│   │   ├── SacTuBachTruongThanhQuy_parallel.xlsx         # Kết quả cấp CÂU (Sheet DONG_HANG)
│   │   ├── SacTuBachTruongThanhQuy_parallel_paragraph.xlsx # Bảng đối chiếu cấp ĐOẠN
│   │   ├── q4_parallel.tsv / .xlsx                       # Kết quả riêng Quyển 4
│   │   └── q7_parallel.tsv / .xlsx                       # Kết quả riêng Quyển 7
│   ├── docs/                              # Tài liệu kỹ thuật và báo cáo
│   │   ├── Guideline.pdf                  # Quy chuẩn và tiêu chí nghiệm thu đồ án
│   │   ├── HUONG_DAN.docx                 # Hướng dẫn trích xuất văn bản từ PDF
│   │   ├── Bang_kiem_ke_nguon.xlsx        # Bảng kiểm kê thông tin nguồn
│   │   ├── example_ocr_result.xlsx        # Mẫu định dạng tham khảo
│   │   └── Bao_cao_chat_luong_dong_hang.md# Báo cáo đánh giá chất lượng tự động
│   ├── src/                               # Toàn bộ mã nguồn sản xuất (Production Code)
│   │   ├── vni_converter.py               # Chuyển đổi mã VNI sang Unicode bằng Regex 1 lượt
│   │   ├── extract_clean.py               # Trích xuất PDF, khử rác và lọc lời bàn
│   │   ├── aligner.py                     # Thuật toán tách câu & dóng hàng quy hoạch động (DP)
│   │   ├── evaluate.py                    # Kiểm thử chất lượng và tính tỷ lệ lỗi
│   │   └── run_pipeline.py                # Bộ điều phối thực thi toàn bộ pipeline
│   └── legacy/                            # Lưu trữ tệp script và nháp ban đầu
├── requirements.txt                       # Thư viện phụ thuộc (PyMuPDF, pandas, openpyxl)
├── .gitignore                             # Cấu hình bỏ qua tệp tạm, môi trường ảo
└── README.md                              # Thuyết minh chi tiết dự án
```

---

## 3. Kiến trúc kỹ thuật và giải pháp cốt lõi

### 3.1. Chuyển đổi bảng mã VNI-Windows không ghi đè (`vni_converter.py`)
Áp dụng **Single-pass Regex Tokenization** (`re.compile('|'.join(...))`) để thay thế toàn bộ tổ hợp phím VNI sang ký tự Unicode dựng sẵn trong một lượt duyệt duy nhất. Phương pháp này khắc phục triệt để lỗi ghi đè ký tự tuần tự (sequential overwrite bug), đảm bảo 100% nguyên âm tiếng Việt và dấu thanh hiển thị chính xác.

### 3.2. Tiền xử lý và làm sạch dữ liệu (`extract_clean.py`)
- Khử sạch header/footer, số trang lặp lại theo trang tài liệu.
- Loại bỏ hoàn toàn các đoạn chú thích riêng **LỜI BÀN** của dịch giả không thuộc nguyên tác chữ Hán.
- Hiệu đính các đoạn bị đánh lệch mã số CBETA trong sách (ví dụ `[1134a02]` $\rightarrow$ `[1134a03]`, `[1150b16]` $\rightarrow$ `[1150b17]`).
- Phân biệt chính xác giữa bản **Phiên âm Hán-Việt** và bản **Dịch nghĩa tiếng Việt**, đảm bảo dữ liệu song ngữ phản ánh đúng quan hệ ngữ nghĩa nguyên tác - bản dịch.

### 3.3. Dóng hàng cấp câu bằng Quy hoạch động (`aligner.py`)
- Tách câu Hán theo dấu `。！？` và câu Việt theo `.?!`.
- Tối ưu hóa chuỗi ghép câu bằng thuật toán **Dynamic Programming** dựa trên hàm tương quan độ dài ký tự đặc trưng Hán - Việt ($\approx 4$ ký tự Việt / 1 chữ Hán).
- Hỗ trợ linh hoạt các quan hệ dóng hàng $1-1, 2-1, 3-1, 1-2, 2-2$, bảo toàn câu có cấu trúc hoàn chỉnh và ngữ nghĩa trọn vẹn.

---

## 4. Hướng dẫn cài đặt và vận hành

### 4.1. Cài đặt môi trường
Yêu cầu Python 3.9 trở lên:
```bash
pip install -r requirements.txt
```

### 4.2. Vận hành Pipeline
Chạy toàn bộ quy trình chỉ với 1 câu lệnh:
```bash
python CV09_SacTuBachTruongThanhQuy/src/run_pipeline.py
```
> **Khả năng mở rộng:** Pipeline tự động quét toàn bộ tệp PDF trong `01_nguon/`. Khi bổ sung thêm các quyển mới (ví dụ Quyển 5, Quyển 6...), chỉ cần đặt tệp PDF vào thư mục và chạy lại lệnh trên.

---

## 5. Kết quả đánh giá nghiệm thu

Dữ liệu được kiểm thử tự động bởi module `evaluate.py`:

| Chỉ số kiểm tra | Kết quả đạt được | Ngưỡng nghiệm thu | Đánh giá |
| :--- | :---: | :---: | :---: |
| **Tổng số cặp câu** | **722 cặp** | - | Cấp câu hoàn chỉnh |
| **Số câu hợp lệ đầy đủ** | **722 / 722 câu** | - | Khớp nghĩa 100% |
| **Khuyết vế Hán (Missing Han)** | **0 câu** | 0 | Đã giải quyết hoàn toàn |
| **Khuyết vế Việt (Missing Viet)** | **0 câu** | 0 | Đã giải quyết hoàn toàn |
| **Định dạng TSV** | Chuẩn `<HÁN>\t<VIỆT>` | Bắt buộc | **✓ Đạt chuẩn** |
| **Định dạng Excel** | Sheet `DONG_HANG` (Hán, Việt) | Bắt buộc | **✓ Đạt chuẩn** |
| **Tỷ lệ lỗi (Error Rate)** | **0.0%** | $\le 30\%$ | **✓ ĐẠT NGHIỆM THU TUYỆT ĐỐI** |
