"""Module trích xuất và làm sạch văn bản Hán - Việt từ tài liệu PDF.

Quy trình xử lý hoàn thiện (Phiên bản v3):
1. Trích xuất lớp văn bản phân biệt font (VNI-Times vs Unicode) từ PDF qua extract_text_from_pdf.
2. Cắt bỏ triệt để 7 cụm 'LỜI BÀN' / 'LỜI BAØN' / 'LÔØI BAØN' của dịch giả khỏi văn bản nguồn Quyển 4 trước khi dóng hàng.
3. Cắt bỏ toàn bộ trang lưu chiểu, ban ấn tống và danh sách công đức cúng dường ở cuối Quyển 4.
4. Xử lý triệt để các cấu trúc dồn bản dịch trong Quyển 7:
   - Bản trướng thức: Ánh xạ chuẩn xác 35 khoản thu chi 1-1, đồng bộ số tiền Hán - Việt (15 quan nhập liệm + 1 quan đánh não bạt...).
   - Loại bỏ trùng lặp và phiên âm ở cuối Bản trướng ([1149c28], [1150a01]).
   - Thảo đơn thức: Ánh xạ chính xác 6 dòng biểu mẫu 1-1.
   - Nguyệt phần tu tri: Ánh xạ chính xác 12 tháng lịch tiết 1-1.
5. Loại bỏ sơ đồ vị trí ngồi (Cấp 1, Cấp 2, Cấp 3...) trước [1152b28] trong Quyển 7.
6. Gom đúng nhóm biểu mẫu hành chính:
   - Quyển 4: [1135c26] cho Mẫu văn trạng + Bì thư, [1136b15] cho Mẫu bảng thức.
   - Quyển 7: Tách chữ '茶狀' ở [1154b15] để vế '但添設知事位次。' không bị lệch nghĩa.
7. Chuẩn hóa tất cả chuỗi viết tắt 'v. v…', 'v. v...', 'v...' thành 'v.v...'.
"""

import os
import re
from typing import Dict, List

from vni_converter import extract_text_from_pdf, clean_vni_artifacts

NOISE_PATTERNS = [
    r"^\s*\d+\s*$",
    r"SẮC TU BÁCH TRƯỢNG THANH QUI.*",
    r"Quyển thứ \d+",
    r"Quyển \d+",
    r"Quyeån \d+",
    r"卷第.*",
    r"勅修百丈清規卷第.*",
]

TAG_CORRECTIONS = {
    "[1134a02]": "[1134a03]",
    "[1150b16]": "[1150b17]",
}

CBETA_PATTERN = re.compile(r"(\[\d{4}[a-z]\d{2}\])(.*?)(?=\[\d{4}[a-z]\d{2}\]|\Z)", re.DOTALL)

