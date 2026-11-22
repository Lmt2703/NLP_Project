"""Module chuyển đổi bảng mã ký tự VNI-Windows sang Unicode dựng sẵn.

Phiên bản nâng cấp:
1. Áp dụng bảng ánh xạ mở rộng đầy đủ các tổ hợp âm, dấu thanh và ký tự đặc biệt của VNI.
2. Xử lý cấp font-span khi trích xuất từ PDF qua extract_text_from_pdf():
   - Span dùng font VNI-* và không phải CJK -> chuyển đổi VNI sang Unicode.
   - Span dùng font khác (TimesNewRoman, MSSong, Arial...) -> giữ nguyên.
3. Tự động chuẩn hóa các biến thể lỗi font/dấu kép tồn đọng (leã -> lễ, saün -> sẵn, mộït -> một, Dieãn -> Diễn, Tâây -> Tây).
"""

import re
from typing import Dict
import fitz  # PyMuPDF


# ---------------------------------------------------------------------------
# Bảng ánh xạ ký tự VNI-Windows → Unicode chuẩn
# ---------------------------------------------------------------------------
VNI_TO_UNICODE_MAP: Dict[str, str] = {
    # Tổ hợp ươ + dấu thanh
    "öôù": "ướ", "öôø": "ườ", "öôû": "ưở", "öôõ": "ưỡ", "öôï": "ượ", "öô": "ươ",
    "ÖÔÙ": "ƯỚ", "ÖÔØ": "ƯỜ", "ÖÔÛ": "ƯỞ", "ÖÔÕ": "ƯỠ", "ÖÔÏ": "ƯỢ", "ÖÔ": "ƯƠ",

    # Ký tự ơ + dấu thanh
    "ôù": "ớ", "ôø": "ờ", "ôû": "ở", "ôõ": "ỡ", "ôï": "ợ", "ô": "ơ",
    "ÔÙ": "Ớ", "ÔØ": "Ờ", "ÔÛ": "Ở", "ÔÕ": "Ỡ", "ÔÏ": "Ợ", "Ô": "Ơ",

    # Ký tự ư + dấu thanh
    "öù": "ứ", "öø": "ừ", "öû": "ử", "öõ": "ữ", "öï": "ự", "ö": "ư",
    "ÖÙ": "Ứ", "ÖØ": "Ừ", "ÖÛ": "Ử", "ÖÕ": "Ữ", "ÖÏ": "Ự", "Ö": "Ư",

    # Ký tự â + dấu thanh
    "aù": "á", "aø": "à", "aû": "ả", "aõ": "ã", "aï": "ạ",
    "aá": "ấ", "aà": "ầ", "aå": "ẩ", "aã": "ẫ", "aä": "ậ", "aâ": "â",
    "AÁ": "Ấ", "AÀ": "Ầ", "AÅ": "Ẩ", "AÃ": "Ẫ", "AÄ": "Ậ", "AÂ": "Â",

    # Ký tự ă + dấu thanh
    "aé": "ắ", "aè": "ằ", "aú": "ẳ", "aö": "ẵ", "aü": "ẵ", "aë": "ặ", "aê": "ă",
    "AÉ": "Ắ", "AÈ": "Ằ", "AÚ": "Ẳ", "AÖ": "Ẵ", "AÜ": "Ẵ", "AË": "Ặ", "AÊ": "Ă",

    # Ký tự ê + dấu thanh
    "eù": "é", "eø": "è", "eû": "ẻ", "eõ": "ẽ", "eï": "ẹ",
    "eá": "ế", "eà": "ề", "eå": "ể", "eö": "ễ", "eã": "ễ", "eä": "ệ", "eâ": "ê",
    "EÁ": "Ế", "EÀ": "Ề", "EÅ": "Ể", "EÖ": "Ễ", "EÃ": "Ễ", "EÄ": "Ệ", "EÂ": "Ê",

    # Ký tự ô + dấu thanh
    "où": "ó", "oø": "ò", "oû": "ỏ", "oõ": "õ", "oï": "ọ",
    "oá": "ố", "oà": "ồ", "oå": "ổ", "oã": "ỗ", "oä": "ộ", "oâ": "ô",
    "OÁ": "Ố", "OÀ": "Ồ", "OÅ": "Ổ", "OÃ": "Ỗ", "OÄ": "Ộ", "OÂ": "Ô",

    # Ký tự u + dấu thanh
    "uù": "ú", "uø": "ù", "uû": "ủ", "uõ": "ũ", "uï": "ụ",
    "UÙ": "Ú", "UØ": "Ù", "UÛ": "Ủ", "UÕ": "Ũ", "UÏ": "Ụ",

    # Ký tự i + dấu thanh
    "í": "í", "ì": "ì", "æ": "ỉ", "ó": "ĩ", "ò": "ị",
    "Í": "Í", "Ì": "Ì", "Æ": "Ỉ", "Ó": "Ĩ", "Ò": "Ị",

    # Ký tự y + dấu thanh
    "yù": "ý", "yø": "ỳ", "yû": "ỷ", "yõ": "ỹ", "yï": "ỵ",
    "YÙ": "Ý", "YØ": "Ỳ", "YÛ": "Ỷ", "YÕ": "Ỹ", "YÏ": "Ỵ",

    # Chữ đ / Đ
    "ñ": "đ", "Ñ": "Đ",

    # Tổ hợp lỗi dấu kép trong PDF
    "oäï": "ộ", "Oäï": "Ộ",
    "eâä": "ệ", "Eâä": "Ệ",
    "Tâaây": "Tây", "Tâây": "Tây",
    "đêä": "đệ", "Đêä": "Đệ",
    "đồøng": "đồng", "Đồøng": "Đồng",
}

