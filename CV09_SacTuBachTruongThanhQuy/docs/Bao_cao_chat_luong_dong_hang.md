# BÁO CÁO TỰ KIỂM TRA CHẤT LƯỢNG DÓNG HÀNG HÁN - VIỆT

- **Mã đề tài:** CV09
- **Tác phẩm:** Sắc tu Bách Trượng thanh quy (勅修百丈清規)
- **Phương pháp:** Neo mã đoạn CBETA kết hợp Tách câu quy hoạch động (Anchor-based Sentence DP Alignment)
- **Thời gian lập:** 09/11/2026 23:23:21

---

## 1. Thống kê số lượng dữ liệu

| Quyển sách | Số cặp cấp Đoạn | Tổng số câu dóng hàng | Số câu hợp lệ |
| :--- | :---: | :---: | :---: |
| q4 (SacTuBachTruongThanhQuy-q4.pdf) | 55 | 388 | 388 |
| q7 (SacTuBachTruongThanhQuy-q7.pdf) | 87 | 334 | 334 |
| **TỔNG CỘNG** | **142** | **722** | **722** |

---

## 2. Kết quả kiểm tra định dạng bàn giao

- **Tệp TSV:** `SacTuBachTruongThanhQuy_parallel.tsv`
  - Chuẩn tab (`<HÁN>\t<VIỆT>`): **HỢP LỆ**
  - Không chứa ký tự newline/tab bên trong ô: **HỢP LỆ**
- **Tệp Excel:** `SacTuBachTruongThanhQuy_parallel.xlsx`
  - Sheet quy định: **DONG_HANG**
  - Cột quy định: đúng 2 cột **Hán** và **Việt**
  - Không gộp ô, không dòng trống: **HỢP LỆ**

---

## 3. Phân loại lỗi và đánh giá nghiệm thu

- **Khuyết vế Hán (Missing Han):** 0 câu
- **Khuyết vế Việt (Missing Viet):** 0 câu
- **Tổng số câu lỗi:** 0 câu
- **Tỷ lệ lỗi:** **0.0%** (Ngưỡng nghiệm thu $\le 30\%$)
- **Kết luận:** **ĐẠT NGHIỆM THU (Pass)**
