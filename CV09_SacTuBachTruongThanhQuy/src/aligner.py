# -*- coding: utf-8 -*-
"""
Module dóng hàng (alignment) văn bản song ngữ Hán - Việt.
Tuân thủ Mục 3 & Mục 3.1 theo Guideline đồ án:
- Định dạng TSV: <CÂU_HÁN>\t<CÂU_VIỆT>
- Định dạng Excel: Sheet 'DONG_HANG', gồm đúng 2 cột 'Hán' và 'Việt'.
- Xử lý các mối quan hệ dóng hàng 1-1, n-1, 1-n.
- Xuất dữ liệu sạch sang 03_text_sach/ (han.txt, viet.txt).
"""

import os
import re
import pandas as pd
from typing import List, Dict, Tuple
from extract_clean import extract_book, is_cjk_char


def align_book_records(records: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Xử lý dóng hàng và chuẩn hóa các cặp Hán - Việt:
    - Loại bỏ các dòng tiêu đề Hán sót lại ở cuối vế Việt.
    - Xử lý các đoạn khuyết hoặc gộp n-1 khi nhiều dòng Hán tương ứng 1 đoạn Việt.
    """
    aligned = []
    
    # Biến tạm để gộp các dòng Hán liên tiếp nếu vế Việt chưa có hoặc dịch gộp
    pending_han = []
    pending_tags = []
    
    for r in records:
        tag = r["tag"]
        han = r["han"].strip()
        viet = r["viet"].strip()
        
        # Cắt bỏ chữ Hán sót ở cuối vế Việt (thường là tiêu đề mục tiếp theo)
        if viet:
            viet = re.sub(r'[\u4e00-\u9fff\s]+$', '', viet).strip()
            
        # Nếu cả 2 vế đều có nội dung
        if han and viet:
            if pending_han:
                # Gộp pending_han vào nếu có
                han = ' '.join(pending_han) + ' ' + han
                tag = f"{pending_tags[0]}-{tag}"
                pending_han = []
                pending_tags = []
                
            aligned.append({
                "tag": tag,
                "han": han,
                "viet": viet
            })
        elif han and not viet:
            # Có Hán nhưng chưa có bản dịch riêng (có thể dịch gộp ở đoạn sau - quan hệ n-1)
            pending_han.append(han)
            pending_tags.append(tag)
        elif not han and viet:
            if pending_han:
                # Ghép các câu Hán chờ với bản dịch này
                combined_han = ' '.join(pending_han)
                combined_tag = f"{pending_tags[0]}-{pending_tags[-1]}" if len(pending_tags) > 1 else pending_tags[0]
                aligned.append({
                    "tag": combined_tag,
                    "han": combined_han,
                    "viet": viet
                })
                pending_han = []
                pending_tags = []
            else:
                # Bản dịch không có nguyên tác Hán tương ứng
                aligned.append({
                    "tag": tag,
                    "han": "",
                    "viet": viet
                })
                
    # Nếu còn pending_han ở cuối sách
    if pending_han:
        combined_han = ' '.join(pending_han)
        combined_tag = f"{pending_tags[0]}-{pending_tags[-1]}" if len(pending_tags) > 1 else pending_tags[0]
        aligned.append({
            "tag": combined_tag,
            "han": combined_han,
            "viet": ""
        })
        
    return aligned


def export_parallel_data(all_pairs: List[Dict[str, str]], output_tsv: str, output_xlsx: str):
    """
    Xuất dữ liệu dóng hàng ra file TSV và Excel theo đúng định dạng bắt buộc trong Guideline:
    1. File TSV: mỗi dòng chứa đúng 1 cặp phân cách bằng phím tab (<CÂU_HÁN>\t<CÂU_VIỆT>).
    2. File Excel: Sheet tên 'DONG_HANG', đúng 2 cột 'Hán' và 'Việt'.
    """
    os.makedirs(os.path.dirname(output_tsv), exist_ok=True)
    os.makedirs(os.path.dirname(output_xlsx), exist_ok=True)
    
    # 1. Ghi file TSV
    with open(output_tsv, 'w', encoding='utf-8') as f:
        for p in all_pairs:
            han = p['han'].replace('\t', ' ').replace('\n', ' ').strip()
            viet = p['viet'].replace('\t', ' ').replace('\n', ' ').strip()
            f.write(f"{han}\t{viet}\n")
            
    print(f"[+] Đã xuất file TSV: {output_tsv} ({len(all_pairs)} cặp)")
    
    # 2. Ghi file Excel đúng chuẩn Sheet DONG_HANG và 2 cột 'Hán', 'Việt'
    df = pd.DataFrame([
        {
            "Hán": p['han'].replace('\n', ' ').strip(),
            "Việt": p['viet'].replace('\n', ' ').strip()
        }
        for p in all_pairs
    ])
    
    with pd.ExcelWriter(output_xlsx, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='DONG_HANG', index=False)
        
    print(f"[+] Đã xuất file Excel: {output_xlsx} (Sheet: DONG_HANG, {len(df)} dòng)")


def export_clean_text_files(all_pairs: List[Dict[str, str]], han_txt_path: str, viet_txt_path: str):
    """
    Xuất các file văn bản Hán và Việt đã làm sạch vào 03_text_sach/
    theo yêu cầu mục 2 của Guideline.
    """
    os.makedirs(os.path.dirname(han_txt_path), exist_ok=True)
    os.makedirs(os.path.dirname(viet_txt_path), exist_ok=True)
    
    with open(han_txt_path, 'w', encoding='utf-8') as fh:
        for p in all_pairs:
            h = p['han'].replace('\n', ' ').strip()
            if h:
                fh.write(h + '\n')
                
    with open(viet_txt_path, 'w', encoding='utf-8') as fv:
        for p in all_pairs:
            v = p['viet'].replace('\n', ' ').strip()
            if v:
                fv.write(v + '\n')
                
    print(f"[+] Đã xuất văn bản sạch: {han_txt_path} và {viet_txt_path}")
