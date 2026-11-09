# BÁO CÁO TỰ KIỂM TRA CHẤT LƯỢNG DÓNG HÀNG HÁN - VIỆT (CẤP CÂU & ĐOẠN)

- **Mã đề tài:** CV09
- **Tên tác phẩm:** Sắc tu Bách Trượng thanh quy (勅修百丈清規)
- **Phương pháp dóng hàng:** Dóng hàng neo theo mã đoạn CBETA kết hợp Tách câu & Quy hoạch động (Anchor-based Sentence DP Alignment).
- **Ngày cập nhật:** 09/11/2026 23:18:27

---

## 1. Thống kê số lượng dữ liệu

| Quyển sách | Số cặp cấp Đoạn | Tổng số câu dóng hàng | Số câu hợp lệ hoàn chỉnh |
| :--- | :---: | :---: | :---: |
| q4 (SacTuBachTruongThanhQuy-q4.pdf) | 55 | 388 | 388 |
| q7 (SacTuBachTruongThanhQuy-q7.pdf) | 87 | 334 | 334 |
| **TOÀN BỘ DỰ ÁN** | **142** | **722** | **722** |

> **Nhận xét về số lượng:**
> Khi chuyển từ cấp Đoạn xuống cấp Câu, số lượng cặp dóng hàng tăng từ **142 cặp** lên **722 cặp câu** (tăng hơn 5 lần), giúp sinh viên tiến sát và nhanh chóng hoàn thành chỉ tiêu 3.000 cặp theo Guideline khi bổ sung thêm quyển.

---

## 2. Kết quả kiểm tra định dạng bàn giao

- **File TSV:** `SacTuBachTruongThanhQuy_parallel.tsv`
  - Chuẩn tab (`<CÂU_HÁN>\t<CÂU_VIỆT>`): **HỢP LỆ**
  - Không chứa tab/newline thừa trong nội dung: **HỢP LỆ**
- **File Excel:** `SacTuBachTruongThanhQuy_parallel.xlsx`
  - Sheet bắt buộc: **DONG_HANG**
  - Cột bắt buộc: đúng 2 cột **Hán** và **Việt**
  - Không gộp ô, không chèn dòng trống: **HỢP LỆ**

---

## 3. Phân loại lỗi và tỷ lệ nghiệm thu

- **Lỗi MISSING (khuyết vế Hán):** 0 cặp
- **Lỗi MISSING (khuyết vế Việt):** 0 cặp
- **Tổng số lỗi phát hiện:** 0 cặp
- **Tỷ lệ lỗi:** **0.0%**
- **Ngưỡng nghiệm thu tối đa theo Guideline:** **30%**
- **Kết luận:** **ĐẠT NGHIỆM THU (Pass)**

---

## 4. Các điểm kỹ thuật nâng cấp

1. **Sửa lỗi lệch mã đoạn:** Tự động phát hiện và liên kết các mã dòng bị người biên soạn sách ghi nhầm (ví dụ `[1134a02]` với `[1134a03]`, `[1150b16]` với `[1150b17]`).
2. **Thuật toán tách câu thông minh (Sentence-level DP Alignment):**
   - Không cắt cơ học: Mỗi câu Hán và Việt được ghép đôi dựa trên hàm khoảng cách tỷ lệ độ dài ngữ nghĩa (Gale-Church cải tiến cho Hán - Việt).
   - Tự động nhận diện các quan hệ $1-1, 2-1, 3-1, 1-2, 2-2$ để câu giữ nguyên ý nghĩa trọn vẹn, không cụt ý.
3. **Pipeline 1 chạm (One-click Pipeline):** Tự động phát hiện mọi file PDF có trong `01_nguon/`, xử lý hàng loạt chỉ bằng một dòng lệnh.
