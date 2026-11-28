# HƯỚNG DẪN CÀI ĐẶT VÀ TÁI LẬP QUY TRÌNH (`RUN_INSTRUCTIONS.md`)
## ĐỀ TÀI CV09 – DÓNG HÀNG SONG NGỮ HÁN – VIỆT (MSSV: 24125105 – LÊ MINH THUẬN)

Tài liệu này hướng dẫn từng bước để cài đặt môi trường, chạy lại toàn bộ pipeline trích xuất – làm sạch – dóng hàng – kiểm định tự động trên **4 quyển / 6 tệp PDF nguồn (6.886 cặp câu)**, và chạy kiểm định chéo độc lập bằng **Bertalign / LaBSE**.

---

## 1. Yêu cầu hệ thống

- **Python:** Phiên bản `3.9` trở lên (đã kiểm thử mượt trên Python `3.11` và `3.13`).
- **Hệ điều hành:** Windows (PowerShell/CMD), macOS hoặc Linux.
- **Thư viện cốt lõi:** `PyMuPDF`, `pandas`, `openpyxl`, `tqdm` (khai báo trong [`requirements.txt`](./requirements.txt)).
- **Kiểm định Bertalign/LaBSE:** Chạy trên **Google Colab (GPU T4)** với notebook [`CV09_Bertalign_Verification.ipynb`](./CV09_Bertalign_Verification.ipynb).

---

## 2. Cài đặt môi trường ảo & thư viện

Mở terminal tại thư mục gốc của bài nộp (`24125105/`):

### Windows PowerShell
```powershell
cd 24125105
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS / Linux
```bash
cd 24125105
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Kiểm tra nhanh thư viện đã cài đặt
```bash
python -c "import pymupdf, pandas, openpyxl, tqdm; print('Dependencies OK')"
```

---

## 3. Vận hành lại toàn bộ Pipeline trích xuất & dóng hàng (Local)

Đảm bảo đầy đủ 6 tệp PDF nguồn nằm trong `01_nguon/`:
1. `SacTuBachTruongThanhQuy-q4.pdf`
2. `SacTuBachTruongThanhQuy-q7.pdf`
3. `Trieu Chau Ngu Luc_VI_Text_ThongPhuong.pdf`
4. `Trieu Chau Ngu Luc_ZH_Text_X1315.pdf`
5. `Giai Thoat Dao Luan_VI_Text_NhuDien.pdf`
6. `Giai Thoat Dao Luan_ZH_Text_T1648.pdf`

Chạy tuần tự 4 lệnh sau từ thư mục `24125105/`:

### Bước 1: Dóng hàng *Sắc tu Bách Trượng thanh quy* (Quyển 4 & Quyển 7 → 886 cặp)
```bash
python src/run_pipeline.py
```
- **Đầu ra:**
  - `03_text_sach/bach_truong/q4_han.txt`, `q4_viet.txt`, `q7_han.txt`, `q7_viet.txt`, `bach_truong_han.txt`, `bach_truong_viet.txt`
  - `04_dong_hang/q4_parallel.tsv` / `.xlsx` *(482 cặp)*
  - `04_dong_hang/q7_parallel.tsv` / `.xlsx` *(404 cặp)*
  - `04_dong_hang/SacTuBachTruongThanhQuy_parallel.tsv` / `.xlsx` *(886 cặp)*

### Bước 2: Dóng hàng *Triệu Châu Ngữ Lục* (Quyển 14 → 1.039 cặp)
```bash
python src/run_pipeline_trieu_chau.py
```
- **Đầu ra:**
  - `03_text_sach/trieu_chau/trieu_chau_han.txt`, `trieu_chau_viet.txt`
  - `04_dong_hang/TrieuChauNguLuc_parallel.tsv` / `.xlsx` *(1.039 cặp)*

### Bước 3: Dóng hàng *Giải Thoát Đạo Luận* (Trọn bộ 12 Quyển / 12 Phẩm → 4.961 cặp)
```bash
python src/run_pipeline_giai_thoat_dao_luan.py
```
- **Đầu ra:**
  - `03_text_sach/giai_thoat_dao_luan/giai_thoat_dao_luan_han.txt`, `giai_thoat_dao_luan_viet.txt`
  - `04_dong_hang/GiaiThoatDaoLuan_parallel.tsv` / `.xlsx` *(4.961 cặp)*