# Ánh xạ 35 khoản mục chi tiết của Bản trướng thức (Quyển 7) chuẩn xác theo từng số tiền
BAN_TRUONG_MAP = [
    ('[1149b11]', r"Nay xin trình bày đầy đủ các hạng mục.*?\(đem bán đấu giá\)\."),
    ('[1149b12]', r"Về phần thu gồm: 1000 quan tiền.*?chép rõ từng hạng mục\)\."),
    ('[1149b13]', r"Về phần chi gồm: 91 quan tiền.*?15 quan tiền hồi khám:"),
    ('[1149b15]', r"3 quan tiền: hồi tế - 3 quan tiền: cúng cháo"),
    ('[1149b16]', r"1 quan tiền: dầu đèn tại kim quan – 10 quan tiền:.*?tuyết liễu\."),
    ('[1149b17]', r"1 quan tiền: cạo tóc\..*?2 quan 500 tiền: di chuyển kim quan\."),
    ('[1149b18]', r"500 tiền: nấu nước tắm\..*?2 quan tiền: tắm người chết\."),
    ('[1149b19]', r"1 quan tiền: người hầu kim quan dùng cơm cháo\..*?500 tiền: Khố ty khách đầu nhờ sắm vật cúng\."),
    ('[1149b20]', r"500 tiền: đinh dùng treo các đồ cúng\..*?500 tiền: ban trai soạn dọn chén bát\."),
    ('[1149b21]', r"500 tiền: thủ kho xuất chi về vật tế lễ\..*?500 tiền: đầu bếp nấu cơm\."),
    ('[1149b22]', r"500 tiền: khố ty trà đầu dâng trà nước\..*?500 tiền: tham đầu sai bảo lao công\."),
    ('[1149b23]', r"2 quan tiền: Đường ty hành giả thông báo đại chúng\..*?500 tiền: giám tác sai bảo lao công\."),
    ('[1149b24]', r"500 tiền: phương trượng cho gọi người bưng hộp hương\..*?10 quan tiền: hành đường tụng kinh\."),
    ('[1149b25]', r"1 quan tiền: phụ thêm cho hành giả Đường ty đánh bản\..*?2 quan tiền: người hầu trà cung cấp cho 4 liêu\."),
    # [1149b26]: 15 quan di chuyển kim quan + 1 quan đánh não bạt
    ('[1149b26]', r"15 quan tiền: nhập liệm\.\s*1 quan tiền: đánh não bạt\."),
    # [1149b27]: 3 quan đánh nhạc lễ + 3 quan 6 người khiêng hương án
    ('[1149b27]', r"3 quan tiền: đánh nhạc lễ\.\s*3 quan tiền: sáu người khiêng hương án, cầm cờ đèn\."),
    # [1149b28]: 500 tiền tuyết liễu + 1 quan châm lửa thiêu xác
    ('[1149b28]', r"500 tiền: biếu cho những kẻ cầm nhành cây tuyết liễu.*?\s*1 quan tiền: châm lửa thiêu xác\."),
    # [1149b29]: 3 quan người phương trượng đưa tang + 1 quan lao công 4 liêu khiêng bàn ghế
    ('[1149b29]', r"3 quan tiền: những người hầu hạ Phương trượng đưa tang\.\s*1 quan tiền: lao công của 4 liêu khiêng bàn ghế\."),
    # [1149c01]: 500 tiền trình y + 500 tiền rao đấu giá y vật
    ('[1149c01]', r"500 tiền: phụ thêm cho hành giả Đường ty trình y\..*?500 tiền: Hành giả Đường ty rao đấu giá\s*y vật\."),
    # [1149c02]: 500 tiền soạn phiếu + 500 tiền thu y
    ('[1149c02]', r"500 tiền: phụ thêm cho cung đầu soạn phiếu rao đấu.*?500 tiền: cung đầu thu y\."),
    # [1149c03]: 500 tiền rút thẻ + 500 tiền thu cốt
    ('[1149c03]', r"500 tiền: hành giả Xướng thực rút thẻ\..*?500 tiền: thu cốt\."),
    # [1149c04]: 1 quan bưng hộp than + 1 quan trực tháp chi lặt vặt
    ('[1149c04]', r"1 quan tiền: bưng hộp than\..*?1 quan tiền: \(trực tháp\) chi lặt vặt"),
    # [1149c05]: Chi 270 quan
    ('[1149c05]', r"Chi 270 quan: theo các khoản chi tiêu trong bản trướng.*?Kể về chi tiêu các việc kể trên\."),
    # [1149c06]: Chi 135 quan
    ('[1149c06]', r"Chi 135 quan: tiền công đức các buổi lễ\."),
    # [1149c07]: Khai cụ nội 20 quan
    ('[1149c07]', r"Khai cụ nội 20 quan: lễ trà tỳ\."),
    # [1149c08]: 10 quan phụ thêm + 40 quan đậy nắp quan...
    ('[1149c08]', r"10 quan: phụ thêm lễ trà tỳ\.\s*40 quan: đậy nắp quan, di quan, di cốt, nhập tháp\."),
    # [1149c09]: 20 quan thêm cho 4 buổi lễ + 30 quan Duy na làm lễ sơn đầu...
    ('[1149c09]', r"20 quan: thêm cho 4 buổi lễ kể trên\.\s*30 quan: Duy na làm lễ sơn đầu, thị giả của Tri khách cầm trướng\."),
    # [1149c10]: 15 quan phụ thêm
    ('[1149c10]', r"15 quan: Phụ thêm 3 Phật sự kể trên\."),
    # [1149c11]: Chi 15 quan: Thủ tọa chủ tang...
    ('[1149c11]', r"Chi 15 quan: Thủ tọa chủ tang, Đô tự đưa tang, Duy-.*?\b5 quan\."),
    # [1149c12]: Chi 9 quan: Tri khách tụng kinh...
    ('[1149c12]', r"Chi 9 quan: Tri khách tụng kinh.*?Trực tuế đưa lửa 1 quan\."),
    # [1149c14]: Chi 15 quan: Phương trượng, lưỡng tự...
    ('[1149c14]', r"Chi 15 quan: Phương trượng, lưỡng tự.*?điểm tâm phương trượng 2 phần\."),
    # [1149c15]: Chi 20 quan: Phương trượng Lưỡng tự thiêm đơn...
    ('[1149c15]', r"Chi 20 quan: Phương trượng Lưỡng tự thiêm đơn, phương trượng 2 phần\."),
    # [1149c16]: Chi 444 quan 500 tiền
    ('[1149c16]', r"Chi 444 quan 500 tiền: biếu cho Tăng chúng tụng kinh tại.*?(?:nữa|nửa)\s*phần người khác\."),
    # [1149c18]: Ngoại trừ các khoản chi ra...
    ('[1149c18]', r"Ngoại trừ các khoản chi ra, Đường ty còn thu được 500 tiền.*?như đã nêu trên\."),
    # [1149c19]-[1150a01]: Ngày... tháng... năm... + Danh sách chức sự ký tên
    ('[1149c19]-[1150a01]', r"Ngày … tháng … năm Hành giả Đường ty mỗ giáp.*?Trụ trì\s*\(nt\)"),
]

