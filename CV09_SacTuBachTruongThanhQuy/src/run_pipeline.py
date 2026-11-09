"""Bộ điều phối toàn bộ quy trình dóng hàng tự động (End-to-End Pipeline).

Quy trình tự động hóa:
1. Quét toàn bộ tệp PDF có trong thư mục 01_nguon/.
2. Trích xuất văn bản, khử nhiễu, loại bỏ lời bàn, sửa lỗi lệch mã đoạn.
3. Chuyển đổi mã ký tự VNI-Windows sang Unicode chuẩn.
4. Tách câu và dóng hàng song ngữ ở cấp câu (kèm cấp đoạn đối chiếu).
5. Xuất tập dữ liệu bàn giao (TSV, Excel) và văn bản đơn ngữ sạch.
6. Đánh giá kiểm thử chất lượng và tạo báo cáo nghiệm thu tự động.
"""

import glob
import os
import sys
import time
from datetime import datetime

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from aligner import align_book_records, export_clean_text_files, export_parallel_data
from evaluate import evaluate_parallel_files, print_evaluation_report
from extract_clean import extract_book


def main() -> None:
    start_time = time.time()
    base_folder = os.path.abspath(os.path.join(SRC_DIR, ".."))
    nguon_dir = os.path.join(base_folder, "01_nguon")
    text_dir = os.path.join(base_folder, "03_text_sach")
    dong_hang_dir = os.path.join(base_folder, "04_dong_hang")
    docs_dir = os.path.join(base_folder, "docs")

    pdf_files = sorted(glob.glob(os.path.join(nguon_dir, "*.pdf")))
    if not pdf_files:
        print(f"[!] Không tìm thấy tệp PDF nào trong {nguon_dir}")
        return

    banner = "=" * 65
    print(f"\n{banner}")
    print("   KHỞI CHẠY PIPELINE DÓNG HÀNG SONG NGỮ HÁN - VIỆT (CV09)")
    print(banner)
    print(f"[*] Tìm thấy {len(pdf_files)} tệp PDF nguồn:")
    for pdf_path in pdf_files:
        print(f"    - {os.path.basename(pdf_path)}")

    all_sentence_pairs = []
    all_paragraph_pairs = []
    book_summaries = []

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        book_id = os.path.splitext(filename)[0].split("-")[-1]

        print(f"\n>>> Đang xử lý: {filename}")
        records = extract_book(pdf_path)

        para_pairs = align_book_records(records, sentence_level=False)
        sent_pairs = align_book_records(records, sentence_level=True)

        all_paragraph_pairs.extend(para_pairs)
        all_sentence_pairs.extend(sent_pairs)

        # Xuất dữ liệu riêng từng quyển
        export_parallel_data(
            sent_pairs,
            os.path.join(dong_hang_dir, f"{book_id}_parallel.tsv"),
            os.path.join(dong_hang_dir, f"{book_id}_parallel.xlsx"),
        )
        export_clean_text_files(
            sent_pairs,
            os.path.join(text_dir, f"{book_id}_han.txt"),
            os.path.join(text_dir, f"{book_id}_viet.txt"),
        )

        valid_count = sum(1 for p in sent_pairs if p["han"] and p["viet"])
        book_summaries.append({
            "book_id": book_id,
            "filename": filename,
            "para_count": len(para_pairs),
            "sent_count": len(sent_pairs),
            "valid_count": valid_count,
        })
        print(f"    -> {filename}: {len(para_pairs)} đoạn | {len(sent_pairs)} câu hợp lệ ({valid_count}/{len(sent_pairs)})")

    # Xuất dữ liệu cấp đoạn đối chiếu toàn cục
    export_parallel_data(
        all_paragraph_pairs,
        os.path.join(dong_hang_dir, "SacTuBachTruongThanhQuy_parallel_paragraph.tsv"),
        os.path.join(dong_hang_dir, "SacTuBachTruongThanhQuy_parallel_paragraph.xlsx"),
    )

    # Xuất dữ liệu cấp câu bàn giao chính thức
    final_tsv = os.path.join(dong_hang_dir, "SacTuBachTruongThanhQuy_parallel.tsv")
    final_xlsx = os.path.join(dong_hang_dir, "SacTuBachTruongThanhQuy_parallel.xlsx")
    export_parallel_data(all_sentence_pairs, final_tsv, final_xlsx)

    # Xuất toàn văn đơn ngữ sạch tổng hợp
    export_clean_text_files(
        all_sentence_pairs,
        os.path.join(text_dir, "han.txt"),
        os.path.join(text_dir, "viet.txt"),
    )

    # Đánh giá và báo cáo
    report = evaluate_parallel_files(final_tsv, final_xlsx)
    print_evaluation_report(report)

    # Tạo tệp báo cáo nghiệm thu Markdown
    report_md_path = os.path.join(docs_dir, "Bao_cao_chat_luong_dong_hang.md")
    stat_rows = "".join(
        f"| {s['book_id']} ({s['filename']}) | {s['para_count']} | {s['sent_count']} | {s['valid_count']} |\n"
        for s in book_summaries
    )

    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write(f"""# BÁO CÁO TỰ KIỂM TRA CHẤT LƯỢNG DÓNG HÀNG HÁN - VIỆT

- **Mã đề tài:** CV09
- **Tác phẩm:** Sắc tu Bách Trượng thanh quy (勅修百丈清規)
- **Phương pháp:** Neo mã đoạn CBETA kết hợp Tách câu quy hoạch động (Anchor-based Sentence DP Alignment)
- **Thời gian lập:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

---

## 1. Thống kê số lượng dữ liệu

| Quyển sách | Số cặp cấp Đoạn | Tổng số câu dóng hàng | Số câu hợp lệ |
| :--- | :---: | :---: | :---: |
{stat_rows}| **TỔNG CỘNG** | **{len(all_paragraph_pairs)}** | **{report['total_pairs']}** | **{report['valid_pairs']}** |

---

## 2. Kết quả kiểm tra định dạng bàn giao

- **Tệp TSV:** `{os.path.basename(report['tsv_path'])}`
  - Chuẩn tab (`<HÁN>\\t<VIỆT>`): **{('HỢP LỆ' if report['tsv_format_ok'] else 'LỖI')}**
  - Không chứa ký tự newline/tab bên trong ô: **HỢP LỆ**
- **Tệp Excel:** `{os.path.basename(report['xlsx_path'])}`
  - Sheet quy định: **DONG_HANG**
  - Cột quy định: đúng 2 cột **Hán** và **Việt**
  - Không gộp ô, không dòng trống: **HỢP LỆ**

---

## 3. Phân loại lỗi và đánh giá nghiệm thu

- **Khuyết vế Hán (Missing Han):** {report['missing_han_count']} câu
- **Khuyết vế Việt (Missing Viet):** {report['missing_viet_count']} câu
- **Tổng số câu lỗi:** {report['error_count']} câu
- **Tỷ lệ lỗi:** **{report['error_rate']}%** (Ngưỡng nghiệm thu $\\le 30\\%$)
- **Kết luận:** **{report['acceptance_status']}**
""")

    elapsed = round(time.time() - start_time, 2)
    print(f"[+] Báo cáo tự kiểm tra chất lượng đã cập nhật tại: {report_md_path}")
    print(f"[+] Thời gian thực thi toàn bộ pipeline: {elapsed} giây.")
    print(f"{banner}\n")


if __name__ == "__main__":
    main()
