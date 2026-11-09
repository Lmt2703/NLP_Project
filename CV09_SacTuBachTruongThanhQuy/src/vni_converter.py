# -*- coding: utf-8 -*-
"""
Module chuyển đổi bảng mã VNI-Windows sang Unicode dựng sẵn.
Được tối ưu hóa bằng Regex một lượt (single-pass regex replacement)
để khắc phục triệt để lỗi ghi đè ký tự tuần tự (sequential overwrite bug).
"""

import re

# Bảng ánh xạ VNI-Windows -> Unicode đầy đủ cho tài liệu Hán Nôm / Phật giáo
VNI_TO_UNICODE = {
    # Tổ hợp 4 ký tự (ươ + dấu)
    'öôù': 'ướ', 'öôø': 'ườ', 'öôû': 'ưở', 'öôõ': 'ưỡ', 'öôï': 'ượ', 'öô': 'ươ',
    'ÖÔÙ': 'ƯỚ', 'ÖÔØ': 'ƯỜ', 'ÖÔÛ': 'ƯỞ', 'ÖÔÕ': 'ƯỠ', 'ÖÔÏ': 'ƯỢ', 'ÖÔ': 'ƯƠ',

    # a + dấu thanh
    'aù': 'á', 'aø': 'à', 'aû': 'ả', 'aõ': 'ã', 'aï': 'ạ',
    'AÙ': 'Á', 'AØ': 'À', 'AÛ': 'Ả', 'AÕ': 'Ã', 'AÏ': 'Ạ',

    # â + dấu thanh
    'aá': 'ấ', 'aà': 'ầ', 'aå': 'ẩ', 'aã': 'ẫ', 'aä': 'ậ', 'aâ': 'â',
    'AÁ': 'Ấ', 'AÀ': 'Ầ', 'AÅ': 'Ẩ', 'AÃ': 'Ẫ', 'AÄ': 'Ậ', 'AÂ': 'Â',

    # ă + dấu thanh
    'aé': 'ắ', 'aè': 'ằ', 'aú': 'ẳ', 'aö': 'ẵ', 'aë': 'ặ', 'aê': 'ă',
    'AÉ': 'Ắ', 'AÈ': 'Ằ', 'AÚ': 'Ẳ', 'AÖ': 'Ẵ', 'AË': 'Ặ', 'AÊ': 'Ă',

    # e + dấu thanh
    'eù': 'é', 'eø': 'è', 'eû': 'ẻ', 'eõ': 'ẽ', 'eï': 'ẹ',
    'EÙ': 'É', 'EØ': 'È', 'EÛ': 'Ẻ', 'EÕ': 'Ẽ', 'EÏ': 'Ẹ',

    # ê + dấu thanh
    'eá': 'ế', 'eà': 'ề', 'eå': 'ể', 'eö': 'ễ', 'eä': 'ệ', 'eâ': 'ê',
    'EÁ': 'Ế', 'EÀ': 'Ề', 'EÅ': 'Ể', 'EÖ': 'Ễ', 'EÄ': 'Ệ', 'EÂ': 'Ê',

    # ô + dấu thanh (tổ hợp o + ...)
    'oá': 'ố', 'oà': 'ồ', 'oå': 'ổ', 'oã': 'ỗ', 'oä': 'ộ', 'oâ': 'ô',
    'OÁ': 'Ố', 'OÀ': 'Ồ', 'OÅ': 'Ổ', 'OÃ': 'Ỗ', 'OÄ': 'Ộ', 'OÂ': 'Ô',

    # o + dấu thanh đơn
    'où': 'ó', 'oø': 'ò', 'oû': 'ỏ', 'oõ': 'õ', 'oï': 'ọ',
    'OÙ': 'Ó', 'OØ': 'Ò', 'OÛ': 'Ỏ', 'OÕ': 'Õ', 'OÏ': 'Ọ',

    # ơ + dấu thanh (tổ hợp từ ô + ...)
    'ôù': 'ớ', 'ôø': 'ờ', 'ôû': 'ở', 'ôõ': 'ỡ', 'ôï': 'ợ', 'ô': 'ơ',
    'ÔÙ': 'Ớ', 'ÔØ': 'Ờ', 'ÔÛ': 'Ở', 'ÔÕ': 'Ỡ', 'ÔÏ': 'Ợ', 'Ô': 'Ơ',

    # u + dấu thanh
    'uù': 'ú', 'uø': 'ù', 'uû': 'ủ', 'uõ': 'ũ', 'uï': 'ụ',
    'UÙ': 'Ú', 'UØ': 'Ù', 'UÛ': 'Ủ', 'UÕ': 'Ũ', 'UÏ': 'Ụ',

    # ư + dấu thanh (tổ hợp từ ö + ...)
    'öù': 'ứ', 'öø': 'ừ', 'öû': 'ử', 'öõ': 'ữ', 'öï': 'ự', 'ö': 'ư',
    'ÖÙ': 'Ứ', 'ÖØ': 'Ừ', 'ÖÛ': 'Ử', 'ÖÕ': 'Ữ', 'ÖÏ': 'Ự', 'Ö': 'Ư',

    # y + dấu thanh
    'yù': 'ý', 'yø': 'ỳ', 'yû': 'ỷ', 'yõ': 'ỹ', 'yï': 'ỵ',
    'YÙ': 'Ý', 'YØ': 'Ỳ', 'YÛ': 'Ỷ', 'YÕ': 'Ỹ', 'YÏ': 'Ỵ',

    # Ký tự đơn lẻ đặc biệt trong VNI-Windows
    'æ': 'ỉ', 'Æ': 'Ỉ',
    'ò': 'ị', 'Ò': 'Ị',
    'ó': 'ĩ', 'Ó': 'Ĩ',
    'ñ': 'đ', 'Ñ': 'Đ',
}

# Compile Regex pattern theo độ dài giảm dần để ưu tiên cụm dài trước
_SORTED_KEYS = sorted(VNI_TO_UNICODE.keys(), key=len, reverse=True)
_PATTERN = re.compile('|'.join(re.escape(k) for k in _SORTED_KEYS))


def convert_vni_to_unicode(text: str) -> str:
    """Chuyển chuỗi mã VNI-Windows sang Unicode dựng sẵn bằng regex thay thế 1 lượt."""
    if not text:
        return ""
    return _PATTERN.sub(lambda m: VNI_TO_UNICODE[m.group(0)], text)


if __name__ == "__main__":
    sample = "Saéc tu Baùch Tröôïng thanh qui coâng vieäc nhaân ñoù hoaèng döông Phaät phaùp"
    print("Gốc: ", sample)
    print("Đổi: ", convert_vni_to_unicode(sample))
