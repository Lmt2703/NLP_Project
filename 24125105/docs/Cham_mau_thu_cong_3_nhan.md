# KẾT QUẢ CHẤM MẪU THỦ CÔNG NGẪU NHIÊN 3 NHÃN LỖI (`OMISSION` / `ADDITION` / `MISSING`)
## ĐỀ TÀI CV09 – MSSV: 24125105 (LÊ MINH THUẬN)

- **Yêu cầu bắt buộc (`Guideline.pdf` Mục 7–8):** Chấm mẫu ngẫu nhiên **tối thiểu 50 cặp / cuốn** theo 3 nhãn lỗi **`OMISSION` / `ADDITION` / `MISSING`** để tính **Tỷ lệ lỗi (%) thực tế** *(mục tiêu ≤ 20%, ngưỡng nghiệm thu ≤ 30%)*.
- **Bảng chấm chi tiết đầy đủ 200 cặp:** [`Cham_mau_thu_cong_3_nhan.xlsx`](./Cham_mau_thu_cong_3_nhan.xlsx) *(gồm 7 sheet: `TONG_HOP`, `MAU_BT_Q4` [50], `MAU_BT_Q7` [50], `MAU_TC_Q14` [50], `MAU_GTDL_12Q` [50], `CHAM_MAU_200` [200], `QUY_UOC_3_NHAN`)*.
- **Phương pháp lấy mẫu ngẫu nhiên tái lập:** Dùng `random.Random(24125105).sample(range(N), 50)` chọn ngẫu nhiên **50 cặp độc lập cho mỗi cuốn** trên cả **4 cuốn** → **tổng cộng N = 200 cặp câu** rút trực tiếp từ các tệp bàn giao trong `04_dong_hang/`.
- **Quy ước 3 nhãn lỗi bắt buộc + nhãn Đạt (`OK`):**
  - **`OK`**: Hai vế Hán – Việt đầy đủ, khớp nội dung ngữ nghĩa và ranh giới câu.
  - **`OMISSION`** *(Thiếu nghĩa / sót vế)*: Cột Hán có mệnh đề/vế mang nghĩa rõ nhưng bị thiếu ở cột Việt cùng dòng (thường do lệch ranh giới 1 vế sang dòng liền kề hoặc bản dịch gốc rút gọn).
  - **`ADDITION`** *(Thừa nội dung / dư vế)*: Cột Việt chứa thêm mệnh đề thuộc câu Hán khác hoặc nội dung ngoài nguyên tác Hán cùng dòng.
  - **`MISSING`** *(Khuyết hoàn toàn 1 bên)*: Bỏ trống hoàn toàn cột Hán hoặc cột Việt.

---

## 1. Bảng tổng hợp kết quả chấm mẫu ngẫu nhiên (50 cặp / cuốn × 4 cuốn = 200 cặp)

