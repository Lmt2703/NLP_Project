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
    ('[1149c16]', r"Chi 444 quan 500 tiền: biếu cho Tăng chúng tụng kinh tại.*?bằng nữa phần người khác\."),
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
    # Chuẩn hóa các biến thể viết tắt v. v...
    text = re.sub(r"\bv\.\s*v[…\.]*", "v.v...", text, flags=re.IGNORECASE)
    text = re.sub(r"\bv[…]+", "v.v...", text, flags=re.IGNORECASE)
    text = re.sub(r"\.{2,}", "...", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_book(pdf_path: str) -> List[Dict[str, str]]:
    """Trích xuất và cấu trúc hóa toàn bộ văn bản Hán - Việt từ tệp PDF theo đúng tuần tự."""
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"Không tìm thấy tệp: {pdf_path}")

    filename = os.path.basename(pdf_path)
    full_text = extract_text_from_pdf(pdf_path)

    # 1. Cắt bỏ trang lưu chiểu, danh sách ấn tống và 7 cụm LỜI BÀN ở Quyển 4
    if "q4" in filename.lower():
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

    if "q4" in filename.lower():
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
    if "q7" in filename.lower():
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
                else:
                    h_item = clean_han_text(by_tag[bt_tag][0]) if bt_tag in by_tag and by_tag[bt_tag] else ""
                if h_item and v_item:
                    extracted_records.append({"tag": bt_tag, "han": h_item, "viet": v_item})
            continue

        # 2. Thảo đơn thức trong Quyển 7: Tách thành 6 dòng biểu mẫu 1-1
        if tag == '[1150b17]' and "q7" in filename.lower():
            for td_tag, td_viet in THAO_DON_MAP:
                td_han = clean_han_text(by_tag[td_tag][0]) if td_tag in by_tag and by_tag[td_tag] else ""
                if td_han and td_viet:
                    extracted_records.append({"tag": td_tag, "han": td_han, "viet": td_viet})
            continue

        # 3. Nguyệt phần tu tri trong Quyển 7: Tách thành 12 tháng lịch tiết 1-1
        if tag == '[1154c23]' and "q7" in filename.lower():
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
            extracted_records.append({
                "tag": f"{tag}-{sub_tags[-1]}",
                "han": " ".join(han_parts),
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
