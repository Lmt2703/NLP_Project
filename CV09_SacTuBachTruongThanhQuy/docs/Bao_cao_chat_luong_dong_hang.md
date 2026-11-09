# BÁO CÁO TỰ KIỂM TRA CHẤT LƯỢNG DÓNG HÀNG HÁN - VIỆT

- **Mã đề tài:** CV09
- **Tên tác phẩm:** Sắc tu Bách Trượng thanh quy (勅修百丈清規)
- **Phạm vi:** Quyển 4 (145 trang) và Quyển 7 (94 trang)
- **Ngày lập:** 09/11/2026 22:39:49

---

## 1. Thống kê số lượng dữ liệu

| Hạng mục | Quyển 4 | Quyển 7 | Toàn bộ tác phẩm |
| :--- | :---: | :---: | :---: |
| Số trang tài liệu nguồn (PDF) | 145 | 94 | 239 trang |
| Số khối văn bản trích xuất (Mã CBETA) | 66 | 117 | 183 |
| Số cặp dóng hàng hợp lệ | 54 | 66 | 120 |
| Tổng số dòng trong file dóng hàng | 60 | 91 | 151 |

---

## 2. Kết quả kiểm tra định dạng bàn giao

- **File TSV:** `SacTuBachTruongThanhQuy_parallel.tsv`
  - Chuẩn tab (`<CÂU_HÁN>\t<CÂU_VIỆT>`): **HỢP LỆ**
  - Không có newline/tab thừa trong ô: **HỢP LỆ**
- **File Excel:** `SacTuBachTruongThanhQuy_parallel.xlsx`
  - Tên Sheet bắt buộc: **DONG_HANG**
  - Số cột bắt buộc: đúng 2 cột **Hán** và **Việt**
  - Không gộp ô, không chèn dòng trống: **HỢP LỆ**

---

## 3. Phân loại lỗi và tỷ lệ nghiệm thu

- **Lỗi MISSING (khuyết vế Hán):** 31 cặp
- **Lỗi MISSING (khuyết vế Việt):** 0 cặp
- **Tổng số lỗi phát hiện:** 31 cặp
- **Tỷ lệ lỗi:** **20.53%**
- **Ngưỡng nghiệm thu tối đa theo Guideline:** **30%** (Mục tiêu nội bộ <= 20%)
- **Kết luận:** **ĐẠT NGHIỆM THU (Pass)**

---

## 4. Công cụ và quy trình kỹ thuật đã áp dụng

1. **Trích xuất văn bản:** Sử dụng PyMuPDF (`fitz`) đọc trực tiếp lớp chữ số (text layer) của tài liệu PDF.
2. **Khắc phục triệt để lỗi font VNI:** Xây dựng module `vni_converter.py` với bảng ánh xạ VNI-Windows -> Unicode đầy đủ, sử dụng thuật toán **Single-pass Regex Tokenization** để loại bỏ hoàn toàn lỗi ghi đè ký tự tuần tự (đã giải quyết dứt điểm các lỗi trước đây như: `đĩ` -> `đó`, `cơng` -> `công`, `trịn` -> `tròn`, `haún hịi` -> `hẳn hòi`).
3. **Làm sạch nhiễu (Denoising):**
   - Loại bỏ số trang, đầu trang (header), chân trang (footer).
   - Loại bỏ 100% các đoạn chú thích riêng **LỜI BÀN** của dịch giả không thuộc nguyên tác Hán.
   - Loại bỏ các dòng tiêu đề Latin dính kèm trong khối chữ Hán.
4. **Dóng hàng tự động (Alignment):** Sử dụng mã định vị chuẩn Đại Chính Tân Tu Đại Tạng Kinh (CBETA) làm neo neo đoạn (anchor), kết hợp xử lý mối quan hệ n-1 khi một bản dịch Việt bao quát nhiều dòng Hán.
