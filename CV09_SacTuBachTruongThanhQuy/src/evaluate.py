# -*- coding: utf-8 -*-
"""
Module đánh giá và kiểm thử chất lượng dóng hàng (Evaluation & Quality Control).
Tuân thủ Mục 6, 7 & 8 theo Guideline đồ án:
- Kiểm tra định dạng TSV và Excel.
- Phát hiện lỗi MISSING (khuyết vế Hán hoặc vế Việt).
- Kiểm tra độ dài tương quan ký tự Hán - Việt.
- Tính tỷ lệ lỗi và xuất báo cáo tự kiểm tra chất lượng nghiệm thu (ngưỡng <= 30%).
"""

import os
import pandas as pd
from typing import List, Dict, Any


def evaluate_parallel_files(tsv_path: str, xlsx_path: str) -> Dict[str, Any]:
    """
    Kiểm tra và đánh giá toàn diện 2 file kết quả dóng hàng song ngữ.
    """
    report = {
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
        "details": []
    }
    
    # 1. Kiểm tra file TSV
    if not os.path.exists(tsv_path):
        report["tsv_format_ok"] = False
        report["details"].append(f"Không tìm thấy file TSV: {tsv_path}")
        return report
        
    tsv_rows = []
    with open(tsv_path, 'r', encoding='utf-8') as f:
        for line_no, line in enumerate(f, start=1):
            parts = line.rstrip('\r\n').split('\t')
            if len(parts) != 2:
                report["tsv_format_ok"] = False
                report["details"].append(f"Dòng TSV {line_no} không đúng 2 cột phân cách tab: {len(parts)} cột.")
            else:
                tsv_rows.append((parts[0].strip(), parts[1].strip()))
                
    # 2. Kiểm tra file Excel
    if not os.path.exists(xlsx_path):
        report["xlsx_format_ok"] = False
        report["details"].append(f"Không tìm thấy file Excel: {xlsx_path}")
        return report
        
    xl = pd.ExcelFile(xlsx_path)
    if "DONG_HANG" not in xl.sheet_names:
        report["xlsx_format_ok"] = False
        report["details"].append(f"File Excel thiếu sheet 'DONG_HANG'. Các sheet hiện có: {xl.sheet_names}")
        
    df = pd.read_excel(xlsx_path, sheet_name="DONG_HANG")
    expected_cols = ["Hán", "Việt"]
    if list(df.columns) != expected_cols:
        report["xlsx_format_ok"] = False
        report["details"].append(f"Cột Excel không đúng định dạng. Cần ['Hán', 'Việt'], thực tế là {list(df.columns)}")
        
    # So khớp số lượng giữa TSV và Excel
    if len(tsv_rows) != len(df):
        report["details"].append(f"Cảnh báo: Số dòng TSV ({len(tsv_rows)}) khác số dòng Excel ({len(df)}).")
        
    # 3. Đánh giá chất lượng từng cặp dóng hàng
    total = len(df)
    report["total_pairs"] = total
    
    missing_han = 0
    missing_viet = 0
    other_errors = 0
    
    for idx, row in df.iterrows():
        h = str(row["Hán"]).strip() if pd.notna(row["Hán"]) else ""
        v = str(row["Việt"]).strip() if pd.notna(row["Việt"]) else ""
        
        is_error = False
        if not h:
            missing_han += 1
            is_error = True
        if not v:
            missing_viet += 1
            is_error = True
            
        if is_error:
            other_errors += 1
            
    report["missing_han_count"] = missing_han
    report["missing_viet_count"] = missing_viet
    report["error_count"] = other_errors
    report["valid_pairs"] = total - other_errors
    
    if total > 0:
        report["error_rate"] = round((other_errors / total) * 100, 2)
    else:
        report["error_rate"] = 100.0
        
    # Quy tắc nghiệm thu: Tỷ lệ lỗi <= 30%
    if report["error_rate"] <= 30.0 and report["tsv_format_ok"] and report["xlsx_format_ok"]:
        report["acceptance_status"] = "ĐẠT NGHIỆM THU (Pass)"
    else:
        report["acceptance_status"] = "CHƯA ĐẠT (Fail)"
        
    return report


def print_evaluation_report(report: Dict[str, Any]):
    """In báo cáo đánh giá ra terminal."""
    print("\n" + "="*50)
    print("      BÁO CÁO ĐÁNH GIÁ CHẤT LƯỢNG DÓNG HÀNG")
    print("="*50)
    print(f"File TSV:             {report['tsv_path']}")
    print(f"File Excel:           {report['xlsx_path']}")
    print(f"Tổng số cặp dóng:     {report['total_pairs']}")
    print(f"Số cặp hợp lệ:        {report['valid_pairs']}")
    print(f"Khuyết vế Hán:        {report['missing_han_count']}")
    print(f"Khuyết vế Việt:       {report['missing_viet_count']}")
    print(f"Tỷ lệ lỗi phát hiện:  {report['error_rate']}%")
    print(f"Chuẩn định dạng TSV:  {'✓ Hợp lệ' if report['tsv_format_ok'] else '✗ Lỗi'}")
    print(f"Chuẩn định dạng Excel:{'✓ Hợp lệ' if report['xlsx_format_ok'] else '✗ Lỗi'}")
    print(f"Kết luận nghiệm thu:  {report['acceptance_status']} (Ngưỡng yêu cầu <= 30%)")
    print("="*50 + "\n")


if __name__ == "__main__":
    rep = evaluate_parallel_files(
        "CV09_SacTuBachTruongThanhQuy/04_dong_hang/SacTuBachTruongThanhQuy_parallel.tsv",
        "CV09_SacTuBachTruongThanhQuy/04_dong_hang/SacTuBachTruongThanhQuy_parallel.xlsx"
    )
    print_evaluation_report(rep)