_SORTED_PATTERNS = sorted(VNI_TO_UNICODE_MAP.keys(), key=len, reverse=True)
_VNI_REGEX = re.compile("|".join(re.escape(k) for k in _SORTED_PATTERNS))

# Chuẩn hóa biến thể sót lại sau khi đổi VNI
POST_NORMALIZATIONS = {
    "leã": "lễ", "Leã": "Lễ",
    "deã": "dễ", "Deã": "Dễ",
    "treã": "trễ", "Treã": "Trễ",
    "meã": "mễ", "Meã": "Mễ",
    "mieãn": "miễn", "Mieãn": "Miễn",
    "Dieãn": "Diễn", "dieãn": "diễn",
    "Nieãn": "Niễn", "nieãn": "niễn",
    "Vieãn": "Viễn", "vieãn": "viễn",
    "saün": "sẵn", "Saün": "Sẵn",
    "mộït": "một", "Mộït": "Một",
    "Tâây": "Tây", "Tâaây": "Tây",
    "Thâïp": "Thập",
    "đêä": "đệ", "Đêä": "Đệ",
    "đồøng": "đồng", "Đồøng": "Đồng",
    "lieãu": "liễu", "nhieãu": "nhiễu", "tieãn": "tiễn",
    "choã": "chõa",
}


def clean_vni_artifacts(text: str) -> str:
    """Loại bỏ triệt để các biến thể lỗi ký tự VNI còn sót lại."""
    if not text:
        return ""
    for bad, good in POST_NORMALIZATIONS.items():
        text = text.replace(bad, good)
    text = re.sub(r'Tâ+y', 'Tây', text)
    text = re.sub(r'eã', 'ễ', text)
    text = re.sub(r'aü', 'ẵ', text)
    text = re.sub(r'oäï', 'ộ', text)
    text = re.sub(r'moäït', 'một', text)
    return text


def convert_vni_to_unicode(text: str) -> str:
    """Chuyển đổi chuỗi văn bản từ mã VNI-Windows sang Unicode chuẩn."""
    if not text:
        return ""
    converted = _VNI_REGEX.sub(lambda m: VNI_TO_UNICODE_MAP[m.group(0)], text)
    return clean_vni_artifacts(converted)


def _is_vni_font(font_name: str) -> bool:
    """Kiểm tra tên font có phải họ VNI hay không."""
    return font_name.upper().startswith("VNI-")


def _is_cjk_text(text: str) -> bool:
    """Kiểm tra khối văn bản có phải chữ CJK (Hán) hay không."""
    if not text.strip():
        return False
    cjk_count = 0
    total = 0
    for ch in text:
        if ch.isspace():
            continue
        total += 1
        cp = ord(ch)
        if 0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or 0x20000 <= cp <= 0x2A6DF:
            cjk_count += 1
    return total > 0 and (cjk_count / total) > 0.4


def extract_text_from_pdf(pdf_path: str) -> str:
    """Trích xuất và chuyển đổi văn bản từ PDF, xử lý phân biệt font VNI và Unicode."""
    doc = fitz.open(pdf_path)
    page_texts = []

    for page in doc:
        data = page.get_text("dict")
        lines_out = []

        for block in data["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                span_texts = []
                for span in line["spans"]:
                    font_name = span.get("font", "")
                    text = span.get("text", "")

                    if _is_vni_font(font_name) and not _is_cjk_text(text):
                        span_texts.append(convert_vni_to_unicode(text))
                    else:
                        # Font đã là Unicode hoặc là CJK: giữ nguyên
                        span_texts.append(clean_vni_artifacts(text) if not _is_cjk_text(text) else text)

                lines_out.append("".join(span_texts))

        page_texts.append("\n".join(lines_out))

    doc.close()
    return clean_vni_artifacts("\n".join(page_texts))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(extract_text_from_pdf(sys.argv[1]))
    else:
        sample = "Saéc tu Baùch Tröôïng thanh qui - Phaät phaùp taêng chuùng leã saün mộït Tâây"
        print("Gốc:       ", sample)
        print("Chuyển đổi:", convert_vni_to_unicode(sample))
