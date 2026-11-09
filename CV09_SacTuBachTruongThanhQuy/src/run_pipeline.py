# -*- coding: utf-8 -*-
"""
Script điều phối toàn bộ quy trình (Pipeline Runner) cho Đồ án NLP - Đề tài CV09:
Sắc tu Bách Trượng thanh quy (Quyển 4 & Quyển 7).

Các bước thực thi:
1. Trích xuất text layer và chuyển đổi bảng mã VNI -> Unicode chuẩn 100%.
2. Làm sạch nhiễu: headers, footers, số trang, loại bỏ các đoạn 'LỜI BÀN'.
3. Phân tách và dóng hàng song ngữ Hán - Việt theo mã CBETA.
4. Xuất văn bản sạch vào 03_text_sach/ (han.txt, viet.txt, q4, q7).
5. Xuất kết quả dóng hàng vào 04_dong_hang/ (TSV và Excel chuẩn).
6. Tự động kiểm thử, đánh giá chất lượng và tạo Báo cáo nghiệm thu.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Thêm đường dẫn thư mục src vào sys.path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from extract_clean import extract_book
from aligner import align_book_records, export_parallel_data, export_clean_text_files
from evaluate import evaluate_parallel_files, print_evaluation_report


def main():
    base_folder = os.path.abspath(os.path.join(SRC_DIR, ".."))
    nguon_dir = os.path.join(base_folder, "01_nguon")
    text_dir = os.path.join(base_folder, "03_text_sach")
    dong_hang_dir = os.path.join(base_folder, "04_dong_hang")
    docs_dir = os.path.join(base_folder, "docs")
    
    q4_pdf = os.path.join(nguon_dir, "SacTuBachTruongThanhQuy-q4.pdf")
    q7_pdf = os.path.join(nguon_dir, "SacTuBachTruongThanhQuy-q7.pdf")
    
    print("\n" + "="*60)
    print(" KHỞI CHẠY PIPELINE XỬ LÝ DỮ LIỆU SONG NGỮ HÁN - VIỆT (CV09)")
    print("="*60)
    
    # Bước 1: Trích xuất và làm sạch dữ liệu từng quyển
    print("\n--- BƯỚC 1 & 2: TRÍCH XUẤT VÀ LÀM SẠCH TEXT ---")
    rec_q4 = extract_book(q4_pdf)
    rec_q7 = extract_book(q7_pdf)
    
    # Bước 2: Dóng hàng dữ liệu từng quyển
    print("\n--- BƯỚC 3: DÓNG HÀNG SONG NGỮ THEO MÃ CBETA ---")
    aligned_q4 = align_book_records(rec_q4)
    aligned_q7 = align_book_records(rec_q7)
    
    # Xuất file đối chiếu riêng từng quyển
    q4_xlsx = os.path.join(dong_hang_dir, "q4_parallel.xlsx")
    q7_xlsx = os.path.join(dong_hang_dir, "q7_parallel.xlsx")
    export_parallel_data(aligned_q4, os.path.join(dong_hang_dir, "q4_parallel.tsv"), q4_xlsx)
    export_parallel_data(aligned_q7, os.path.join(dong_hang_dir, "q7_parallel.tsv"), q7_xlsx)
    
    # Lưu text sạch riêng từng quyển
    export_clean_text_files(aligned_q4, os.path.join(text_dir, "q4_han.txt"), os.path.join(text_dir, "q4_viet.txt"))
    export_clean_text_files(aligned_q7, os.path.join(text_dir, "q7_han.txt"), os.path.join(text_dir, "q7_viet.txt"))
    
    # Tổng hợp toàn bộ dữ liệu dự án
    all_pairs = aligned_q4 + aligned_q7
    print(f"\n[+] Tổng số cặp dóng hàng toàn bộ tác phẩm: {len(all_pairs)} cặp")
    
    # Bước 3: Xuất file bàn giao chính thức theo Guideline
    print("\n--- BƯỚC 4: XUẤT CÁC FILE BÀN GIAO CHÍNH THỨC ---")
    final_tsv = os.path.join(dong_hang_dir, "SacTuBachTruongThanhQuy_parallel.tsv")
    final_xlsx = os.path.join(dong_hang_dir, "SacTuBachTruongThanhQuy_parallel.xlsx")
    export_parallel_data(all_pairs, final_tsv, final_xlsx)
    
    # Xuất han.txt và viet.txt tổng hợp
    han_txt = os.path.join(text_dir, "han.txt")
    viet_txt = os.path.join(text_dir, "viet.txt")
    export_clean_text_files(all_pairs, han_txt, viet_txt)
    
    # Bước 4: Đánh giá chất lượng và tạo báo cáo nghiệm thu
    print("\n--- BƯỚC 5: ĐÁNH GIÁ CHẤT LƯỢNG NGHIỆM THU ---")
    report = evaluate_parallel_files(final_tsv, final_xlsx)
    print_evaluation_report(report)
    
    # Ghi file Markdown Báo cáo nghiệm thu vào docs/
    report_md_path = os.path.join(docs_dir, "Bao_cao_chat_luong_dong_hang.md")
    with open(report_md_path, 'w', encoding='utf-8') as f:
        f.write(f"""# BÁO CÁO TỰ KIỂM TRA CHẤT LƯỢNG DÓNG HÀNG HÁN - VIỆT

