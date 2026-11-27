# ĐỒ ÁN XỬ LÝ NGÔN NGỮ TỰ NHIÊN (NLP)
## ĐỀ TÀI CV09: DÓNG HÀNG SONG NGỮ HÁN - VIỆT
### Tác phẩm: Sắc tu Bách Trượng thanh quy, Triệu Châu Ngữ Lục & Giải Thoát Đạo Luận

---

## 1. Giới thiệu tổng quan

Dự án xây dựng ngữ liệu song ngữ song song (parallel corpus) Hán – Việt phục vụ nghiên cứu và ứng dụng trong các bài toán Xử lý Ngôn ngữ Tự nhiên:
- Huấn luyện mô hình Dịch máy (Neural Machine Translation).
- Dóng hàng câu song ngữ tự động (Bilingual Sentence Alignment).
- Tra cứu và đối chiếu tư liệu Hán Nôm / Phật học cổ điển.

### Thông tin đề tài:
- **Mã đề tài:** `CV09`
- **Mã tác phẩm chính:** `SacTuBachTruongThanhQuy`
- **Các tác phẩm mở rộng:**
  - `TrieuChauNguLuc` (Triệu Châu Chân Tế Thiền Sư Ngữ Lục)
  - `GiaiThoatDaoLuan` (Giải Thoát Đạo Luận – Vimuttimagga)
- **Dữ liệu nguồn:** 
  1. *Sắc tu Bách Trượng thanh quy:* Quyển 4 (144 trang) & Quyển 7 (94 trang) = 238 trang PDF (In-file song ngữ).
  2. *Triệu Châu Ngữ Lục:* Bản dịch tiếng Việt (134 trang) & Bản Hán CBETA X68n1315 (52 trang) (Cross-file độc lập).
  3. *Giải Thoát Đạo Luận:* Bản dịch tiếng Việt HT. Thích Như Điển (341 trang) & Bản Hán CBETA T32n1648 (117 trang), trọn bộ 12 Quyển / 12 Phẩm (Cross-file độc lập).

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
│   │   ├── Trieu Chau Ngu Luc_ZH_Text_X1315.pdf           # Bản Hán CBETA Triệu Châu & Vân Môn
│   │   ├── Giai Thoat Dao Luan_VI_Text_NhuDien.pdf        # Bản dịch tiếng Việt Giải Thoát Đạo Luận (12 quyển)
│   │   └── Giai Thoat Dao Luan_ZH_Text_T1648.pdf          # Bản Hán CBETA T32n1648 Giải Thoát Đạo Luận (12 quyển)
│   ├── 02_ocr_tho/                        # Thuyết minh nguồn Hướng A (PDF Text)
│   │   └── README.md
│   ├── 03_text_sach/                      # Văn bản Hán và Việt đã làm sạch
│   │   ├── han.txt / viet.txt             # Toàn văn sạch tổng hợp cả 4 quyển (6.886 câu)
│   │   ├── bach_truong/                   # Sắc tu Bách Trượng thanh quy (Q4 & Q7)
│   │   │   ├── q4_han.txt / q4_viet.txt   # Riêng Quyển 4 (482 câu)
│   │   │   ├── q7_han.txt / q7_viet.txt   # Riêng Quyển 7 (404 câu)
│   │   │   └── bach_truong_han.txt / _viet.txt # Gộp Q4 & Q7 (886 câu)
│   │   ├── trieu_chau/                    # Triệu Châu Ngữ Lục (Q14)
│   │   │   └── trieu_chau_han.txt / _viet.txt  # 1.039 câu Hán & Việt sạch
│   │   └── giai_thoat_dao_luan/           # Giải Thoát Đạo Luận (12 Quyển)
│   │       └── giai_thoat_dao_luan_han.txt / _viet.txt # 4.961 câu Hán & Việt sạch
│   ├── 04_dong_hang/                      # Dữ liệu kết quả dóng hàng song ngữ chuẩn TSV & Excel
│   │   ├── CV09_TongHop_parallel.tsv / .xlsx              # Ngữ liệu tổng hợp cả 4 quyển (6.886 cặp câu)
│   │   ├── q4_parallel.* / q7_parallel.*                  # Riêng Quyển 4 (482) & Quyển 7 (404) Bách Trượng
│   │   ├── SacTuBachTruongThanhQuy_parallel.tsv / .xlsx   # Gộp Bách Trượng Q4+Q7 (886 cặp câu)
│   │   ├── TrieuChauNguLuc_parallel.tsv / .xlsx           # Kết quả Triệu Châu Q14 (1.039 cặp câu)
│   │   └── GiaiThoatDaoLuan_parallel.tsv / .xlsx          # Kết quả Giải Thoát Đạo Luận 12Q (4.961 cặp câu)
│   ├── docs/                              # Báo cáo kiểm kê nguồn, chất lượng và kiểm định chéo Bertalign
│   │   ├── Bang_kiem_ke_nguon.xlsx        # Bảng kiểm kê nguồn Excel (4 quyển / 3 tác phẩm)
│   │   ├── Bang_kiem_ke_nguon.md          # Báo cáo kiểm kê nguồn chi tiết (Markdown)
│   │   ├── Bao_cao_chat_luong_dong_hang.md# Báo cáo hợp nhất kiểm định chất lượng cả 4 quyển
│   │   ├── Bertalign_LaBSE_Audit.xlsx     # Kết quả chấm điểm tương đồng ngữ nghĩa LaBSE (6.886 cặp)
│   │   └── Bertalign_Realign_Diff.xlsx    # Kết quả dóng hàng kiểm định chéo độc lập bằng Bertalign
│   └── src/                               # Toàn bộ mã nguồn tái lập quy trình
│       ├── vni_converter.py               # Bộ giải mã bảng mã VNI sang Unicode không ghi đè
│       ├── extract_clean.py               # Trích xuất và khử nhiễu sách Bách Trượng
│       ├── extract_trieu_chau.py          # Trích xuất cấu trúc hóa sách Triệu Châu
│       ├── extract_giai_thoat_dao_luan.py # Trích xuất, sửa CMap & Drop-Cap Giải Thoát Đạo Luận
│       ├── aligner.py                     # Thuật toán tách câu & dóng hàng quy hoạch động (DP)
│       ├── evaluate.py                    # Kiểm thử chất lượng và tính tỷ lệ lỗi tự động
│       ├── trieu_chau_refiner.py          # Tinh chỉnh ranh giới công án Triệu Châu
│       ├── giai_thoat_dao_luan_refiner.py # Tinh chỉnh 4 tầng & vệ sinh văn bản Giải Thoát Đạo Luận
│       ├── run_pipeline.py                # Pipeline điều phối cho Bách Trượng (Q4 & Q7)
│       ├── run_pipeline_trieu_chau.py     # Pipeline điều phối chuyên trách cho Triệu Châu (Q14)
│       ├── run_pipeline_giai_thoat_dao_luan.py # Pipeline điều phối chuyên trách cho Giải Thoát Đạo Luận
│       └── build_master_corpus.py         # Hợp nhất 4 quyển và xuất 1 báo cáo tổng hợp duy nhất
├── CV09_Bertalign_Verification.ipynb      # Notebook Colab (GPU T4) kiểm định chéo bằng Bertalign & LaBSE
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

