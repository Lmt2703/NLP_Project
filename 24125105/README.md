# HỒ SƠ NỘP ĐỒ ÁN GIỮA KỲ NLP – ĐỀ TÀI CV09
## MSSV: 24125105 – LÊ MINH THUẬN
### Dóng hàng song ngữ Hán – Việt: *Sắc tu Bách Trượng thanh quy* (Q4 & Q7), *Triệu Châu Ngữ Lục* (Q14) & *Giải Thoát Đạo Luận* (12 Quyển)

---

## 1. Tóm tắt kết quả bàn giao

- **Tổng số dữ liệu nguồn:** **6 tệp PDF Text (Hướng A)** = **882 trang PDF** (4 quyển/bộ sách).
- **Tổng số cặp câu song ngữ Hán – Việt bàn giao:** **6.886 cặp câu hợp lệ** *(113.897 chữ Hán CJK; 144.536 từ tiếng Việt)* — vượt xa mức tối thiểu 3.000 cặp/thành viên.
  - *Sắc tu Bách Trượng thanh quy – Quyển 4:* **482 cặp**
  - *Sắc tu Bách Trượng thanh quy – Quyển 7:* **404 cặp** *(tệp gộp Q4+Q7: **886 cặp**)*
  - *Triệu Châu Chân Tế Thiền Sư Ngữ Lục – Quyển 14:* **1.039 cặp**
  - *Giải Thoát Đạo Luận – Trọn bộ 12 Quyển / 12 Phẩm:* **4.961 cặp**
- **Kiểm định cấu trúc & định dạng (`evaluate.py`):** **0.0% lỗi** (`0` dòng `MISSING`, `0` CJK rò rỉ trong vế Việt, `0` lỗi font VNI/CMap, `100%` hợp lệ chuẩn `.tsv` & `.xlsx` sheet `DONG_HANG`).
- **Kiểm định chéo độc lập Bertalign / LaBSE (Colab GPU T4):** **6.290 / 6.886 = 91.34%** đồng thuận trực tiếp `1–1`.
- **Soi ngẫu nhiên PDF gốc ↔ `03_text_sach/` (≥ 5 trang / cuốn):** **30 trang ngẫu nhiên** (`5 trang/PDF`: `BT_Q4` 5 tr, `BT_Q7` 5 tr, `TC_Q14` 10 tr, `GTDL_12Q` 10 tr) → **30/30 (100%) khớp sạch**.
- **Chấm mẫu ngẫu nhiên 3 nhãn (`OMISSION` / `ADDITION` / `MISSING`, 50 cặp / cuốn = 200 cặp):** **171/200 đạt (`OK`)**, `24 OMISSION`, `5 ADDITION`, `0 MISSING` → tỷ lệ lỗi thực tế **14.50%** *(ước lượng có trọng số toàn corpus **~16.91%**)* — đạt mục tiêu **≤ 20%**, vượt xa ngưỡng nghiệm thu **≤ 30%**.

---

## 2. Cấu trúc đầy đủ thư mục nộp bài `24125105/`

```text
24125105/
├── 01_nguon/                                      # 6 tệp PDF nguồn nguyên bản (882 trang)
│   ├── SacTuBachTruongThanhQuy-q4.pdf
│   ├── SacTuBachTruongThanhQuy-q7.pdf
│   ├── Trieu Chau Ngu Luc_VI_Text_ThongPhuong.pdf
│   ├── Trieu Chau Ngu Luc_ZH_Text_X1315.pdf
│   ├── Giai Thoat Dao Luan_VI_Text_NhuDien.pdf
│   └── Giai Thoat Dao Luan_ZH_Text_T1648.pdf
├── 02_ocr_tho/
│   └── README.md                                  # Thuyết minh nguồn Hướng A (PDF Text)
├── 03_text_sach/                                  # Văn bản đơn ngữ Hán & Việt sạch (6.886 dòng)
│   ├── han.txt / viet.txt
│   ├── bach_truong/                               # q4, q7, bach_truong
│   ├── trieu_chau/                                # trieu_chau_han/viet
│   └── giai_thoat_dao_luan/                       # giai_thoat_dao_luan_han/viet
├── 04_dong_hang/                                  # Kết quả dóng hàng chuẩn .tsv & .xlsx (Sheet DONG_HANG)
│   ├── CV09_TongHop_parallel.tsv / .xlsx          # Tổng hợp 4 quyển (6.886 cặp + sheet THONG_KE)
│   ├── SacTuBachTruongThanhQuy_parallel.tsv / .xlsx
│   ├── q4_parallel.tsv / .xlsx
│   ├── q7_parallel.tsv / .xlsx
│   ├── TrieuChauNguLuc_parallel.tsv / .xlsx
│   └── GiaiThoatDaoLuan_parallel.tsv / .xlsx
├── docs/                                          # Toàn bộ hồ sơ kiểm kê, báo cáo & minh chứng
│   ├── Bang_kiem_ke_nguon.xlsx / .md              # Bảng kiểm kê nguồn chuẩn 8 trường (có Link nguồn)
│   ├── Ket_qua_soi_PDF_goc.xlsx / .md             # Soi 30 trang ngẫu nhiên PDF gốc ↔ 03_text_sach/ (≥5 tr/cuốn)
│   ├── Cham_mau_thu_cong_3_nhan.xlsx / .md        # Chấm ngẫu nhiên 200 cặp (50/cuốn – OMISSION/ADDITION/MISSING)
│   ├── Bertalign_LaBSE_Audit.xlsx                 # Chấm điểm tương đồng ngữ nghĩa LaBSE (6.886 cặp)
│   ├── Bertalign_Realign_Diff.xlsx                # Kiểm định chéo độc lập Bertalign (91.34% 1-1)
│   ├── notes.xlsx                                 # Ghi chú sai khác bản dịch theo quy định Guideline
│   ├── Bao_cao_chat_luong_dong_hang.md            # Báo cáo tổng hợp kiểm tra chất lượng cả 4 quyển
│   └── minh_chung/                                # 10 ảnh chụp minh chứng PDF gốc, .xlsx, .tsv & kiểm định
│       ├── pdf_01_BT_q4_p1_p6.png
│       ├── pdf_02_BT_q4_p144_BT_q7_p1.png
│       ├── pdf_03_BT_q7_p4_p11_bantruong.png
│       ├── pdf_04_TC_vi_p1_p52_p101.png
│       ├── pdf_05_TC_zh_p2_p18.png
│       ├── pdf_06_GTDL_vi_p51_zh_p5_p115.png
│       ├── evidence_xlsx_CV09_TongHop.png
│       ├── evidence_tsv_CV09_TongHop.png
│       ├── evidence_xlsx_per_book.png
│       └── evidence_bertalign_and_manual_audit.png
├── src/                                           # 12 module Python tái lập toàn bộ pipeline
├── CV09_Bertalign_Verification.ipynb              # Notebook Colab (GPU T4) kiểm định Bertalign & LaBSE
├── requirements.txt                               # Thư viện phụ thuộc Python
├── RUN_INSTRUCTIONS.md                            # Hướng dẫn cài đặt và chạy lại từng bước
└── README.md                                      # Tệp giới thiệu này
```

---

## 3. Chạy nhanh (Quick Start)

Xem hướng dẫn chi tiết tại [`RUN_INSTRUCTIONS.md`](./RUN_INSTRUCTIONS.md):
```bash
pip install -r requirements.txt
python src/run_pipeline.py
python src/run_pipeline_trieu_chau.py
python src/run_pipeline_giai_thoat_dao_luan.py
python src/build_master_corpus.py
python src/evaluate.py
```