# 22 lỗi chính tả/gõ dấu từ nguyên bản scan và OCR cần chuẩn hóa
TYPO_REPLACEMENTS = [
    (r'\bniêu hiệu\b', 'niên hiệu'),
    (r'\bDó đó\b', 'Do đó'),
    (r'\blưõng\b', 'lưỡng'),
    (r'\bngười củ\b', 'người cũ'),
    (r'\bgian tri\b', 'gian trái'),
    (r'\bnữa phần\b', 'nửa phần'),
    (r'\bbửa\b', 'bữa'),
    (r'\bchậm rải\b', 'chậm rãi'),
    (r'\bSai khi\b', 'Sau khi'),
    (r'\bsai khi\b', 'sau khi'),
    (r'\bNgười giữa liêu\b', 'Người giữ liêu'),
    (r'\bngười giữa liêu\b', 'người giữ liêu'),
    (r'\bLăng mghiêm\b', 'Lăng nghiêm'),
    (r'\btruớc\b', 'trước'),
    (r'\bTruớc\b', 'Trước'),
    (r'\bphứơc\b', 'phước'),
    (r'\bPhứơc\b', 'Phước'),
    (r'\bthuợng\b', 'thượng'),
    (r'\bThuợng\b', 'Thượng'),
    (r'\bhuớng\b', 'hướng'),
    (r'\bHuớng\b', 'Hướng'),
    (r'\bĐô tử\b', 'Đô tự'),
    (r'\bngừơi\b', 'người'),
    (r'\bNgừơi\b', 'Người'),
    (r'\btrựơng\b', 'trượng'),
    (r'\bTrựơng\b', 'Trượng'),
    (r'\blập bang\b', 'lập ban'),
    (r'\btủ khăn\b', 'phủ khăn'),
    (r'\bhứớng\b', 'hướng'),
    (r'\bHứớng\b', 'Hướng'),
    (r'\bsọan\b', 'soạn'),
    (r'\bSọan\b', 'Soạn'),
    (r'\bchổ\b', 'chỗ'),
    (r'\bChổ\b', 'Chỗ'),
    (r'\bmâu-\s*ni\b', 'Mâu-ni'),
    (r'\bMâu-\s*ni\b', 'Mâu-ni'),
    (r'\bcựu ban trị sự\b', 'cựu ban tri sự'),
    (r'\bduy-\s*na\b', 'duy-na'),
    (r'\bDuy-\s*na\b', 'Duy-na'),
    (r'\bPhương trựợng\b', 'Phương trượng'),
    (r'\bphương trựợng\b', 'phương trượng'),
]
THAO_DON_MAP = [
    ('[1150b17]', 'Giới lạp của Tăng chúng: Giới của Đức Uy Âm Vương, Tôn giả Kiều-trần-như.'),
    ('[1150b18]', 'Đường đầu Hòa thượng: Năm Chí Nguyện mấy giới, Năm Nguyên Trinh mấy giới.'),
    ('[1150b19]', 'Thượng tọa mỗ giáp, Thượng tọa mỗ giáp, Năm Đại đức mấy giới.'),
    ('[1150b20]', 'Năm Chí Đại mấy giới, Thượng tọa mỗ giáp, Thượng tọa mỗ giáp.'),
    ('[1150b21]', 'Kính xin ghi đầy đủ như trên. Nếu có sai sót, xin các vị tự cải chính giúp. Rất mong được sự thể tất.'),
    ('[1150b22]', 'Hôm nay, ngày ….. tháng …... Đường ty mỗ giáp, xin ghi đầy đủ như vậy.')
]


def is_cjk_char(ch: str) -> bool:
    """Kiểm tra ký tự có thuộc dải mã CJK (chữ Hán) hay không."""
    code = ord(ch)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0x20000 <= code <= 0x2A6DF)


def clean_han_text(raw_text: str) -> str:
    """Làm sạch văn bản chữ Hán: giữ chữ CJK và dấu câu Hán chuẩn, loại bỏ tiêu đề Latin và chú thích CBETA."""
    text = re.sub(r"\[(?:\d+|＊|\*)\]", "", raw_text)
    text = re.sub(r"勅修百丈清規\s*$", "", text)
    valid_lines = []
    for line in text.splitlines():
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

    joined = re.sub(r"\s+", " ", " ".join(valid_lines)).strip()
    joined = re.sub(r"(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])", "", joined)
    joined = re.sub(r"勅修百丈清規\s*$", "", joined).strip()
    return joined


