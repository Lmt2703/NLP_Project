# -*- coding: utf-8 -*-
"""
Module trích xuất và tiền xử lý làm sạch văn bản Hán - Việt từ PDF.
Tuân thủ Quy trình thực hiện tổng thể (Bước 4 & Bước 5) theo Guideline đồ án:
1. Trích xuất text layer nguyên bản từ PDF.
2. Chuyển đổi bảng mã VNI sang Unicode chuẩn.
3. Loại bỏ header, footer, số trang lặp lại.
4. Loại bỏ các đoạn 'LỜI BÀN' của dịch giả (không có nguyên tác Hán).
5. Sửa lỗi lệch mã đoạn do người biên soạn gõ nhầm (ví dụ: [1134a02] -> [1134a03], [1150b16] -> [1150b17]).
6. Phân loại chuẩn xác khối Hán vs khối Việt (kể cả các câu ngắn 4-10 chữ).
"""

import fitz  # PyMuPDF
import re
import os
from typing import List, Dict
from vni_converter import convert_vni_to_unicode


def is_cjk_char(ch: str) -> bool:
    """Kiểm tra một ký tự có thuộc khối CJK (chữ Hán) hay không."""
    cp = ord(ch)
    return (0x4E00 <= cp <= 0x9FFF) or (0x3400 <= cp <= 0x4DBF) or (0x20000 <= cp <= 0x2A6DF)


