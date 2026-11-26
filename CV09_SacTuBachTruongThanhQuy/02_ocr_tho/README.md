# 02_ocr_tho

Theo tài liệu **Hướng dẫn thực hiện đồ án (`Guideline.pdf`)** và **Bảng kiểm kê nguồn (`Bang_kiem_ke_nguon.md` / `.xlsx`)**:

- Toàn bộ **6 tệp PDF nguồn** thuộc **4 quyển/bộ sách** của đề tài `CV09` đều có định dạng **PDF Text** (có sẵn lớp chữ kỹ thuật số – **Hướng A**):
  1. **Sắc tu Bách Trượng thanh quy – Quyển 4:** `SacTuBachTruongThanhQuy-q4.pdf` (144 trang, song ngữ Hán–Việt in-file, font Việt VNI-Times).
  2. **Sắc tu Bách Trượng thanh quy – Quyển 7:** `SacTuBachTruongThanhQuy-q7.pdf` (94 trang, song ngữ Hán–Việt in-file, font Việt VNI-Times).
  3. **Triệu Châu Chân Tế Thiền Sư Ngữ Lục – Quyển 14:** `Trieu Chau Ngu Luc_VI_Text_ThongPhuong (1).pdf` (134 trang) & `Trieu Chau Ngu Luc_ZH_Text_X1315.pdf` (52 trang, CBETA `X68n1315`).
  4. **Giải Thoát Đạo Luận (12 Quyển / 12 Phẩm):** `Giai Thoat Dao Luan_VI_Text_NhuDien.pdf` (341 trang) & `Giai Thoat Dao Luan_ZH_Text_T1648.pdf` (117 trang, CBETA `T32n1648`).
- Toàn bộ văn bản chữ Hán và tiếng Việt được trích xuất trực tiếp từ lớp text PDF bằng thư viện **PyMuPDF (`pymupdf`)** ở cấp span (kết hợp giải mã bảng mã VNI-Times, sửa lỗi CMap chữ `ẩ` và ghép nối 19 chữ cái lớn Drop-Cap), không cần qua bước OCR từ ảnh scan (**Hướng B**).
- Thư mục `02_ocr_tho/` được giữ lại để đảm bảo tuân thủ đầy đủ cấu trúc cây thư mục chuẩn bàn giao của đồ án.