def clean_viet_text(raw_text: str) -> str:
    """Làm sạch văn bản tiếng Việt: loại bỏ lời bàn, sơ đồ vị trí, rác chữ Hán và tiêu đề thừa."""
    text = re.sub(r"(?:LỜI|LÔØI)\s*(?:BÀN|BAØN).*?(?=\[\d{4}[a-z]\d{2}\]|\Z|\*\s*\*|\*\s*\*\s*\*)", "", raw_text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"Mô hình bữa đãi nước.*?(?=\*|\Z|四節|TỨ TIẾT|\[\d{4}[a-z]\d{2}\])", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\*+", "", text)
    # Loại bỏ triệt để mọi ký tự CJK bị rò rỉ vào khối tiếng Việt
    text = "".join(" " if is_cjk_char(c) else c for c in text)

    valid_lines = []
    header_filter = re.compile(
        r"^(?:SẮC TU|CHƯƠNG \d+|LƯỠNG TỰ\s+CHƯƠNG|LƯỠNG TỰ\s+BAN\s+THỦ|BẢN TRƯỚNG\s+THỨC|ĐẠI TRÍ|ĐẠI LONG|TRỤ TRÌ CHÙA|Chương [A-ZÀ-Ỹa-ỹ\s]+ hết|Tiết lạp chương chung|Quyển \d+|Cấp \d+:)",
        re.IGNORECASE,
    )
    for line in text.splitlines():
        line = line.strip()
        if not line or header_filter.match(line):
            continue
        if re.match(r"^Mô hình\s*[:\-\d]*$", line, re.IGNORECASE):
            continue
        if re.match(r"^\d+$", line) or re.match(r"^[\(\)\s\.\,\-\_]+$", line):
            continue
        if re.match(r"^[\d\s\,\-\.]+khách", line, re.IGNORECASE) or re.match(r"^[\d\s\,\-\.]+chủ", line, re.IGNORECASE):
            continue
        valid_lines.append(line)

    text = " ".join(valid_lines)
    text = clean_vni_artifacts(text)
    for pat, rep in TYPO_REPLACEMENTS:
        text = re.sub(pat, rep, text)
    # Ghép lời giải thích tệ đoan điền trang vào câu trước
    text = re.sub(
        r'(Đây là vụ việc thứ ba\.)\s*(\(Trong ban ruộng vườn có ba loại tệ đoan lớn[^)]*\)\.?)',
        r'Đây là vụ việc thứ ba \2',
        text
    )
    # Chuẩn hóa các biến thể viết tắt v. v...
    text = re.sub(r"\bv\.\s*v[…\.]*", "v.v...", text, flags=re.IGNORECASE)
    text = re.sub(r"\bv[…]+", "v.v...", text, flags=re.IGNORECASE)
    text = re.sub(r"\.{2,}", "...", text)
    return re.sub(r"\s+", " ", text).strip()


def apply_han_fixes(tag: str, han: str, is_q4: bool) -> str:
    """Tinh chỉnh dấu ngắt câu Hán trên chuỗi đã làm sạch để đồng bộ 1-1 với bản dịch tiếng Việt."""
    if not han:
        return han

    if is_q4:
        # Bổ sung tiêu đề khuyết cho mục Thị giả [1131c09]
        if tag == '[1131c09]' and not han.startswith('侍者(燒香'):
            han = '侍者(燒香書狀請客)。' + han
            han = han.replace('侍者之職最為近密。觀道德於前後。聽教誨於朝夕。', '侍者之職最為近密觀道德於前後聽教誨於朝夕。')
            han = han.replace('親炙參扣。期法道底于大成。', '親炙參扣期法道底于大成。')

        elif tag == '[1131a24]':
            han = han.replace('凡看經者初入經堂。先白堂主同到藏司相看。送歸按位對觸禮一拜。', '凡看經者初入經堂先白堂主同到藏司相看送歸按位對觸禮一拜。')
            han = han.replace('今各僧看經多就眾寮。而藏殿無設几案者。', '今各僧看經多就眾寮而藏殿無設几案者。')
            han = han.replace('然充其名當盡其職。函帙目錄常加點對缺者補完。', '然充其名當盡其職函帙目錄常加點對。缺者補完')
            han = han.replace('缺者補完。蒸潤者焙拭。', '缺者補完蒸潤者焙拭。')
            han = han.replace('若大眾披閱則藏主置簿。照堂司所排經單列名。逐函交付。', '若大眾披閱則藏主置簿照堂司所排經單列名逐函交付。')
            han = han.replace('看畢照簿交收入藏。庶無散失。', '看畢照簿交收入藏庶無散失。')
            han = han.replace('推原吾宗既曰教外別傳。猶命僧專司其藏者何也。', '推原吾宗既曰教外別傳猶命僧專司其藏者何也。')
            han = han.replace('以佛之所言所行為教律。而僧有不遵佛之言行乎。', '以佛之所言所行為教律而僧有不遵佛之言行乎。')
            han = han.replace('特吾之所證所得不溺於文字。而超乎言行之表。以見夫自性之妙焉。', '特吾之所證所得不溺於文字而超乎言行之表以見夫自性之妙焉。')
            han = han.replace('又祖之意。欲吾徒遍探諸部與外之百氏。期以折衝外侮應變無窮。', '又祖之意欲吾徒遍探諸部與外之百氏期以折衝外侮應變無窮。')

        elif tag == '[1131b18]':
            han = han.replace('凡遇開浴。齋前掛開浴牌。', '凡遇開浴齋前掛開浴牌。')
            han = han.replace('寒月五日一浴。暑天每日淋汗。', '寒月五日一浴暑天每日淋汗。')
            han = han.replace('鋪設浴室。掛手巾。出面盆拖鞋脚布。', '鋪設浴室掛手巾出面盆拖鞋脚布。')
            han = han.replace('齋罷浴頭覆維那首座住持畢。鳴鼓三下。浴聖桶內皆著少湯。燒香禮拜想請聖浴。', '齋罷浴頭覆維那首座住持畢鳴鼓三下浴聖桶內皆著少湯燒香禮拜想請聖浴。')
            han = han.replace('此時住持方入。以屏風遮隔而浴。', '此時住持方入以屏風遮隔而浴。')
            han = han.replace('監作行者知事居末浴。就彈壓之。併點視。令息竈中火及炭煤。水洒乾淨有餘柴搬於遠處。', '監作行者知事居末浴就彈壓之併點視令息竈中火及炭煤水洒乾淨有餘柴搬於遠處。')
            han = han.replace('其入浴資次當刊揭浴室外(今時謂住持殿頭首後浴。知事殿行者後浴。非也。如往持有故欲同頭首先浴。則不用設屏障。不入小閣內。只頭首板頭解衣)室內掛小板旁釘小牌。', '其入浴資次當刊揭浴室外(今時謂住持殿頭首後浴，知事殿行者後浴，非也，如往持有故欲同頭首先浴，則不用設屏障，不入小閣內，只頭首板頭解衣)。室內掛小板旁釘小牌')
            han = han.replace('室內掛小板旁釘小牌。書云(鳴板一聲添湯。', '室內掛小板旁釘小牌書云(鳴板一聲添湯。')
            han = han.replace('三聲則止。以此為節)如施主設浴。則課經回向能妙觸宣明。', '三聲則止以此為節)。如施主設浴則課經回向能妙觸宣明。')

        elif tag == '[1133c03]':
            han = (
                han.replace('特賜開允)受請人', '特賜開允)。受請人')
                .replace('不敢有違)答云', '不敢有違)。答云')
                .replace('仰乞垂情)謝已', '仰乞垂情)。謝已')
                .replace('不勝愧悚)仍往', '不勝愧悚)。仍往')
            )

        elif tag == '[1133c27]':
            han = han.replace('住持須預稟露。如有允意。方丈先請茶。兩序光伴即鳴鼓陞座。更不報眾。', '住持須預稟露如有允意方丈先請茶兩序光伴。即鳴鼓陞座更不報眾。')
            han = han.replace('下座與大眾同伸拜請。鳴鍾送歸寮。', '下座與大眾同伸拜請鳴鍾送歸寮。')

        elif tag in ('[1134a03]', '[1134a03]-[1134a05]'):
            han = '堂頭和尚今晨齋退就雲堂點茶特為新命首座聊旌陳賀之儀。仍請諸知事大眾同垂光伴。今月日侍司某敬白。'

        elif tag == '[1134a07]':
            han = han.replace('下情無任愧懷之至)再展', '下情無任愧懷之至)。再展')
            han = han.replace('轉位獻湯(咸淳規揖坐揖香揖湯。至今諸方行之。', '轉位獻湯(咸淳規揖坐揖香揖湯至今諸方行之。')
            han = han.replace('或謂當晚有特為此可免', '或謂當晚有特為。此可免')
            han = han.replace('在往持意)湯罷謝禮。或展或免。', '在往持意)。湯罷謝禮或展或免。')
            han = han.replace('各喝云(兩班勤舊送以次舊頭首知事歸蒙堂前資)禮亦如前。', '各喝云(兩班勤舊送以次舊頭首知事歸蒙堂前資)。禮亦如前。')
            han = han.replace('送住持出。寮主先相接。交互轉身對。觸禮一拜。不送出。', '送住持出寮主先相接交互轉身對觸禮一拜不送出。')
            han = han.replace('然後受賀俱畢新舊人各懷香。即詣方丈拜謝。', '然後受賀俱畢新舊人各懷香即詣方丈拜謝。')
            han = han.replace('新人香係庫司備。謝畢。', '新人香係庫司備。謝畢')
            han = han.replace('謝畢。新舊人同巡寮方丈請半齋點心。', '謝畢新舊人同巡寮。方丈請半齋點心。')
            han = han.replace('齋時草飯仍請西堂勤舊。光伴列職雜務待請兩序了。別日詣堂司告退。', '齋時草飯仍請西堂勤舊光伴。列職雜務待請兩序了別日詣堂司告退。')

        elif tag == '[1134c14]':
            han = han.replace('維那攸賀而已。勿視為常) 方丈行者', '維那攸賀而已勿視為常)。方丈行者')
            han = han.replace('維那攸賀而已。勿視為常)方丈行者', '維那攸賀而已勿視為常)。方丈行者')

        elif tag == '[1135a16]':
            han = han.replace('(小座湯禮同)至晚湯果次日粥罷。請新舊人茶。庫司亦請茶。然不及赴。赴方丈茶罷。却往致謝。', '(小座湯禮同)。至晚湯果。次日粥罷請新舊人茶庫司亦請茶然不及赴赴方丈茶罷却往致謝。')

        elif tag == '[1135b07]':
            han = han.replace('伏望降重)客頭隨後請云', '伏望降重)。客頭隨後請云')
            han = han.replace('就坐藥石)及請', '就坐藥石)。及請')

        elif tag in ('[1135c26]', '[1135c26]-[1135c30]'):
            han = han.replace('伏望降重)呈納狀訖', '伏望降重)。呈納狀訖')

        elif tag == '[1136a05]':
            han = han.replace('就寮獻茶)隨令茶頭', '就寮獻茶)。隨令茶頭')

    else:  # Quyển 7
        if tag == '[1150b06]':
            han = han.replace('喧譁撓眾犯者合擯', '喧譁撓眾。犯者合擯')

        elif tag == '[1150c11]':
            han = han.replace('惟鉢位圖(遍呈單。寮', '惟鉢位圖遍呈單寮。')
            han = han.replace('惟鉢位圖(遍呈單寮', '惟鉢位圖遍呈單寮。')
            han = han.replace('排被鉢位)(伏幸悉眾', '排被鉢位)。(伏幸悉眾')
            han = han.replace('草單已定。堂司依戒臘寫楞嚴圖念誦巡堂圖被位圖鉢位圖(式前後互見)戒臘牌。', '草單已定堂司依戒臘寫楞嚴圖念誦巡堂圖被位圖鉢位圖(式前後互見)戒臘牌。')
            han = han.replace('除單寮西堂首座勤舊。排板頭外。其餘並依戒臘。', '除單寮西堂首座勤舊排板頭外其餘並依戒臘。')
            han = han.replace('舊以送蒙堂者排副鉢。後因爭兢不排。', '舊以送蒙堂者排副鉢後因爭兢不排。')
            han = han.replace('悉依戒次具草本。呈首座。次呈住持看定方寫諸圖。', '悉依戒次具草本呈首座次呈住持看定方寫諸圖。')
            han = han.replace('被鉢位圖叉當預出。書小榜報眾云。粥罷排被鉢位)(伏幸悉眾', '被鉢位圖叉當預出書小榜報眾云(粥罷排被鉢位伏幸悉眾)。')
            han = han.replace('今月日堂司某白)貼僧堂前後門。', '今月日堂司某白貼僧堂前後門。')
            han = han.replace('(伏幸悉眾今月日堂司某白', '伏幸悉眾今月日堂司某白')

        elif tag == '[1152a09]':
            han = han.replace('摩登慶喜妙協冥權世尊文殊特彰化軌', '摩登慶喜妙協冥權。世尊文殊特彰化軌。')
            han = han.replace('闡一代教觀則有觀有教示密因修證而無證無修', '闡一代教觀則有觀有教。示密因修證而無證無修。')
            han = han.replace('明真見而息諸塵。空花無蒂。居正定以制群動。止水不波。', '明真見而息諸塵空花無蒂。居正定以制群動止水不波。')
            han = han.replace('顧末裔之何知。誦遺言而自警。', '顧末裔之何知誦遺言而自警。')
            han = han.replace('伏願促恒河沙劫為一念。無間長期。會十方剎土以同居。咸成正覺', '伏願促恒河沙劫為一念無間長期。會十方剎土以同居咸成正覺。')
            han = han.replace('(滿散)睠此林園宛爾祇桓精舍現前海眾儼然一會靈山', '(滿散)睠此林園宛爾祇桓精舍。現前海眾儼然一會靈山。')
            han = han.replace('括大千於微塵融三際於當念', '括大千於微塵。融三際於當念。')
            han = han.replace('屬休夏之自恣。無犯無持。總萬象以交參。孰凡孰聖。', '屬休夏之自恣無犯無持。總萬象以交參孰凡孰聖。')
            han = han.replace('人人妙覺。剎剎毘盧示現千百億身超越五十七位', '人人妙覺剎剎毘盧。示現千百億身超越五十七位。')
            han = han.replace('以指喻指之非指。指亦俱亡。似空藏空而合空。空寧可餉', '以指喻指之非指指亦俱亡。似空藏空而合空空寧可餉。')
            han = han.replace('為憐幼穉特獎愚蒙。遵遺教以受持。賴安居之無障', '為憐幼穉特獎愚蒙。遵遺教以受持賴安居之無障。')
            han = han.replace('伏願奢摩寂靜具足諸塵勞門大用繁興等入首楞嚴定', '伏願奢摩寂靜具足諸塵勞門。大用繁興等入首楞嚴定。')

        elif tag == '[1152b02]':
            han = han.replace('四節講行按古有三座湯', '四節講行。按古有三座湯。')
            han = han.replace('第二座分四出。頭首一出。知事二出西序勤舊三出。東序勤舊四出。西堂光伴。', '第二座分四出頭首一出知事二出西序勤舊三出東序勤舊四出。西堂光伴。')
            han = han.replace('第三座位。多分六出。本山辦事。諸方辦事。隨職高下分坐。', '第三座位多分六出本山辦事諸方辦事隨職高下分坐。')
            han = han.replace('職同者次之。首座光伴', '職同者次之首座光伴。')
            han = han.replace('侍司預備草圖。呈方丈議定。', '侍司預備草圖呈方丈議定。')
            han = han.replace('至日依名書照牌。午後備卓袱。', '至日依名書照牌午後。備卓袱。')
            han = han.replace('堂頭和尚請今晚就寢堂。特為獻湯。', '堂頭和尚請今晚就寢堂特為獻湯。')
            han = han.replace('方丈和尚參前請就寢堂。特為獻湯。', '方丈和尚參前請就寢堂特為獻湯。')

        elif tag in ('[1153a23]', '[1153a23]-[1153a25]'):
            han = '庫司今晚就雲堂點湯一中特為首座大眾聊旌某節之儀。伏望眾慈同垂光降。今月日庫司比丘某等敬白。'

        elif tag in ('[1154b04]', '[1154b04]-[1154b07]'):
            han = '堂頭和尚今晨齋退就雲堂點茶一中。特為首座大眾聊旌某節之儀。仍請諸知事同垂光降。今月日侍司某敬白。'

        elif tag == '[1153a27]':
            han = han.replace('復位喝云。首座禮謝大眾。對觸禮三拜畢。', '復位喝云(首座禮謝大眾)對觸禮三拜畢。')
            han = han.replace('知事入燒香展拜巡堂畢排立聖僧板頭。喝云 (知事禮謝大眾)對觸禮三拜畢不出堂。', '知事入燒香展拜巡堂畢排立聖僧板頭。喝云(知事禮謝大眾)對觸禮三拜畢。不出堂。')
            han = han.replace('知事入燒香展拜巡堂畢排立聖僧板頭。喝云(知事禮謝大眾)對觸禮三拜畢不出堂。', '知事入燒香展拜巡堂畢排立聖僧板頭。喝云(知事禮謝大眾)對觸禮三拜畢。不出堂。')

        elif tag == '[1155a02]':
            han = han.replace('初四五間告香普說初八日)佛誕浴佛。', '初四五間告香普說。初八日)佛誕浴佛。')
            han = han.replace('庫司預造黑飯。方丈請大眾。夏前點心。', '庫司預造黑飯方丈請大眾夏前點心。')
            han = han.replace('十五日結制(候天氣僧堂內下暖簾上涼簾)。', '十五日結制。(候天氣僧堂內下暖簾上涼簾)。')

        elif tag == '[1155a17]':
            han = han.replace('九月初一日首座復鳴坐禪板。堂司提調', '九月初一日首座復鳴坐禪板堂司提調')
            han = han.replace('堂司提調糊僧堂窓。下涼簾上暖簾。', '堂司提調糊僧堂窓下涼簾上暖簾。')
            han = han.replace('重陽日早晨知事', '重陽日早晨。知事')
            han = han.replace('知事燒香點茱萸茶。住持上堂', '知事燒香點茱萸茶住持上堂')

    return re.sub(r'。+', '。', han)


def extract_book(pdf_path: str) -> List[Dict[str, str]]:
    """Trích xuất và cấu trúc hóa toàn bộ văn bản Hán - Việt từ tệp PDF theo đúng tuần tự."""
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"Không tìm thấy tệp: {pdf_path}")

    filename = os.path.basename(pdf_path)
    is_q4 = "q4" in filename.lower()
    full_text = extract_text_from_pdf(pdf_path)

    # 1. Cắt bỏ trang lưu chiểu, danh sách ấn tống và 7 cụm LỜI BÀN ở Quyển 4
    if is_q4:
        cut_match = re.search(r"quyển\s*(?:đệ\s*)?4\s*hết", full_text, re.IGNORECASE)
        if cut_match:
            full_text = full_text[:cut_match.end()]
        full_text = re.sub(
            r"(?:LỜI|LÔØI)\s*(?:BÀN|BAØN).*?(?=\[\d{4}[a-z]\d{2}\]|\Z|\*\s*\*|\*\s*\*\s*\*)",
            "",
            full_text,
            flags=re.DOTALL | re.IGNORECASE
        )

    for pattern in NOISE_PATTERNS:
        full_text = re.sub(pattern, "", full_text, flags=re.MULTILINE | re.IGNORECASE)

    raw_matches = CBETA_PATTERN.findall(full_text)
    by_tag: Dict[str, List[str]] = {}
    tag_order: List[str] = []

    for tag, content in raw_matches:
        corrected_tag = TAG_CORRECTIONS.get(tag, tag)
        if corrected_tag not in by_tag:
            tag_order.append(corrected_tag)
        by_tag.setdefault(corrected_tag, []).append(content.strip())

    if is_q4:
        TEMPLATE_GROUPS = {
            "[1134a03]": ["[1134a04]", "[1134a05]"],
            # [1135c26] là thẻ bắt đầu của Mẫu văn trạng và Phong bì
            "[1135c26]": ["[1135c27]", "[1135c28]", "[1135c29]", "[1135c30]"],
            # [1136b15] là thẻ bắt đầu của Mẫu bảng thức mời trà
            "[1136b15]": ["[1136b16]", "[1136b17]", "[1136b18]", "[1136b19]"],
        }
    else:
        TEMPLATE_GROUPS = {
            "[1151b13]": ["[1151b14]", "[1151b15]", "[1151b16]", "[1151b17]", "[1151b18]"],
            "[1152a01]": ["[1152a02]", "[1152a03]", "[1152a04]", "[1152a05]", "[1152a06]", "[1152a07]", "[1152a08]"],
            "[1153a23]": ["[1153a24]", "[1153a25]"],
            "[1154b04]": ["[1154b05]", "[1154b06]", "[1154b07]"],
            "[1154b17]": ["[1154b18]", "[1154b19]", "[1154b20]", "[1154b21]", "[1154b22]"],
        }

    SUB_TAGS = set(sub for subs in TEMPLATE_GROUPS.values() for sub in subs)
    BAN_TRUONG_SUB_TAGS = (
        {f"[1149b{i:02d}]" for i in range(12, 30)}
        | {f"[1149c{i:02d}]" for i in range(1, 30)}
        | {'[1150a01]'}
    )
    THAO_DON_SUB_TAGS = {'[1150b16]', '[1150b18]', '[1150b19]', '[1150b20]', '[1150b21]', '[1150b22]'}
    NGUYET_PHAN_SUB_TAGS = {
        '[1154c26]', '[1154c28]', '[1155a02]', '[1155a05]',
        '[1155a10]', '[1155a12]', '[1155a15]', '[1155a17]', '[1155a20]',
        '[1155a21]', '[1155a24]', '[1155a26]'
    }
    CHAPTER_END_TAGS = {'[1136b25]', '[1150a12]', '[1155a26]'}

    # Di chuyển tiêu đề 'Sớ văn (tuyên đọc):' từ cuối [1152a01] sang đầu [1152a09] trong Quyển 7
    if not is_q4:
        if '[1152a01]' in by_tag and by_tag['[1152a01]']:
            v_orig = by_tag['[1152a01]'][-1]
            if "Sớ văn (tuyên đọc):" in v_orig:
                by_tag['[1152a01]'][-1] = re.sub(r"\s*Sớ văn\s*\(tuyên đọc\)\s*:\s*$", "", v_orig)
                if '[1152a09]' in by_tag and len(by_tag['[1152a09]']) >= 3:
                    by_tag['[1152a09]'][2] = "Sớ văn (tuyên đọc): " + by_tag['[1152a09]'][2]

    extracted_records: List[Dict[str, str]] = []

    for tag in tag_order:
        blocks = by_tag[tag]
        if tag in SUB_TAGS or tag in BAN_TRUONG_SUB_TAGS or tag in THAO_DON_SUB_TAGS or tag in NGUYET_PHAN_SUB_TAGS:
            continue
        if tag in CHAPTER_END_TAGS:
            continue

        # 1. Bản trướng thức trong Quyển 7: Tách thành 35 khoản thu chi tương ứng chuẩn xác
        if tag == '[1149b11]' and "q7" in filename.lower():
            viet_chunk_bt = blocks[2] if len(blocks) >= 3 else ""
            clean_vc_bt = clean_viet_text(viet_chunk_bt)
            for bt_tag, pat in BAN_TRUONG_MAP:
                m = re.search(pat, clean_vc_bt, re.DOTALL | re.IGNORECASE)
                v_item = clean_viet_text(m.group(0)) if m else ""
                if bt_tag == '[1149c19]-[1150a01]':
                    sub_tags_bt = [
                        '[1149c19]', '[1149c20]', '[1149c21]', '[1149c22]', '[1149c23]',
                        '[1149c24]', '[1149c25]', '[1149c26]', '[1149c27]', '[1149c28]', '[1150a01]'
                    ]
                    h_item = " ".join(clean_han_text(by_tag[st][0]) for st in sub_tags_bt if st in by_tag and by_tag[st])
                elif bt_tag == '[1149c16]':
                    h_16 = clean_han_text(by_tag['[1149c16]'][0]) if '[1149c16]' in by_tag else ""
                    h_17 = clean_han_text(by_tag['[1149c17]'][0]) if '[1149c17]' in by_tag else ""
                    h_item = f"{h_16} {h_17}".strip()
                else:
                    h_item = clean_han_text(by_tag[bt_tag][0]) if bt_tag in by_tag and by_tag[bt_tag] else ""
                h_item = apply_han_fixes(bt_tag, h_item, False)
                if h_item and v_item:
                    extracted_records.append({"tag": bt_tag, "han": h_item, "viet": v_item})
            continue

        # 2. Thảo đơn thức trong Quyển 7: Tách thành 6 dòng biểu mẫu 1-1
        if tag == '[1150b17]' and not is_q4:
            for td_tag, td_viet in THAO_DON_MAP:
                td_han = clean_han_text(by_tag[td_tag][0]) if td_tag in by_tag and by_tag[td_tag] else ""
                td_han = apply_han_fixes(td_tag, td_han, False)
                if td_han and td_viet:
                    extracted_records.append({"tag": td_tag, "han": td_han, "viet": td_viet})
            continue

        # 3. Nguyệt phần tu tri trong Quyển 7: Tách thành 12 tháng lịch tiết 1-1
        if tag == '[1154c23]' and not is_q4:
            full_translation = ""
            if '[1155a26]' in by_tag and by_tag['[1155a26]']:
                full_translation = clean_viet_text(by_tag['[1155a26]'][-1])

            month_patterns = [
                (r"Tháng giêng:.*?(?=Tháng hai:|\Z)", '[1154c23]'),
                (r"Tháng hai:.*?(?=Tháng ba:|\Z)", '[1154c26]'),
                (r"Tháng ba:.*?(?=Tháng tư:|\Z)", '[1154c28]'),
                (r"Tháng tư:.*?(?=Tháng năm:|\Z)", '[1155a02]'),
                (r"Tháng năm:.*?(?=Tháng sáu:|\Z)", '[1155a05]'),
                (r"Tháng sáu:.*?(?=Tháng bảy:|\Z)", '[1155a10]'),
                (r"Tháng bảy:.*?(?=Tháng tám:|\Z)", '[1155a12]'),
                (r"Tháng tám:.*?(?=Tháng chín:|\Z)", '[1155a15]'),
                (r"Tháng chín:.*?(?=Tháng mười:|\Z)", '[1155a17]'),
                (r"Tháng mười:.*?(?=Tháng mười một:|\Z)", '[1155a20]'),
                (r"Tháng mười một:.*?(?=Tháng mười hai:|\Z)", '[1155a21]'),
                (r"Tháng mười hai:.*?(?=Tiết lạp chương|Sắc tu|\Z)", '[1155a24]'),
            ]
            for pat, m_tag in month_patterns:
                m_match = re.search(pat, full_translation, re.DOTALL | re.IGNORECASE)
                m_viet = clean_viet_text(m_match.group(0)) if m_match else ""
                m_han = clean_han_text(by_tag[m_tag][0]) if m_tag in by_tag and by_tag[m_tag] else ""
                m_han = apply_han_fixes(m_tag, m_han, False)
                if m_han and m_viet:
                    extracted_records.append({"tag": m_tag, "han": m_han, "viet": m_viet})
            continue

        # 4. Nhóm biểu mẫu hành chính gom thẻ phong bì và lạc khoản
        if tag in TEMPLATE_GROUPS:
            sub_tags = TEMPLATE_GROUPS[tag]
            all_tags = [tag] + sub_tags
            han_parts = []
            for g_tag in all_tags:
                if g_tag in by_tag and by_tag[g_tag]:
                    han_parts.append(clean_han_text(by_tag[g_tag][0]))
            viet_text = clean_viet_text(blocks[-1]) if len(blocks) >= 2 else ""
            combined_han = " ".join(han_parts)
            combined_han = apply_han_fixes(f"{tag}-{sub_tags[-1]}", combined_han, is_q4)
            combined_han = apply_han_fixes(tag, combined_han, is_q4)
            extracted_records.append({
                "tag": f"{tag}-{sub_tags[-1]}",
                "han": combined_han,
                "viet": viet_text,
            })
            continue

        # 5. Các thẻ thông thường: Khối 0 = Hán, Khối 2 = Dịch nghĩa (Khối 1 = Phiên âm bị bỏ qua)
        han_clean = clean_han_text(blocks[0]) if blocks else ""
        viet_clean = ""
        if len(blocks) >= 3:
            viet_clean = clean_viet_text(blocks[2])
        elif len(blocks) == 2:
            viet_clean = clean_viet_text(blocks[1])

        # Xử lý đặc thù ở [1154b15]: tách chữ 茶狀 sang đầu tiêu đề mẫu thiệp
        if tag == '[1154b15]' and han_clean.endswith('茶狀'):
            han_clean = han_clean[:-2].strip()

        han_clean = apply_han_fixes(tag, han_clean, is_q4)

        if han_clean and viet_clean:
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
        print(f"Trích xuất thành công: {len(results)} khối CBETA hợp lệ.")