def clean_han_text(raw_text: str) -> str:
    """
    Làm sạch khối văn bản Hán:
    - Loại bỏ các dòng tiêu đề Latin in hoa bị dính ở cuối khối Hán.
    - Giữ lại chữ Hán và các dấu câu Hán chuẩn.
    - Chuẩn hóa khoảng trắng.
    """
    lines = []
    for line in raw_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        cjk_cnt = sum(1 for c in line if is_cjk_char(c))
        latin_cnt = sum(1 for c in line if c.isalpha() and not is_cjk_char(c))
        
        # Nếu dòng chứa chữ Hán chiếm ưu thế hoặc thuần Hán
        if cjk_cnt > 0 and (cjk_cnt >= latin_cnt or latin_cnt == 0):
            lines.append(line)
        elif cjk_cnt > 0:
            cleaned = ''.join(c for c in line if is_cjk_char(c) or c in '。，、：；！？「」『』（）《》\u3000 ')
            if cleaned.strip():
                lines.append(cleaned.strip())
    
    text = ' '.join(lines)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_viet_text(raw_text: str) -> str:
    """
    Làm sạch khối văn bản tiếng Việt:
    - Loại bỏ đoạn LỜI BÀN của dịch giả.
    - Loại bỏ các ký tự phân cách rác (*, ***).
    - Cắt bỏ tiêu đề chữ Hán hoặc câu chú thích cuối chương không có nguyên tác Hán.
    - Chuẩn hóa khoảng trắng.
    """
    # 1. Loại bỏ các đoạn LỜI BÀN
    text = re.sub(r'LỜI BÀN.*?(?=\[\d{4}[a-z]\d{2}\]|\Z|\*\s*\*|\*\s*\*\s*\*)', '', raw_text, flags=re.DOTALL | re.IGNORECASE)
    # 2. Xóa các dấu sao phân cách
    text = re.sub(r'\*+', '', text)
    # 3. Cắt bỏ cụm chữ Hán tiêu đề sót lại ở cuối bản Việt
    text = re.sub(r'[\u4e00-\u9fff\s]+$', '', text)
    
    # 4. Loại bỏ các dòng tiêu đề hoặc câu kết riêng
    lines = []
    for line in text.split('\n'):
        l = line.strip()
        if not l:
            continue
        if re.match(r'^(SẮC TU|CHƯƠNG \d+|LƯỠNG TỰ|BẢN TRƯỚNG|ĐẠI TRÍ|ĐẠI LONG|TRỤ TRÌ CHÙA|Chương [A-ZÀ-Ỹa-ỹ\s]+ hết|Tiết lạp chương chung)', l, re.IGNORECASE):
            continue
        lines.append(l)
        
    text = ' '.join(lines)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_book(pdf_path: str) -> List[Dict[str, str]]:
    """
    Trích xuất toàn bộ văn bản từ file PDF sách,
    chuyển mã và bóc tách các khối Hán - Việt theo mã CBETA.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Không tìm thấy file: {pdf_path}")
        
    print(f"[*] Đang đọc và trích xuất PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    
    pages_text = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        raw = page.get_text("text")
        uni = convert_vni_to_unicode(raw)
        pages_text.append(uni)
        
    full_text = '\n'.join(pages_text)
    
    # Dọn dẹp header/footer lặp lại trên toàn văn bản
    headers = [
        r'^\s*\d+\s*$', # Số trang riêng lẻ
        r'SẮC TU BÁCH TRƯỢNG THANH QUI.*',
        r'Quyển thứ \d+',
        r'Quyển \d+',
        r'Quyeån \d+',
        r'卷第.*',
        r'勅修百丈清規卷第.*'
    ]
    for h in headers:
        full_text = re.sub(h, '', full_text, flags=re.MULTILINE | re.IGNORECASE)
        
    # Tìm các khối văn bản theo mã tag CBETA [xxxx y zz]
    pattern = r'(\[\d{4}[a-z]\d{2}\])(.*?)(?=\[\d{4}[a-z]\d{2}\]|\Z)'
    matches = re.findall(pattern, full_text, re.DOTALL)
    
    # Hiệu đính các tag bị gõ nhầm mã trong sách gốc theo nhận xét của người hướng dẫn
    corrected_matches = []
    for tag, body in matches:
        # Sửa mã [1134a02] ở bản Việt thành [1134a03] để khớp với cụm Hán [1134a03-05]
        if tag == '[1134a02]':
            tag = '[1134a03]'
        # Sửa mã [1150b16] ở bản Việt thành [1150b17] để khớp với cụm Hán [1150b17-22]
        elif tag == '[1150b16]':
            tag = '[1150b17]'
        corrected_matches.append((tag, body))
    
    by_tag: Dict[str, List[str]] = {}
    for tag, body in corrected_matches:
        by_tag.setdefault(tag, []).append(body.strip())
        
    extracted_records: List[Dict[str, str]] = []
    
    for tag, blocks in by_tag.items():
        han_blocks = []
        viet_blocks = []
        
        for b in blocks:
            cjk_cnt = sum(1 for c in b if is_cjk_char(c))
            latin_cnt = sum(1 for c in b if c.isalpha() and not is_cjk_char(c))
            
            # Phân loại khối Hán vs khối Việt:
            # - Khối Hán: cjk >= 20, hoặc thuần Hán (latin == 0), hoặc cjk > latin,
            #   hoặc các câu hạ khoản ngắn (cjk >= 5 và tỷ lệ cjk chiếm >= 25% khối)
            is_han_block = (
                (cjk_cnt >= 20) or 
                (cjk_cnt > 0 and latin_cnt == 0) or 
                (cjk_cnt > latin_cnt) or 
                (cjk_cnt >= 5 and (cjk_cnt / (cjk_cnt + latin_cnt)) >= 0.25)
            )
            
            if is_han_block:
                han_blocks.append(b)
            else:
                viet_blocks.append(b)
                
        # Làm sạch Hán
        han_clean = clean_han_text(' '.join(han_blocks)) if han_blocks else ""
        
        # Làm sạch Việt (ưu tiên khối dịch nghĩa ở cuối)
        viet_clean = ""
        if len(viet_blocks) >= 2:
            viet_clean = clean_viet_text(viet_blocks[-1])
        elif len(viet_blocks) == 1:
            viet_clean = clean_viet_text(viet_blocks[0])
            
        extracted_records.append({
            "tag": tag,
            "han": han_clean,
            "viet": viet_clean
        })
        
    print(f"[+] Hoàn tất: {pdf_path} -> Trích xuất được {len(extracted_records)} khối mã CBETA.")
    return extracted_records


if __name__ == "__main__":
    records = extract_book("CV09_SacTuBachTruongThanhQuy/01_nguon/SacTuBachTruongThanhQuy-q4.pdf")
    print(f"Đã trích xuất {len(records)} bản ghi.")
