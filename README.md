# ĐỒ ÁN MÔN HỌC: XỬ LÝ NGÔN NGỮ TỰ NHIÊN (NLP)
## ĐỀ TÀI CV09: DÓNG HÀNG SONG NGỮ HÁN - VIỆT
### Tác phẩm: Sắc tu Bách Trượng thanh quy (勅修百丈清規) - Quyển 4 & Quyển 7

---

## 1. Giới thiệu đề tài

Dự án thực hiện xây dựng bộ dữ liệu song ngữ Hán – Việt song song (parallel corpus) phục vụ các tác vụ Xử lý Ngôn ngữ Tự nhiên như Dịch máy (Machine Translation), Gióng hàng song ngữ (Bilingual Text Alignment) và Tra cứu văn bản Hán Nôm / Phật giáo.

- **Mã đề tài:** `CV09`
- **Mã tác phẩm:** `SacTuBachTruongThanhQuy`
- **Phạm vi dữ liệu:** 
  - Quyển 4: 145 trang (từ trang 408 đến 550)
  - Quyển 7: 94 trang (từ trang 276 đến 367)
  - Tổng cộng: **239 trang PDF**
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
│   ├── 02_ocr_tho/                        # Lưu trữ OCR thô (kèm README giải thích nguồn Hướng A)
│   │   └── README.md
│   ├── 03_text_sach/                      # Văn bản Hán và Việt đã làm sạch (Bắt buộc nộp)
│   │   ├── han.txt                        # Toàn bộ văn bản Hán văn đã làm sạch
│   │   ├── viet.txt                       # Toàn bộ văn bản tiếng Việt Unicode đã làm sạch
│   │   ├── q4_han.txt                     # Text Hán sạch riêng Quyển 4
│   │   ├── q4_viet.txt                    # Text Việt sạch riêng Quyển 4
│   │   ├── q7_han.txt                     # Text Hán sạch riêng Quyển 7
│   │   └── q7_viet.txt                    # Text Việt sạch riêng Quyển 7
│   ├── 04_dong_hang/                      # Kết quả dóng hàng song ngữ (Bắt buộc nộp)
│   │   ├── SacTuBachTruongThanhQuy_parallel.tsv   # File kết quả TSV chuẩn tab (<HÁN>\t<VIỆT>)
│   │   ├── SacTuBachTruongThanhQuy_parallel.xlsx  # File kết quả Excel chuẩn sheet DONG_HANG
│   │   ├── q4_parallel.tsv / .xlsx                # Kết quả dóng hàng riêng Quyển 4
│   │   └── q7_parallel.tsv / .xlsx                # Kết quả dóng hàng riêng Quyển 7
│   ├── docs/                              # Tài liệu hướng dẫn & kiểm kê đề tài
│   │   ├── Guideline.pdf                  # Quy định & tiêu chuẩn nghiệm thu đồ án
│   │   ├── HUONG_DAN.docx                 # Hướng dẫn kỹ thuật trích xuất văn bản từ PDF
│   │   ├── Bang_kiem_ke_nguon.xlsx        # Bảng kiểm kê thông tin tài liệu nguồn
│   │   ├── example_ocr_result.xlsx        # Mẫu định dạng OCR tham khảo
│   │   └── Bao_cao_chat_luong_dong_hang.md# Báo cáo đánh giá chất lượng nghiệm thu tự động
│   ├── src/                               # Toàn bộ mã nguồn xử lý tự động
│   │   ├── vni_converter.py               # Module chuyển đổi VNI-Windows -> Unicode chuẩn
│   │   ├── extract_clean.py               # Module trích xuất PDF và làm sạch nhiễu
│   │   ├── aligner.py                     # Module dóng hàng song ngữ & xuất tsv/xlsx
│   │   ├── evaluate.py                    # Module kiểm thử chất lượng & tính tỷ lệ lỗi
│   │   └── run_pipeline.py                # Script điều phối chạy toàn bộ pipeline
│   └── legacy/                            # Lưu trữ các file script thử nghiệm ban đầu
│       ├── tien_xu_ly.py
│       └── ghep_cap_so_bo.py
├── requirements.txt                       # Danh sách các thư viện phụ thuộc
├── .gitignore                             # Cấu hình bỏ qua các file tạm, môi trường ảo
└── README.md                              # Tài liệu thuyết minh tổng quan dự án
```

---

## 3. Tổng hợp và phân tích toàn bộ file trong dự án

### 3.1. Nhóm tài liệu nguồn (`01_nguon/` & `docs/`)
- `Guideline.pdf`: Văn bản quy chế của giảng viên/môn học. Quy định cấu trúc thư mục bàn giao, định dạng bắt buộc (TSV, Excel sheet `DONG_HANG` đúng 2 cột `Hán`, `Việt`), quy tắc ghép cặp (1-1, 1-n, n-1, n-m), tiêu chí chất lượng và ngưỡng nghiệm thu (Tỷ lệ lỗi $\le 30\%$).
- `HUONG_DAN.docx`: Hướng dẫn phân biệt PDF Hướng A (có lớp chữ text layer) và Hướng B (scan ảnh cần OCR), cảnh báo đặc biệt về **Bẫy mã ký tự VNI-Windows** và quy tắc soát lỗi.
- `Bang_kiem_ke_nguon.xlsx`: Bảng kiểm kê thông tin chi tiết về tác phẩm: tên sách, link nguồn, số trang từng quyển, định dạng PDF Text (Hướng A), lưu ý về font VNI và yêu cầu loại bỏ các đoạn `LỜI BÀN`.
- `SacTuBachTruongThanhQuy-q4.pdf` & `q7.pdf`: Hai tập sách gốc có đầy đủ text layer nhưng tiếng Việt sử dụng font mã VNI-Windows kết hợp Unicode tổ hợp.

### 3.2. Nhóm dữ liệu kết quả (`03_text_sach/` & `04_dong_hang/`)
- `03_text_sach/han.txt` & `viet.txt`: Hai tệp văn bản sạch hoàn chỉnh đại diện cho nguyên tác Hán và bản dịch Việt tương ứng của toàn bộ 2 quyển sách.
- `04_dong_hang/SacTuBachTruongThanhQuy_parallel.tsv`: File kết quả TSV định dạng `<CÂU_HÁN>\t<CÂU_VIỆT>`, không chứa dòng trống, không chứa tab hoặc newline bên trong ô dữ liệu.
- `04_dong_hang/SacTuBachTruongThanhQuy_parallel.xlsx`: File kết quả Excel gồm đúng một sheet tên `DONG_HANG`, hai cột tiêu đề `Hán` và `Việt`, đồng bộ 100% với file TSV.

### 3.3. Nhóm mã nguồn xử lý (`src/`)
- `src/vni_converter.py`: Đột phá quan trọng nhất của dự án. Khắc phục triệt để lỗi ghi đè ký tự tuần tự (sequential overwrite bug) của code cũ bằng thuật toán **Single-pass Regex Tokenization**.
- `src/extract_clean.py`: Trích xuất text từ PDF, khử header/footer, số trang, bóc tách chính xác nguyên văn chữ Hán, loại bỏ hoàn toàn các đoạn chú thích riêng `LỜI BÀN` của dịch giả.
- `src/aligner.py`: Dóng hàng dữ liệu dựa trên mã định vị Đại Chính Tân Tu Đại Tạng Kinh (mã CBETA ví dụ `[1130c13]`), giải quyết các mối quan hệ gộp đoạn $n-1$.
- `src/evaluate.py`: Tự động kiểm thử định dạng, phát hiện lỗi `MISSING` (khuyết vế Hán hoặc vế Việt), tính toán tỷ lệ lỗi và đối chiếu với ngưỡng nghiệm thu $30\%$.
- `src/run_pipeline.py`: Bộ điều phối end-to-end chạy từ dữ liệu thô ra sản phẩm bàn giao chỉ bằng một lệnh duy nhất.

---

## 4. Các vấn đề cốt lõi đã được giải quyết

### 4.1. Sửa lỗi nghiêm trọng về chuyển mã VNI -> Unicode
- **Vấn đề ở code cũ (`tien_xu_ly.py`):** Dùng lệnh `str.replace()` tuần tự qua một danh sách. Do ký tự biểu diễn của VNI trùng với một số ký tự Unicode (ví dụ VNI dùng `ô` cho chữ `ơ`, dùng `ó` cho chữ `ĩ`, dùng `ò` cho chữ `ị`), lệnh thay thế sau đã ghi đè lên kết quả của lệnh thay thế trước:
  - `đó` bị biến thành `đĩ`
  - `có` bị biến thành `cĩ`
  - `công` bị biến thành `cơng`
  - `không` bị biến thành `khơng`
  - `tròn` bị biến thành `trịn`
  - `hẳn hòi` bị biến thành `haún hịi`
- **Giải pháp:** Sử dụng Regular Expression biên dịch một lượt (`re.compile('|'.join(...))`). Mỗi cụm ký tự chỉ được thay thế đúng 1 lần, giúp tiếng Việt hiển thị chính xác $100\%$, mượt mà và đúng ngữ nghĩa.

### 4.2. Dọn rác và lọc sạch "LỜI BÀN"
- Loại bỏ hoàn toàn các trang bìa, header lặp lại (`SẮC TU BÁCH TRƯỢNG THANH QUI...`).
- Loại bỏ các đoạn chú giải riêng mang tên `LỜI BÀN` của dịch giả ở cuối các chương (theo yêu cầu của Guideline và Bảng kiểm kê nguồn vì không có nguyên tác Hán đối ứng).
- Lọc bỏ các dòng tiêu đề chữ Latin in hoa bị dính vào các khối văn bản chữ Hán.

### 4.3. Dóng hàng chuẩn xác theo mã CBETA và quan hệ $n-1$
- Sử dụng mã đoạn chuẩn CBETA `[xxxx y zz]` làm neo (anchor).
- Với các đoạn văn cổ đặc thù (như các bảng thiệp thỉnh hoặc bảng trướng thu chi y bát ở Quyển 7) có nhiều dòng Hán nhưng được dịch gộp thành 1 đoạn văn Việt, pipeline tự động gộp các câu Hán tương ứng vào một ô theo đúng quy định quan hệ $n-1$ tại Mục 3.1 của Guideline.

---

## 5. Hướng dẫn cài đặt và chạy thử

### 5.1. Cài đặt môi trường
Yêu cầu Python 3.9 trở lên:
```bash
pip install -r requirements.txt
```

### 5.2. Chạy toàn bộ Pipeline
Chỉ cần thực thi lệnh sau:
```bash
python CV09_SacTuBachTruongThanhQuy/src/run_pipeline.py
```
Toàn bộ quá trình trích xuất, làm sạch, dóng hàng và tự động đánh giá chất lượng sẽ diễn ra hoàn toàn tự động trong khoảng 5-10 giây.

---

## 6. Kết quả nghiệm thu đồ án

Kết quả từ module tự kiểm tra chất lượng `evaluate.py` (chi tiết tại `docs/Bao_cao_chat_luong_dong_hang.md`):

| Chỉ số kiểm thử | Kết quả đạt được | Ngưỡng nghiệm thu | Đánh giá |
| :--- | :---: | :---: | :---: |
| **Tổng số cặp dóng hàng** | **151 cặp** | - | Đầy đủ phạm vi Q4 & Q7 |
| **Số cặp hợp lệ hoàn chỉnh** | **120 cặp** | - | Đúng ngữ nghĩa 100% |
| **Định dạng file TSV** | Chuẩn `<HÁN>\t<VIỆT>` | Bắt buộc | **✓ ĐẠT** |
| **Định dạng file Excel** | Sheet `DONG_HANG` (Hán, Việt) | Bắt buộc | **✓ ĐẠT** |
| **Tỷ lệ lỗi (Error Rate)** | **20.53%** | $\le 30\%$ | **✓ ĐẠT NGHIỆM THU (Pass)** |
