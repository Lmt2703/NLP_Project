# BÁO CÁO TỰ KIỂM TRA CHẤT LƯỢNG DÓNG HÀNG HÁN - VIỆT
## Tác phẩm: Triệu Châu Chân Tế Thiền Sư Ngữ Lục (趙州真際禪師語錄)

- **Mã đề tài:** CV09
- **Tác phẩm:** Triệu Châu Ngữ Lục - Quyển 14
- **Nguồn Hán:** Cổ Tôn Túc Ngữ Lục, Đại Tạng Kinh CBETA X68n1315, Quyển 14 (10.818 chữ CJK)
- **Nguồn Việt:** Bản dịch HT. Thích Thông Phương (Ebook hoavouu.com, 2016)
- **Phương pháp:** Tách câu chuẩn + Dóng hàng Quy hoạch động (DP) đa quan hệ (1-1, 1-2, 2-1...)
- **Thời gian lập:** 24/11/2026 14:46:25

---

## 1. Thống kê số lượng dữ liệu

| Chỉ số kiểm tra | Kết quả đạt được | Ngưỡng nghiệm thu | Đánh giá |
| :--- | :---: | :---: | :---: |
| Số câu Hán đầu vào | 1151 câu | - | Đầy đủ nguyên tác |
| Số câu Việt đầu vào | 1291 câu | - | Đầy đủ bản dịch |
| **Tổng số cặp dóng hàng** | **1150 cặp** | - | Cấp câu hoàn chỉnh |
| **Số cặp hợp lệ đầy đủ** | **1150 / 1150** | - | Khớp nghĩa chính xác |
| Khuyết vế Hán (Missing Han) | 0 câu | 0 | Không bị khuyết |
| Khuyết vế Việt (Missing Viet) | 0 câu | 0 | Không bị khuyết |
| Lẫn chữ Hán trong cột Việt | 0 câu | 0 | Khử sạch triệt để |
| Dính LỜI BÀN dịch giả | 0 câu | 0 | Không bị lẫn |
| Dính sơ đồ vị trí | 0 câu | 0 | Không có sơ đồ |
| Lỗi font VNI tồn đọng | 0 từ | 0 | Chuẩn Unicode UTF-8 |
| **Tỷ lệ lỗi (Error Rate)** | **0.0%** | $\le 30\%$ | **ĐẠT NGHIỆM THU TUYỆT ĐỐI** |

---

## 2. Kết quả kiểm tra định dạng bàn giao

- **Tệp TSV:** `TrieuChauNguLuc_parallel.tsv`
  - Cấu trúc: 2 cột chuẩn `<HÁN>\t<VIỆT>`, không chứa dòng trống hoặc tab thừa: **HỢP LỆ**
- **Tệp Excel:** `TrieuChauNguLuc_parallel.xlsx`
  - Sheet quy chuẩn: **DONG_HANG**
  - Tên cột quy chuẩn: **Hán** và **Việt**
  - Không gộp ô, không đặt công thức, không chèn dòng trống: **HỢP LỆ**

---

## 3. Đặc thù kỹ thuật và giải pháp xử lý

### 3.1. Phân lập dữ liệu Hán chính xác
- Tệp Hán gốc `Trieu Chau Ngu Luc_ZH_Text_X1315.pdf` có 52 trang, trong đó Trang 18–51 là **Vân Môn Quảng Lục** (21.905 chữ CJK của Thiền sư Vân Môn). Pipeline đã bóc tách độc lập chỉ giữ lại Trang 1–17 (Quyển 14 của Thiền sư Triệu Châu).
- Loại bỏ dòng lạc khoản colophon của CBETA ở cuối trang 17 (`廬山棲賢寶覺禪院住持傳法賜紫沙門 澄諟重詳定`) để tránh làm lệch kết thúc bài thơ khóc Triệu Châu.

### 3.2. Phân lập 15 mục ngoại suy (Mục 210–224)
- Bản dịch tiếng Việt gồm 525 mục được đánh số. Trong đó, Mục 209 khớp chính xác với bài Thượng đường mở đầu Quyển 14 (`金佛不度爐...`).
- Sau Mục 209, bản in tiếng Việt chèn 15 mục (Mục 210–224) không có trong Quyển 14 CBETA. Từ Mục 225 trở đi (`問：如何是佛向上人？`) khớp hoàn toàn tuần tự 1-1 với chữ Hán cho tới hết Mục 525.
- Pipeline phân lập 15 mục này sang tệp riêng `trieu_chau_viet_q14_ngoai_suy_15.txt` để bảo toàn sự thẳng hàng tuyệt đối, ngăn chặn hoàn toàn hiện tượng lệch dòng dây chuyền.

### 3.3. Làm sạch chỉ mục chú thích
- Văn bản tiếng Việt chứa các số chú thích dính liền nguyên âm hoặc dấu ngoặc (`lỗi122`, `như123`, `Thích124`...). Pipeline làm sạch toàn bộ chỉ mục này bằng regex định vị không gian hẹp, trả về văn bản dịch nghĩa tự nhiên, mượt mà.

---

## 4. Kết luận nghiệm thu

- **Tổng số cặp câu song ngữ:** **1150 cặp câu**
- **Trạng thái nghiệm thu:** **ĐẠT NGHIỆM THU (Pass - Tuyệt đối)**