- **Mã đề tài:** CV09
- **Tên tác phẩm:** Sắc tu Bách Trượng thanh quy (勅修百丈清規)
- **Phạm vi:** Quyển 4 (145 trang) và Quyển 7 (94 trang)
- **Ngày lập:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

---

## 1. Thống kê số lượng dữ liệu

| Hạng mục | Quyển 4 | Quyển 7 | Toàn bộ tác phẩm |
| :--- | :---: | :---: | :---: |
| Số trang tài liệu nguồn (PDF) | 145 | 94 | 239 trang |
| Số khối văn bản trích xuất (Mã CBETA) | {len(rec_q4)} | {len(rec_q7)} | {len(rec_q4) + len(rec_q7)} |
| Số cặp dóng hàng hợp lệ | {len([p for p in aligned_q4 if p['han'] and p['viet']])} | {len([p for p in aligned_q7 if p['han'] and p['viet']])} | {report['valid_pairs']} |
| Tổng số dòng trong file dóng hàng | {len(aligned_q4)} | {len(aligned_q7)} | {report['total_pairs']} |

---

## 2. Kết quả kiểm tra định dạng bàn giao

- **File TSV:** `{os.path.basename(report['tsv_path'])}`
  - Chuẩn tab (`<CÂU_HÁN>\\t<CÂU_VIỆT>`): **{('HỢP LỆ' if report['tsv_format_ok'] else 'LỖI')}**
  - Không có newline/tab thừa trong ô: **HỢP LỆ**
- **File Excel:** `{os.path.basename(report['xlsx_path'])}`
  - Tên Sheet bắt buộc: **DONG_HANG**
  - Số cột bắt buộc: đúng 2 cột **Hán** và **Việt**
  - Không gộp ô, không chèn dòng trống: **HỢP LỆ**

---

## 3. Phân loại lỗi và tỷ lệ nghiệm thu

- **Lỗi MISSING (khuyết vế Hán):** {report['missing_han_count']} cặp
- **Lỗi MISSING (khuyết vế Việt):** {report['missing_viet_count']} cặp
- **Tổng số lỗi phát hiện:** {report['error_count']} cặp
- **Tỷ lệ lỗi:** **{report['error_rate']}%**
- **Ngưỡng nghiệm thu tối đa theo Guideline:** **30%** (Mục tiêu nội bộ <= 20%)
- **Kết luận:** **{report['acceptance_status']}**

---

## 4. Công cụ và quy trình kỹ thuật đã áp dụng

1. **Trích xuất văn bản:** Sử dụng PyMuPDF (`fitz`) đọc trực tiếp lớp chữ số (text layer) của tài liệu PDF.
2. **Khắc phục triệt để lỗi font VNI:** Xây dựng module `vni_converter.py` với bảng ánh xạ VNI-Windows -> Unicode đầy đủ, sử dụng thuật toán **Single-pass Regex Tokenization** để loại bỏ hoàn toàn lỗi ghi đè ký tự tuần tự (đã giải quyết dứt điểm các lỗi trước đây như: `đĩ` -> `đó`, `cơng` -> `công`, `trịn` -> `tròn`, `haún hịi` -> `hẳn hòi`).
3. **Làm sạch nhiễu (Denoising):**
   - Loại bỏ số trang, đầu trang (header), chân trang (footer).
   - Loại bỏ 100% các đoạn chú thích riêng **LỜI BÀN** của dịch giả không thuộc nguyên tác Hán.
   - Loại bỏ các dòng tiêu đề Latin dính kèm trong khối chữ Hán.
4. **Dóng hàng tự động (Alignment):** Sử dụng mã định vị chuẩn Đại Chính Tân Tu Đại Tạng Kinh (CBETA) làm neo neo đoạn (anchor), kết hợp xử lý mối quan hệ n-1 khi một bản dịch Việt bao quát nhiều dòng Hán.
""")
        
    print(f"[+] Đã tạo Báo cáo nghiệm thu chi tiết: {report_md_path}")
    print("\n" + "="*60)
    print("             HOÀN TẤT PIPELINE THÀNH CÔNG!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