### Bước 4: Hợp nhất toàn đề tài & cập nhật báo cáo kiểm định tự động (6.886 cặp)
```bash
python src/build_master_corpus.py
```
- **Đầu ra:**
  - `03_text_sach/han.txt` & `03_text_sach/viet.txt` *(6.886 dòng sạch)*
  - `04_dong_hang/CV09_TongHop_parallel.tsv` & `.xlsx` *(Sheet `DONG_HANG` + Sheet `THONG_KE`)*
  - `docs/Bao_cao_chat_luong_dong_hang.md`

### Bước 5: Chạy riêng bộ kiểm định cấu trúc & định dạng (`evaluate.py`)
```bash
python src/evaluate.py
```
- Kết quả kỳ vọng: `Tổng số cặp dóng: 6886`, `Số cặp hợp lệ: 6886`, `Tỷ lệ lỗi: 0.0%`, `Chuẩn định dạng TSV/Excel: ✓ Hợp lệ`, `Kết luận nghiệm thu: ĐẠT NGHIỆM THU (Pass - Tuyệt đối)`.

---

## 4. Tái lập kiểm định chéo độc lập bằng Bertalign & LaBSE (Google Colab)

1. Tải tệp [`CV09_Bertalign_Verification.ipynb`](./CV09_Bertalign_Verification.ipynb) lên **Google Colab** (`https://colab.research.google.com`).
2. Chọn menu **Runtime → Change runtime type → Hardware accelerator: T4 GPU**.
3. Chạy lần lượt các ô lệnh:
   - **Cell 1:** Tự động clone `bfsujason/bertalign`, cài `sentence-transformers`, `faiss-cpu`, `numba`, `sentence-splitter`, và vá lỗi tương thích `googletrans` trên Python 3.11+.
   - **Cell 2:** Tải lên 4 tệp `.tsv` từ `04_dong_hang/` (`q4_parallel.tsv`, `q7_parallel.tsv`, `TrieuChauNguLuc_parallel.tsv`, `GiaiThoatDaoLuan_parallel.tsv`) với `LOAD_MODE = "upload"`.
   - **Cell 3:** Chạy `Encoder("LaBSE")` tính điểm tương đồng ngữ nghĩa cosine và xuất `Bertalign_LaBSE_Audit.xlsx`.
   - **Cell 4:** Chạy `Bertalign(..., is_split=True)` độc lập so sánh đồng thuận `1–1` và xuất `Bertalign_Realign_Diff.xlsx`.
   - **Cell 5:** Tải 2 tệp báo cáo Excel về máy (đã lưu sẵn kết quả đã chạy tại `docs/Bertalign_LaBSE_Audit.xlsx` và `docs/Bertalign_Realign_Diff.xlsx`).

---

## 5. Đối chiếu danh mục hồ sơ minh chứng đã hoàn thiện

- **Bảng kiểm kê nguồn 8 trường (có link nguồn):** [`docs/Bang_kiem_ke_nguon.xlsx`](./docs/Bang_kiem_ke_nguon.xlsx) & [`docs/Bang_kiem_ke_nguon.md`](./docs/Bang_kiem_ke_nguon.md)
- **Kết quả soi 30 trang PDF gốc ngẫu nhiên ↔ `03_text_sach/` (≥ 5 trang / cuốn):** [`docs/Ket_qua_soi_PDF_goc.xlsx`](./docs/Ket_qua_soi_PDF_goc.xlsx) & [`docs/Ket_qua_soi_PDF_goc.md`](./docs/Ket_qua_soi_PDF_goc.md) + ảnh chụp trong [`docs/minh_chung/`](./docs/minh_chung/)
- **Kết quả chấm mẫu ngẫu nhiên 3 nhãn (50 cặp / cuốn = 200 cặp):** [`docs/Cham_mau_thu_cong_3_nhan.xlsx`](./docs/Cham_mau_thu_cong_3_nhan.xlsx) & [`docs/Cham_mau_thu_cong_3_nhan.md`](./docs/Cham_mau_thu_cong_3_nhan.md)
- **Biên bản ghi chú sai khác bản dịch gốc (theo Guideline):** [`docs/notes.xlsx`](./docs/notes.xlsx)
- **Kết quả kiểm định chéo Bertalign / LaBSE:** [`docs/Bertalign_LaBSE_Audit.xlsx`](./docs/Bertalign_LaBSE_Audit.xlsx), [`docs/Bertalign_Realign_Diff.xlsx`](./docs/Bertalign_Realign_Diff.xlsx) & [`CV09_Bertalign_Verification.ipynb`](./CV09_Bertalign_Verification.ipynb)
- **Ảnh chụp minh chứng `.xlsx` / `.tsv` / kiểm định:** [`docs/minh_chung/`](./docs/minh_chung/)
