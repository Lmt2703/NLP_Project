"""Module trích xuất và làm sạch văn bản Hán - Việt từ tài liệu PDF.

Quy trình xử lý:
1. Trích xuất lớp văn bản (text layer) từ PDF qua thư viện PyMuPDF.
2. Chuyển đổi mã ký tự VNI-Windows sang Unicode dựng sẵn.
3. Loại bỏ header, footer, số trang và các đoạn 'Lời bàn' riêng của dịch giả.
4. Hiệu đính các mã đoạn CBETA bị lệch trong ấn bản gốc.
5. Phân tách và làm sạch khối văn bản chữ Hán và tiếng Việt tương ứng.
"""

import os
import re
from typing import Dict, List
import fitz

from vni_converter import convert_vni_to_unicode

# Biểu thức chính quy loại bỏ thành phần nhiễu
NOISE_PATTERNS = [
    r"^\s*\d+\s*$",
    r"SẮC TU BÁCH TRƯỢNG THANH QUI.*",
    r"Quyển thứ \d+",
    r"Quyển \d+",
    r"Quyeån \d+",
    r"卷第.*",
    r"勅修百丈清規卷第.*",
]

# Ánh xạ hiệu đính mã đoạn CBETA bị gõ lệch trong nguyên bản
TAG_CORRECTIONS = {
    "[1134a02]": "[1134a03]",
    "[1150b16]": "[1150b17]",
}

CBETA_PATTERN = re.compile(r"(\[\d{4}[a-z]\d{2}\])(.*?)(?=\[\d{4}[a-z]\d{2}\]|\Z)", re.DOTALL)


def is_cjk_char(ch: str) -> bool:
    """Kiểm tra ký tự có thuộc dải mã CJK (chữ Hán) hay không."""
    code = ord(ch)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0x20000 <= code <= 0x2A6DF)


def clean_han_text(raw_text: str) -> str:
    """Làm sạch văn bản chữ Hán: giữ chữ CJK và dấu câu Hán chuẩn, loại bỏ tiêu đề Latin."""
    valid_lines = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        cjk_count = sum(1 for c in line if is_cjk_char(c))
        latin_count = sum(1 for c in line if c.isalpha() and not is_cjk_char(c))

        if cjk_count > 0 and (cjk_count >= latin_count or latin_count == 0):
            valid_lines.append(line)
        elif cjk_count > 0:
            cleaned = "".join(c for c in line if is_cjk_char(c) or c in "。，、：；！？「」『』（）《》\u3000 ")
            if cleaned.strip():
                valid_lines.append(cleaned.strip())

    return re.sub(r"\s+", " ", " ".join(valid_lines)).strip()


def clean_viet_text(raw_text: str) -> str:
    """Làm sạch văn bản tiếng Việt: loại bỏ lời bàn, dấu phân cách và tiêu đề thừa."""
    text = re.sub(r"LỜI BÀN.*?(?=\[\d{4}[a-z]\d{2}\]|\Z|\*\s*\*|\*\s*\*\s*\*)", "", raw_text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"[\u4e00-\u9fff\s]+$", "", text)

    valid_lines = []
    header_filter = re.compile(
        r"^(SẮC TU|CHƯƠNG \d+|LƯỠNG TỰ|BẢN TRƯỚNG|ĐẠI TRÍ|ĐẠI LONG|TRỤ TRÌ CHÙA|Chương [A-ZÀ-Ỹa-ỹ\s]+ hết|Tiết lạp chương chung)",
        re.IGNORECASE,
    )
    for line in text.splitlines():
        line = line.strip()
        if line and not header_filter.match(line):
            valid_lines.append(line)

    return re.sub(r"\s+", " ", " ".join(valid_lines)).strip()


def extract_book(pdf_path: str) -> List[Dict[str, str]]:
    """Trích xuất và cấu trúc hóa toàn bộ văn bản Hán - Việt từ tệp PDF."""
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"Không tìm thấy tệp: {pdf_path}")

    doc = fitz.open(pdf_path)
    full_text = "\n".join(convert_vni_to_unicode(page.get_text("text")) for page in doc)

    for pattern in NOISE_PATTERNS:
        full_text = re.sub(pattern, "", full_text, flags=re.MULTILINE | re.IGNORECASE)

    raw_matches = CBETA_PATTERN.findall(full_text)
    by_tag: Dict[str, List[str]] = {}

    for tag, content in raw_matches:
        corrected_tag = TAG_CORRECTIONS.get(tag, tag)
        by_tag.setdefault(corrected_tag, []).append(content.strip())

    extracted_records: List[Dict[str, str]] = []

    for tag, blocks in by_tag.items():
        han_blocks: List[str] = []
        viet_blocks: List[str] = []

        for block in blocks:
            cjk_count = sum(1 for c in block if is_cjk_char(c))
            latin_count = sum(1 for c in block if c.isalpha() and not is_cjk_char(c))
            total_alpha = cjk_count + latin_count

            is_han = (
                (cjk_count >= 20)
                or (cjk_count > 0 and latin_count == 0)
                or (cjk_count > latin_count)
                or (cjk_count >= 5 and total_alpha > 0 and (cjk_count / total_alpha) >= 0.25)
            )

            if is_han:
                han_blocks.append(block)
            else:
                viet_blocks.append(block)

        han_clean = clean_han_text(" ".join(han_blocks)) if han_blocks else ""
        viet_clean = ""
        if len(viet_blocks) >= 2:
            viet_clean = clean_viet_text(viet_blocks[-1])
        elif len(viet_blocks) == 1:
            viet_clean = clean_viet_text(viet_blocks[0])

        extracted_records.append({
            "tag": tag,
            "han": han_clean,
            "viet": viet_clean,
        })

    return extracted_records


if __name__ == "__main__":
    test_pdf = "CV09_SacTuBachTruongThanhQuy/01_nguon/SacTuBachTruongThanhQuy-q4.pdf"
    if os.path.exists(test_pdf):
        results = extract_book(test_pdf)
        print(f"Trích xuất thành công: {len(results)} khối CBETA.")
