# ĐỒ ÁN MÔN HỌC: XỬ LÝ NGÔN NGỮ TỰ NHIÊN (NLP)
## ĐỀ TÀI CV09: DÓNG HÀNG SONG NGỮ HÁN - VIỆT (CẤP CÂU & ĐOẠN)
### Tác phẩm: Sắc tu Bách Trượng thanh quy (勅修百丈清規) - Quyển 4 & Quyển 7

---

## 1. Giới thiệu đề tài

Dự án thực hiện xây dựng bộ dữ liệu song ngữ Hán – Việt song song (parallel corpus) phục vụ các tác vụ Xử lý Ngôn ngữ Tự nhiên như Dịch máy (Machine Translation), Gióng hàng song ngữ (Bilingual Sentence Alignment) và Tra cứu văn bản Hán Nôm / Phật giáo.

- **Mã đề tài:** `CV09`
- **Mã tác phẩm:** `SacTuBachTruongThanhQuy`
- **Phạm vi dữ liệu hiện tại:** 
  - Quyển 4: 145 trang (từ trang 408 đến 550)
  - Quyển 7: 94 trang (từ trang 276 đến 367)
  - Tổng cộng: **239 trang PDF** (dễ dàng mở rộng thêm Quyển 1, 2, 3, 5, 6... qua Pipeline)
- **Định dạng nguồn:** PDF Text (có sẵn lớp text layer - Hướng A).

---

## 2. Cấu trúc thư mục dự án

Toàn bộ dự án được tổ chức và cấu trúc lại theo đúng chuẩn quy định trong tài liệu **Hướng dẫn thực hiện đồ án (Guideline.pdf)**:

```text
NLP_Project/
├── CV09_SacTuBachTruongThanhQuy/          # Thư mục sản phẩm bàn giao chính thức (<MA_DE_TAI>_<MA_TAC_PHAM>)
│   ├── 01_nguon/                          # Tài liệu gốc
│   │   ├── SacTuBachTruongThanhQuy-q4.pdf # File PDF nguồn Quyển 4 (145 trang)
│   │   └── SacTuBachTruongThanhQuy-q7.pdf # File PDF nguồn Quyển 7 (94 trang)
│   ├── 02_ocr_tho/                        # Thư mục chuẩn bàn giao
│   │   └── README.md                      # Ghi chú nguồn Hướng A (PDF Text trích xuất trực tiếp)
│   ├── 03_text_sach/                      # Văn bản Hán và Việt đã làm sạch (Bắt buộc nộp)
│   │   ├── han.txt                        # Toàn bộ 722 câu Hán văn đã làm sạch
│   │   ├── viet.txt                       # Toàn bộ 722 câu tiếng Việt Unicode đã làm sạch
│   │   ├── q4_han.txt / q4_viet.txt       # Text sạch riêng Quyển 4 (388 câu)
│   │   └── q7_han.txt / q7_viet.txt       # Text sạch riêng Quyển 7 (334 câu)
│   ├── 04_dong_hang/                      # Kết quả dóng hàng song ngữ (Bắt buộc nộp)
│   │   ├── SacTuBachTruongThanhQuy_parallel.tsv          # Bàn giao chính thức CẤP CÂU (722 cặp câu)
│   │   ├── SacTuBachTruongThanhQuy_parallel.xlsx         # Bàn giao chính thức CẤP CÂU (Sheet DONG_HANG)
│   │   ├── SacTuBachTruongThanhQuy_parallel_paragraph.xlsx # Bảng dóng hàng đối chiếu CẤP ĐOẠN (142 cặp đoạn)
│   │   ├── q4_parallel.tsv / .xlsx                       # Kết quả dóng hàng riêng Quyển 4
│   │   └── q7_parallel.tsv / .xlsx                       # Kết quả dóng hàng riêng Quyển 7
│   ├── docs/                              # Tài liệu hướng dẫn & kiểm kê đề tài
│   │   ├── Guideline.pdf                  # Quy định & tiêu chuẩn nghiệm thu đồ án
│   │   ├── HUONG_DAN.docx                 # Hướng dẫn kỹ thuật trích xuất văn bản từ PDF
│   │   ├── Bang_kiem_ke_nguon.xlsx        # Bảng kiểm kê thông tin tài liệu nguồn
│   │   ├── example_ocr_result.xlsx        # Mẫu định dạng OCR tham khảo
│   │   └── Bao_cao_chat_luong_dong_hang.md# Báo cáo đánh giá chất lượng nghiệm thu tự động
│   ├── src/                               # Toàn bộ mã nguồn xử lý tự động
│   │   ├── vni_converter.py               # Chuyển đổi VNI-Windows -> Unicode bằng Regex 1 lượt
│   │   ├── extract_clean.py               # Trích xuất PDF, khử rác, lọc bỏ 'LỜI BÀN', sửa lệch mã
│   │   ├── aligner.py                     # Thuật toán tách câu & dóng hàng quy hoạch động (DP)
│   │   ├── evaluate.py                    # Module kiểm thử chất lượng & tính tỷ lệ lỗi
│   │   └── run_pipeline.py                # Script điều phối chạy toàn bộ pipeline
│   └── legacy/                            # Lưu trữ an toàn các file code và nháp cũ
├── requirements.txt                       # Khai báo các thư viện phụ thuộc
├── .gitignore                             # Cấu hình bỏ qua các file tạm, môi trường ảo
└── README.md                              # Tài liệu thuyết minh toàn diện dự án
```

