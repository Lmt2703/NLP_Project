"""Bộ điều phối toàn bộ quy trình dóng hàng tự động (End-to-End Pipeline).

Quy trình tự động hóa hoàn thiện:
1. Quét toàn bộ tệp PDF có trong thư mục 01_nguon/.
2. Trích xuất văn bản phân biệt font VNI/Unicode, khử nhiễu, cắt bỏ rác ấn tống/lưu chiểu.
3. Phân biệt chính xác Hán, Phiên âm và Dịch nghĩa; giải quyết triệt để các khối dồn bản dịch (Bản trướng thức, Thảo đơn thức, 12 tháng).
4. Dóng hàng song ngữ cấp câu bằng thuật toán quy hoạch động tối ưu O(1) kết hợp neo từ khóa Phật học.
5. Xuất tập dữ liệu bàn giao (TSV, Excel) và văn bản đơn ngữ sạch cho từng quyển và toàn bộ tác phẩm.
6. Đánh giá kiểm thử chất lượng và cập nhật báo cáo nghiệm thu Markdown tự động.
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
    text_dir = os.path.join(base_folder, "03_text_sach", "bach_truong")
    dong_hang_dir = os.path.join(base_folder, "04_dong_hang")

    pdf_files = sorted(glob.glob(os.path.join(nguon_dir, "SacTuBachTruongThanhQuy-*.pdf")))
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
        tsv_path = os.path.join(dong_hang_dir, f"{book_id}_parallel.tsv")
        xlsx_path = os.path.join(dong_hang_dir, f"{book_id}_parallel.xlsx")
        export_parallel_data(sent_pairs, tsv_path, xlsx_path)
        export_clean_text_files(
            sent_pairs,
            os.path.join(text_dir, f"{book_id}_han.txt"),
            os.path.join(text_dir, f"{book_id}_viet.txt"),
        )

        book_report = evaluate_parallel_files(tsv_path, xlsx_path)
        book_summaries.append({
            "book_id": book_id,
            "filename": filename,
            "para_count": len(para_pairs),
            "sent_count": len(sent_pairs),
            "valid_count": book_report["valid_pairs"],
            "missing_han": book_report["missing_han_count"],
            "missing_viet": book_report["missing_viet_count"],
            "cjk_in_viet": book_report["cjk_in_viet_count"],
            "vni_err": book_report["vni_artifact_count"],
            "error_rate": book_report["error_rate"],
        })
        print(
            f"    -> {filename}: {len(para_pairs)} đoạn | {len(sent_pairs)} câu | "
            f"Hợp lệ: {book_report['valid_pairs']}/{len(sent_pairs)} | "
            f"Lỗi: {book_report['error_rate']}% | CJK rò rỉ: {book_report['cjk_in_viet_count']}"
        )

    # Xuất dữ liệu cấp câu bàn giao chính thức
    final_tsv = os.path.join(dong_hang_dir, "SacTuBachTruongThanhQuy_parallel.tsv")
    final_xlsx = os.path.join(dong_hang_dir, "SacTuBachTruongThanhQuy_parallel.xlsx")
    export_parallel_data(all_sentence_pairs, final_tsv, final_xlsx)

    # Xuất toàn văn đơn ngữ sạch cho Sắc tu Bách Trượng thanh quy
    export_clean_text_files(
        all_sentence_pairs,
        os.path.join(text_dir, "bach_truong_han.txt"),
        os.path.join(text_dir, "bach_truong_viet.txt"),
    )

    # Đánh giá và báo cáo tổng hợp
    final_report = evaluate_parallel_files(final_tsv, final_xlsx)
    print_evaluation_report(final_report)

    # Cập nhật ngữ liệu tổng hợp 4 quyển và báo cáo hợp nhất
    from build_master_corpus import build_master_and_report
    build_master_and_report()

    elapsed = round(time.time() - start_time, 2)
    print(f"[+] Thời gian thực thi toàn bộ pipeline Bách Trượng: {elapsed} giây.")
    print(f"{banner}\n")


if __name__ == "__main__":
    main()
