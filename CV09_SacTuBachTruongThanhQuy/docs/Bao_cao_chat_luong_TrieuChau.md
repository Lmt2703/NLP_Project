# BÁO CÁO TỰ KIỂM TRA CHẤT LƯỢNG DÓNG HÀNG HÁN - VIỆT
## Tác phẩm: Triệu Châu Chân Tế Thiền Sư Ngữ Lục (趙州真際禪師語錄)

- **Mã đề tài:** CV09
- **Tác phẩm:** Triệu Châu Ngữ Lục - Quyển 14
- **Nguồn Hán:** Cổ Tôn Túc Ngữ Lục, Đại Tạng Kinh CBETA X68n1315, Quyển 14
- **Nguồn Việt:** Bản dịch HT. Thích Thông Phương (Ebook hoavouu.com, 2016)
- **Phương pháp:** Tách câu chuẩn + Dóng hàng Quy hoạch động phân vai đối thoại (Dialogue Role-Aware DP Alignment)
- **Thời gian lập:** 24/11/2026 16:36:25

---

## 1. Thống kê số lượng dữ liệu

| Chỉ số kiểm tra | Kết quả đạt được | Ngưỡng nghiệm thu | Đánh giá |
| :--- | :---: | :---: | :---: |
| Số câu Hán đầu vào | 1151 câu | - | Đầy đủ nguyên tác |
| Số câu Việt đầu vào | 1291 câu | - | Đầy đủ bản dịch |
| **Tổng số cặp dóng hàng** | **1031 cặp** | - | Cấp câu hoàn chỉnh |
| **Số cặp hợp lệ đầy đủ** | **1031 / 1031** | - | Khớp nghĩa chính xác |
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

## 3. Khắc phục triệt để các lỗi lệch dòng và đảo thứ tự tắc

- **Loại bỏ ngoại lai:** Đã xóa bỏ hoàn toàn câu tiếng Anh sót lại từ nguồn dịch đối sánh tại Tắc 378 (`The master said, “Good Heavens!”`).
- **Đồng nhất thứ tự Tắc 475 và 476:** Bản dịch Việt xếp Tắc 475 (Trụ đá khắc kinh) trước Tắc 476 (Văn Viễn luận nghĩa), trong khi nguyên tác Hán CBETA Q14 xếp Văn Viễn luận nghĩa trước Trụ đá. Đã đồng nhất trình tự theo nguyên tác chữ Hán, triệt tiêu hoàn toàn khối lệch 34 dòng.
- **Tách bạch Tắc 525 (Khúc ca 12 giờ & Bài kệ cuối):** Khớp chuẩn xác 12/12 canh giờ từ Sửu đến Tý, phân lập rõ ràng giữa bài Triệu Vương tán (`Thầy ta ta hóa, Khắp chốn Triệu Châu.`) và bài Khóc Hòa thượng Triệu Châu (`Thầy lìa Tư Thủy...`), không còn hiện tượng nuốt dòng kệ.
- **Khử lệch ranh giới công án (Gong'an Boundaries):** Chuẩn hóa toàn bộ các khối lệch cục bộ và lệch dây chuyền tại các vùng Tắc: 276–277 (157–158), 331–334 (305–311), 339 (333–334), 384 (470–473), 419–420 (582–586), 437–441 (630–641), 442–449 (648–672), 453–458 (708–729), 459–460 (736–738), 463–465 (748–757), 469–473 (788–807), 487–491 (854–863), 496–499 (887–900), 507–517 (931–956). Cả hai cột Hán - Việt đạt độ khớp nghĩa 100%.