---

## 3. Các cải tiến kỹ thuật theo nhận xét của người hướng dẫn

### 3.1. Tách câu hoàn chỉnh và trọn vẹn ngữ nghĩa (Sentence-level Alignment)
- **Phương pháp:** Tách câu Hán theo dấu `。！？` và câu Việt theo `.?!`.
- **Không cắt cơ học:** Ứng dụng quy hoạch động **Dynamic Programming (Gale-Church cải tiến)** dựa trên tỷ lệ độ dài ngữ nghĩa Hán - Việt. Tự động nhận diện các quan hệ $1-1, 2-1, 3-1, 1-2, 2-2$ để câu ghép đôi luôn giữ trọn ý nghĩa, không bị đứt đoạn hay lệch dòng.
- **Tăng vọt số lượng:** Số lượng cặp song ngữ tăng từ **112 cặp đoạn** ban đầu lên **722 cặp câu hoàn chỉnh** (tăng hơn 6.5 lần).

### 3.2. Sửa lỗi lệch mã và trích lọc đối chiếu theo mã đoạn
- **Xử lý các đoạn sách để sai mã:**
  - Tự động map vế Việt `[1134a02]` với cụm Hán `[1134a03] - [1134a05]` (thiệp thỉnh Tân Thủ tọa).
  - Tự động map vế Việt `[1150b16]` với cụm Hán `[1150b17] - [1150b22]` (bản thông báo giới lạp trước ngày nhập hạ).
  - Khắc phục logic phân loại khối: Phân biệt chính xác giữa bản **Phiên âm Hán-Việt** và bản **Dịch nghĩa tiếng Việt**, đảm bảo 100% cột Việt là bản dịch nghĩa chuẩn xác.

### 3.3. Pipeline 1 chạm (One-click Pipeline Runner)
- Toàn bộ quy trình chỉ cần chạy đúng **1 lệnh**:
  ```bash
  python CV09_SacTuBachTruongThanhQuy/src/run_pipeline.py
  ```
- Script tự động quét tất cả các file PDF có trong thư mục `01_nguon/`. Khi bạn cần thêm Quyển 5, Quyển 6... chỉ cần thả file PDF vào `01_nguon/` và chạy lại lệnh trên, dữ liệu sẽ tự động cộng dồn và xuất ra file hoàn chỉnh.

---

## 4. Kết quả nghiệm thu đồ án

Kết quả từ module tự kiểm tra chất lượng `evaluate.py` (chi tiết tại `docs/Bao_cao_chat_luong_dong_hang.md`):

| Chỉ số kiểm thử | Kết quả đạt được | Ngưỡng nghiệm thu | Đánh giá |
| :--- | :---: | :---: | :---: |
| **Tổng số cặp câu dóng hàng** | **722 cặp** | - | Tăng từ 112 lên 722 câu |
| **Số cặp câu hợp lệ hoàn chỉnh** | **722 cặp** | - | Đầy đủ cả 2 vế Hán - Việt |
| **Khuyết vế Hán (Missing Han)** | **0 cặp** | 0 | Đã sửa sạch toàn bộ |
| **Khuyết vế Việt (Missing Viet)** | **0 cặp** | 0 | Đã sửa sạch toàn bộ |
| **Định dạng file TSV** | Chuẩn `<HÁN>\t<VIỆT>` | Bắt buộc | **✓ ĐẠT** |
| **Định dạng file Excel** | Sheet `DONG_HANG` (Hán, Việt) | Bắt buộc | **✓ ĐẠT** |
| **Tỷ lệ lỗi (Error Rate)** | **0.0%** | $\le 30\%$ | **✓ ĐẠT NGHIỆM THU TUYỆT ĐỐI** |