| Mã quyển | Tên cuốn sách | Tổng cặp corpus | Mẫu ngẫu nhiên | `OK` (Đạt) | `OMISSION` | `ADDITION` | `MISSING` | Tổng lỗi (3 nhãn) | Tỷ lệ lỗi (%) | Đánh giá (Mục tiêu ≤20%, Đạt ≤30%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`BT_Q4`** | Sắc tu Bách Trượng thanh quy – Quyển 4 | 482 | **50** | 38 *(76.0%)* | 10 | 2 | 0 | 12 | **24.00%** | **ĐẠT NGƯỠNG (≤ 30%)** |
| **`BT_Q7`** | Sắc tu Bách Trượng thanh quy – Quyển 7 | 404 | **50** | 43 *(86.0%)* | 7 | 0 | 0 | 7 | **14.00%** | **ĐẠT MỤC TIÊU (≤ 20%)** |
| **`TC_Q14`** | Triệu Châu Chân Tế Thiền Sư Ngữ Lục – Q14 | 1,039 | **50** | 50 *(100.0%)* | 0 | 0 | 0 | 0 | **0.00%** | **ĐẠT MỤC TIÊU (≤ 20%)** |
| **`GTDL_12Q`** | Giải Thoát Đạo Luận – Trọn bộ 12 Quyển | 4,961 | **50** | 40 *(80.0%)* | 7 | 3 | 0 | 10 | **20.00%** | **ĐẠT MỤC TIÊU (≤ 20%)** |
| **TỔNG 200** | **Tổng hợp không trọng số (50 cặp/cuốn)** | **6,886** | **200** | **171 (85.5%)** | **24 (12.0%)** | **5 (2.5%)** | **0 (0.0%)** | **29** | **14.50%** | **ĐẠT MỤC TIÊU (≤ 20%)** |
| **ƯỚC LƯỢNG** | **Có trọng số theo quy mô 4 cuốn (6,886 cặp)** | **6,886** | **200** | **~83.09%** | — | — | **0.0%** | — | **~16.91%** | **ĐẠT MỤC TIÊU (≤ 20%)** |

---

## 2. Phân tích chi tiết từng loại lỗi trên 200 cặp ngẫu nhiên

1. **`MISSING` = 0 / 200 (0.0%):** Tuyệt đối không có dòng khuyết Hán hay khuyết Việt — khớp 100% với kiểm định tự động `evaluate.py` trên toàn bộ 6.886 cặp.
2. **`OMISSION` = 24 / 200 (12.0%):**
   - *Sắc tu Bách Trượng Q4* (`10/50`) & *Q7* (`7/50`): Chủ yếu do đặc thù văn ngôn đời Nguyên súc tích kết hợp bản dịch diễn giải dài gấp 5.3×–7.1× và tách lại câu khác dấu `。` của CBETA, dẫn đến 1 vế ngắn (2–6 chữ) ở đầu/cuối câu Hán nằm sang dòng Việt liền kề (cô lập cục bộ, không gây trượt dây chuyền).
   - *Triệu Châu Q14* (`0/50`): Đạt **100% khớp chuẩn** trên cả 50 cặp ngẫu nhiên, đồng nhất với kết quả kiểm định chéo độc lập Bertalign (**98.85%** đồng thuận `1–1`).
   - *Giải Thoát Đạo Luận 12Q* (`7/50`): Gồm 6 vị trí lệch ranh giới 1 vế ngắn cục bộ (dòng `981, 1563, 1623, 2505, 3009, 3018`) và 1 vị trí bản dịch PDF gốc bỏ sót 2 chữ `識陰` (dòng `1761` — đã lập biên bản trong [`notes.xlsx`](./notes.xlsx)).
3. **`ADDITION` = 5 / 200 (2.5%):**
   - `BT_Q4` (2 cặp: dòng `97, 306`) và `GTDL_12Q` (3 cặp: dòng `960, 1888, 3209`) — đều là cụm ngắn 3–6 từ ở đầu/cuối câu Việt thuộc câu Hán liền kề.
4. **Kết luận nghiệm thu (`Guideline.pdf` Mục 7–8):**
   - Cả **4/4 cuốn sách** đều đạt ngưỡng nghiệm thu **≤ 30%** (`24.0%`, `14.0%`, `0.0%`, `20.0%`), trong đó **3/4 cuốn** đạt mức mục tiêu khắt khe **≤ 20%**.
   - **Tỷ lệ lỗi tổng thể thực tế** đạt **14.50%** *(29/200 cặp)* và **ước lượng có trọng số toàn corpus** đạt **~16.91%** — đều đạt **mục tiêu ≤ 20%** và vượt xa **ngưỡng nghiệm thu ≤ 30%**.
5. **Biên bản sai khác bản dịch gốc (`notes.xlsx`):** Toàn bộ các điểm sai khác do bản in PDF dịch Việt (như dòng `1606`, `1761`, `2189`, `3648`, `4669`, `4815`, `4899` ở *Giải Thoát Đạo Luận*) được ghi nhận riêng tại [`notes.xlsx`](./notes.xlsx), tuân thủ nguyên tắc không tự ý sửa nội dung bản dịch.
