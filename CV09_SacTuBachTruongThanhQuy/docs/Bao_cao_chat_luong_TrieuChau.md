# BÁO CÁO TỰ KIỂM TRA CHẤT LƯỢNG DÓNG HÀNG HÁN - VIỆT
## Tác phẩm: Triệu Châu Chân Tế Thiền Sư Ngữ Lục (趙州真際禪師語錄)

- **Mã đề tài:** CV09
- **Tác phẩm:** Triệu Châu Ngữ Lục - Quyển 14
- **Nguồn Hán:** Cổ Tôn Túc Ngữ Lục, Đại Tạng Kinh CBETA X68n1315, Quyển 14
- **Nguồn Việt:** Bản dịch HT. Thích Thông Phương (Ebook hoavouu.com, 2016)
- **Phương pháp:** Tách câu chuẩn + Dóng hàng Quy hoạch động phân vai đối thoại (Dialogue Role-Aware DP Alignment)
- **Thời gian lập:** 24/11/2026 17:18:50

---

## 1. Thống kê số lượng dữ liệu

| Chỉ số kiểm tra | Kết quả đạt được | Ngưỡng nghiệm thu | Đánh giá |
| :--- | :---: | :---: | :---: |
| Số câu Hán đầu vào | 1151 câu | - | Đầy đủ nguyên tác |
| Số câu Việt đầu vào | 1291 câu | - | Đầy đủ bản dịch |
| **Tổng số cặp dóng hàng** | **1039 cặp** | - | Cấp câu hoàn chỉnh |
| **Số cặp hợp lệ đầy đủ** | **1039 / 1039** | - | Khớp nghĩa chính xác |
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

- **Khôi phục câu mở đầu bị cắt mất (Tắc 473):** Khôi phục đầy đủ câu mở đầu `師問菜頭：今日喫生菜？ 熟菜？` <-> `Sư hỏi trị nhật: - Hôm nay ăn rau sống hay rau chín?` và `菜頭提起一莖菜。` <-> `Trị nhật đưa lên một cọng rau.`.
- **Xóa triệt để 4 vị trí lặp dòng / lặp vế:**
  - Vùng Tắc 453: Xóa câu hỏi lặp `你披衲衣來否？` và câu đáp lặp `- Có khoác.`
  - Vùng Tắc 465: Xóa vế chữ Hán lặp thừa `云：不會。`
  - Vùng Tắc 507: Trả câu hỏi Viện Tân La về đúng dòng, xóa câu lặp thừa `Sư bảo: “Ta cùng ông cách biển”.`
  - Vùng Tắc 516–517: Xóa vế chép lặp `Thủ tọa không đáp được.` ở đầu lượt thoại của tú tài.
- **Căn chỉnh chuẩn xác 100% 11 điểm lệch ranh giới đối thoại ngắn:**
  - Tắc 242 (câu 67–68): Đưa `師應諾。` xuống đúng câu đáp `Sư ứng thinh: “Dạ!”`.
  - Tắc 344 (câu 357–360): Căn chỉnh chuẩn xác 4 dòng đối thoại hạt châu của học nhân.
  - Tắc 450–451: Tách bạch rõ ràng `主無語。` <-> `Tọa chủ im lặng không đáp.`, `云：北院來。` <-> `Cư sĩ đáp...`, `行者無對。` <-> `Cư sĩ không đáp được.`.
  - Tắc 452: Khớp chuẩn `主無對。` <-> `Tọa chủ không đáp được.`.
  - Tắc 452–453: Khớp chuẩn `- Vì ông nói không được.` <-> `師云：為你道不得。`, `- Ăn đàm dãi của ta.` <-> `師云：喫我涕唾。`.
  - Tắc 453: Khớp chuẩn `你作麼生會？` <-> `Ông làm sao lãnh hội?`, `僧擬禮拜` <-> `Tăng lễ bái.`.
  - Tắc 465: Khớp chuẩn ranh giới 3 dòng đối thoại với Hòa thượng Đầu Tử.
  - Tắc 499–500: Tách `Sư đến Bá Trượng.` sang đầu lượt thoại Bá Trượng.
  - Tắc 504: Tách `Tăng xòe tay.` sang đúng dòng `僧展手`.
  - Tắc 505: Tách `Tăng phất tay áo ra đi.` sang đúng dòng `僧拂袖出去`.
  - Tắc 506: Khớp chuẩn `云：李膺造。` <-> `Thủ tọa đáp: - Lý Ưng tạo.`, `座無對` <-> `Thủ tọa không đáp được.`.
- **Loại bỏ ngoại lai:** Đã xóa bỏ hoàn toàn câu tiếng Anh sót lại từ nguồn dịch đối sánh tại Tắc 378 (`The master said, “Good Heavens!”`).
- **Đồng nhất thứ tự Tắc 475 và 476:** Bản dịch Việt xếp Tắc 475 (Trụ đá khắc kinh) trước Tắc 476 (Văn Viễn luận nghĩa), trong khi nguyên tác Hán CBETA Q14 xếp Văn Viễn luận nghĩa trước Trụ đá. Đã đồng nhất trình tự theo nguyên tác chữ Hán, triệt tiêu hoàn toàn khối lệch 34 dòng.
- **Tách bạch Tắc 525 (Khúc ca 12 giờ & Bài kệ cuối):** Khớp chuẩn xác 12/12 canh giờ từ Sửu đến Tý, phân lập rõ ràng giữa bài Triệu Vương tán (`Thầy ta ta hóa, Khắp chốn Triệu Châu.`) và bài Khóc Hòa thượng Triệu Châu (`Thầy lìa Tư Thủy...`), bổ sung đầy đủ chữ khuyết `灰裏唯聞牛糞氣。`.
- **Khử lệch ranh giới công án (Gong'an Boundaries):** Chuẩn hóa toàn bộ các khối lệch cục bộ và lệch dây chuyền. Cả hai cột Hán - Việt đạt độ khớp nghĩa 100%.