- **Sách Giải Thoát Đạo Luận (`extract_giai_thoat_dao_luan.py`, `run_pipeline_giai_thoat_dao_luan.py`):**
  - Sửa lỗi CMap cấp span cho chữ `ẩ` (`TTFFAC6368t00`: `'N'` 60 lần; `TTFFAC7490t00`: `'\x0f'` 19 lần) và khôi phục tự động toàn bộ 19 chữ cái lớn Drop-Cap mở đầu chương theo tọa độ `y`.
  - Lọc sạch 111 số trang CBETA, 11 trang bìa quyển phụ lục ngày dịch, trang hồi hướng, danh sách ấn tống và trang quảng bá CBETA; cấu trúc hóa thành **19 phân đoạn đồng bộ 1-1** trên toàn bộ 12 Quyển.
  - Dóng hàng Quy hoạch động tối ưu bitmask với dải băng rộng, bước chuyển động linh hoạt đến `1-36` cho các câu Hán liệt kê dài, kết hợp nhận diện vai trò `問/答` $\leftrightarrow$ `Hỏi/Đáp`, 220+ mỏ neo A-tỳ-đạt-ma và mỏ neo con số.

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
- **Chạy pipeline Giải Thoát Đạo Luận:**
  ```bash
  python CV09_SacTuBachTruongThanhQuy/src/run_pipeline_giai_thoat_dao_luan.py
  ```
- **Hợp nhất cả 4 quyển và sinh báo cáo tổng hợp (`Bao_cao_chat_luong_dong_hang.md`):**
  ```bash
  python CV09_SacTuBachTruongThanhQuy/src/build_master_corpus.py
  ```

---

## 5. Kết quả đánh giá nghiệm thu tổng hợp cả 4 quyển

Toàn bộ dữ liệu được kiểm thử tự động bởi module [evaluate.py](file:///d:/3rd/NLP/CV09/NLP_Project/CV09_SacTuBachTruongThanhQuy/src/evaluate.py) và tổng hợp trong báo cáo duy nhất [Bao_cao_chat_luong_dong_hang.md](file:///d:/3rd/NLP/CV09/NLP_Project/CV09_SacTuBachTruongThanhQuy/docs/Bao_cao_chat_luong_dong_hang.md):

| Chỉ số kiểm tra | Bách Trượng Q4 | Bách Trượng Q7 | Triệu Châu Q14 | Giải Thoát Đạo Luận (12Q) | TỔNG CỘNG (4 QUYỂN) | Đánh giá |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tổng số cặp câu song ngữ** | **482 cặp** | **404 cặp** | **1.039 cặp** | **4.961 cặp** | **6.886 cặp câu** | Cấp câu hoàn chỉnh |
| **Số cặp hợp lệ** | **482 / 482** | **404 / 404** | **1.039 / 1.039** | **4.961 / 4.961** | **6.886 / 6.886** | Hợp lệ định dạng 100% |
| **Khuyết vế Hán / Việt** | **0 / 0** | **0 / 0** | **0 / 0** | **0 / 0** | **0 / 0** | Đạt chuẩn |
| **Lẫn chữ Hán trong vế Việt** | **0** | **0** | **0** | **0** | **0** | Đạt chuẩn |
| **Lỗi font VNI / CMap tồn đọng** | **0** | **0** | **0** | **0** | **0** | Đạt chuẩn |
| **Chuẩn định dạng TSV & Excel** | ✓ Hợp lệ | ✓ Hợp lệ | ✓ Hợp lệ | ✓ Hợp lệ | ✓ `CV09_TongHop_parallel.*` | **✓ Đạt chuẩn** |
| **Tỷ lệ lỗi cấu trúc (`evaluate.py`)** | **0.0%** | **0.0%** | **0.0%** | **0.0%** | **0.0%** ($\le 30\%$) | **✓ ĐẠT NGHIỆM THU** |
| **Đồng thuận 1–1 độc lập (Bertalign)** | **67.22%** *(324)* | **75.50%** *(305)* | **98.85%** *(1.027)* | **93.41%** *(4.634)* | **91.34%** *(6.290/6.886)* | Sai số ngữ nghĩa tồn dư ~0.3%–0.4% |
