"""Module chuyển đổi bảng mã ký tự VNI-Windows sang Unicode dựng sẵn.

Áp dụng phương pháp Regex Tokenization một lượt (single-pass) để đảm bảo
tính toàn vẹn của dữ liệu và loại bỏ hoàn toàn lỗi ghi đè ký tự tuần tự.
"""

import re
from typing import Dict

# Bảng ánh xạ ký tự VNI-Windows sang Unicode
VNI_TO_UNICODE_MAP: Dict[str, str] = {
    # Tổ hợp ươ + dấu thanh
    "öôù": "ướ", "öôø": "ườ", "öôû": "ưở", "öôõ": "ưỡ", "öôï": "ượ", "öô": "ươ",
    "ÖÔÙ": "ƯỚ", "ÖÔØ": "ƯỜ", "ÖÔÛ": "ƯỞ", "ÖÔÕ": "ƯỠ", "ÖÔÏ": "ƯỢ", "ÖÔ": "ƯƠ",

    # Nguyên âm a và các biến thể
    "aù": "á", "aø": "à", "aû": "ả", "aõ": "ã", "aï": "ạ",
    "AÙ": "Á", "AØ": "À", "AÛ": "Ả", "AÕ": "Ã", "AÏ": "Ạ",
    "aá": "ấ", "aà": "ầ", "aå": "ẩ", "aã": "ẫ", "aä": "ậ", "aâ": "â",
    "AÁ": "Ấ", "AÀ": "Ầ", "AÅ": "Ẩ", "AÃ": "Ẫ", "AÄ": "Ậ", "AÂ": "Â",
    "aé": "ắ", "aè": "ằ", "aú": "ẳ", "aö": "ẵ", "aë": "ặ", "aê": "ă",
    "AÉ": "Ắ", "AÈ": "Ằ", "AÚ": "Ẳ", "AÖ": "Ẵ", "AË": "Ặ", "AÊ": "Ă",

    # Nguyên âm e và các biến thể
    "eù": "é", "eø": "è", "eû": "ẻ", "eõ": "ẽ", "eï": "ẹ",
    "EÙ": "É", "EØ": "È", "EÛ": "Ẻ", "EÕ": "Ẽ", "EÏ": "Ẹ",
    "eá": "ế", "eà": "ề", "eå": "ể", "eö": "ễ", "eä": "ệ", "eâ": "ê",
    "EÁ": "Ế", "EÀ": "Ề", "EÅ": "Ể", "EÖ": "Ễ", "EÄ": "Ệ", "EÂ": "Ê",

    # Nguyên âm o, ô, ơ và các biến thể
    "oá": "ố", "oà": "ồ", "oå": "ổ", "oã": "ỗ", "oä": "ộ", "oâ": "ô",
    "OÁ": "Ố", "OÀ": "Ồ", "OÅ": "Ổ", "OÃ": "Ỗ", "OÄ": "Ộ", "OÂ": "Ô",
    "où": "ó", "oø": "ò", "oû": "ỏ", "oõ": "õ", "oï": "ọ",
    "OÙ": "Ó", "OØ": "Ò", "OÛ": "Ỏ", "OÕ": "Õ", "OÏ": "Ọ",
    "ôù": "ớ", "ôø": "ờ", "ôû": "ở", "ôõ": "ỡ", "ôï": "ợ", "ô": "ơ",
    "ÔÙ": "Ớ", "ÔØ": "Ờ", "ÔÛ": "Ở", "ÔÕ": "Ỡ", "ÔÏ": "Ợ", "Ô": "Ơ",

    # Nguyên âm u, ư và các biến thể
    "uù": "ú", "uø": "ù", "uû": "ủ", "uõ": "ũ", "uï": "ụ",
    "UÙ": "Ú", "UØ": "Ù", "UÛ": "Ủ", "UÕ": "Ũ", "UÏ": "Ụ",
    "öù": "ứ", "öø": "ừ", "öû": "ử", "öõ": "ữ", "öï": "ự", "ö": "ư",
    "ÖÙ": "Ứ", "ÖØ": "Ừ", "ÖÛ": "Ử", "ÖÕ": "Ữ", "ÖÏ": "Ự", "Ö": "Ư",

    # Nguyên âm y và phụ âm đ
    "yù": "ý", "yø": "ỳ", "yû": "ỷ", "yõ": "ỹ", "yï": "ỵ",
    "YÙ": "Ý", "YØ": "Ỳ", "YÛ": "Ỷ", "YÕ": "Ỹ", "YÏ": "Ỵ",
    "æ": "ỉ", "Æ": "Ỉ",
    "ò": "ị", "Ò": "Ị",
    "ó": "ĩ", "Ó": "Ĩ",
    "ñ": "đ", "Ñ": "Đ",
}

# Biên dịch trước mẫu regex sắp xếp theo độ dài giảm dần
_SORTED_PATTERNS = sorted(VNI_TO_UNICODE_MAP.keys(), key=len, reverse=True)
_VNI_REGEX = re.compile("|".join(re.escape(k) for k in _SORTED_PATTERNS))


def convert_vni_to_unicode(text: str) -> str:
    """Chuyển đổi chuỗi văn bản từ mã VNI-Windows sang Unicode chuẩn."""
    if not text:
        return ""
    return _VNI_REGEX.sub(lambda match: VNI_TO_UNICODE_MAP[match.group(0)], text)


if __name__ == "__main__":
    sample_text = "Saéc tu Baùch Tröôïng thanh qui - Phaät phaùp taêng chuùng"
    print("Văn bản gốc:     ", sample_text)
    print("Văn bản chuyển đổi:", convert_vni_to_unicode(sample_text))
