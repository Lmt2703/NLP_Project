"""Module đánh giá và kiểm thử chất lượng dóng hàng song ngữ Hán - Việt.

Tuân thủ Mục 6, 7 & 8 trong Guideline đồ án:
- Kiểm tra tính hợp lệ của cấu trúc TSV và Excel.
- Phát hiện các lỗi MISSING (khuyết vế Hán hoặc vế Việt).
- Tính toán tỷ lệ lỗi và đối chiếu với ngưỡng nghiệm thu (tối đa 30%).
"""

import os
from typing import Any, Dict
import pandas as pd


def evaluate_parallel_files(tsv_path: str, xlsx_path: str) -> Dict[str, Any]:
    """Kiểm tra và đánh giá toàn diện hai file kết quả song ngữ."""
    report: Dict[str, Any] = {
        "tsv_path": tsv_path,
        "xlsx_path": xlsx_path,
        "total_pairs": 0,
        "valid_pairs": 0,
        "missing_han_count": 0,
        "missing_viet_count": 0,
        "error_count": 0,
        "error_rate": 0.0,
        "tsv_format_ok": True,
        "xlsx_format_ok": True,
        "acceptance_status": "KHÔNG ĐẠT",
    }

    if not os.path.isfile(tsv_path):
        report["tsv_format_ok"] = False
        return report

    tsv_rows = []
    with open(tsv_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            if len(parts) != 2:
                report["tsv_format_ok"] = False
            else:
                tsv_rows.append((parts[0].strip(), parts[1].strip()))

    if not os.path.isfile(xlsx_path):
        report["xlsx_format_ok"] = False
        return report

    excel_file = pd.ExcelFile(xlsx_path)
    if "DONG_HANG" not in excel_file.sheet_names:
        report["xlsx_format_ok"] = False

    df = pd.read_excel(xlsx_path, sheet_name="DONG_HANG")
    if list(df.columns) != ["Hán", "Việt"]:
        report["xlsx_format_ok"] = False

    total = len(df)
    missing_han = 0
    missing_viet = 0

    for _, row in df.iterrows():
        h = str(row["Hán"]).strip() if pd.notna(row["Hán"]) else ""
        v = str(row["Việt"]).strip() if pd.notna(row["Việt"]) else ""
        if not h:
            missing_han += 1
        if not v:
            missing_viet += 1

    error_count = missing_han + missing_viet
    report["total_pairs"] = total
    report["valid_pairs"] = total - error_count
    report["missing_han_count"] = missing_han
    report["missing_viet_count"] = missing_viet
    report["error_count"] = error_count
    report["error_rate"] = round((error_count / total) * 100, 2) if total > 0 else 100.0

    if report["error_rate"] <= 30.0 and report["tsv_format_ok"] and report["xlsx_format_ok"]:
        report["acceptance_status"] = "ĐẠT NGHIỆM THU (Pass)"
    else:
        report["acceptance_status"] = "CHƯA ĐẠT (Fail)"

    return report


def print_evaluation_report(report: Dict[str, Any]) -> None:
    """Hiển thị bảng báo cáo đánh giá nghiệm thu trên terminal."""
    bar = "=" * 56
    print(f"\n{bar}")
    print("        BÁO CÁO ĐÁNH GIÁ CHẤT LƯỢNG DÓNG HÀNG")
    print(bar)
    print(f" File TSV:              {os.path.basename(report['tsv_path'])}")
    print(f" File Excel:            {os.path.basename(report['xlsx_path'])}")
    print(f" Tổng số cặp dóng:      {report['total_pairs']}")
    print(f" Số cặp hợp lệ:         {report['valid_pairs']}")
    print(f" Khuyết vế Hán:         {report['missing_han_count']}")
    print(f" Khuyết vế Việt:        {report['missing_viet_count']}")
    print(f" Tỷ lệ lỗi:             {report['error_rate']}%")
    print(f" Chuẩn định dạng TSV:   {'✓ Hợp lệ' if report['tsv_format_ok'] else '✗ Lỗi'}")
    print(f" Chuẩn định dạng Excel: {'✓ Hợp lệ' if report['xlsx_format_ok'] else '✗ Lỗi'}")
    print(f" Kết luận nghiệm thu:   {report['acceptance_status']}")
    print(f"{bar}\n")


if __name__ == "__main__":
    tsv = "CV09_SacTuBachTruongThanhQuy/04_dong_hang/SacTuBachTruongThanhQuy_parallel.tsv"
    xlsx = "CV09_SacTuBachTruongThanhQuy/04_dong_hang/SacTuBachTruongThanhQuy_parallel.xlsx"
    if os.path.exists(tsv) and os.path.exists(xlsx):
        print_evaluation_report(evaluate_parallel_files(tsv, xlsx))
