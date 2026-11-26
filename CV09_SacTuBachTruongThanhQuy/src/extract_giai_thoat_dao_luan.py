"""Script trích xuất, làm sạch, sửa lỗi mã hóa font và cấu trúc hóa dữ liệu
song ngữ cho tác phẩm Giải Thoát Đạo Luận (解脫道論 - Vimuttimagga, CV09).

Nguồn dữ liệu:
- Bản Việt: Giai Thoat Dao Luan_VI_Text_NhuDien.pdf (341 trang, HT. Thích Như Điển dịch, 2006)
- Bản Hán:  Giai Thoat Dao Luan_ZH_Text_T1648.pdf (117 trang, CBETA T32n1648, 12 quyển)

Xử lý kỹ thuật chuyên biệt:
1. Khắc phục triệt để lỗi bảng mã ToUnicode CMap ở cấp span cho 2 font Việt đặc thù:
   - TTFFAC6368t00: ký tự 'N' (60 lần) -> 'ẩ' (khẩu, phẩm, ẩm, tẩy, chuẩn, bẩn...)
   - TTFFAC7490t00: ký tự điều khiển '\\x0f' (19 lần) -> 'ẩ' (Phẩm)
2. Tự động ghép nối lại toàn bộ 19 chữ cái lớn mở đầu chương (Drop-Cap size >= 28pt)
   vào đúng dòng văn bản tương ứng theo tọa độ y.
3. Loại bỏ tiêu đề đầu trang lặp lại, số trang, bìa quyển phụ lục ngày dịch (2005–2006),
   bản phiên âm Hán-Việt bài kệ kết trang 325, bài kệ hồi hướng dịch giả (trang 326),
   danh sách ấn tống (trang 327–341) và trang quảng bá CBETA (trang 116–117 bản Hán).
4. Phân tách cấu trúc đồng bộ 1-1 thành 19 phân đoạn chuẩn (12 Quyển / 12 Phẩm) làm mỏ neo
   cấu trúc cho bước dóng hàng câu bằng Quy hoạch động.
"""

import json
import os
import re
from typing import Any, Dict, List, Tuple
import pymupdf


# 19 phân đoạn cấu trúc khớp 1-1 giữa bản Hán (T32n1648) và bản Việt (Thích Như Điển)
SECTION_SPECS: List[Dict[str, Any]] = [
    {"id": "Q01_P01", "vol": 1, "zh_title": "因緣品第一", "vi_title": "Phẩm Nhơn Duyên thứ nhất", "zh_marker": "因緣品第一", "vi_page": 9},
    {"id": "Q01_P02", "vol": 1, "zh_title": "分別戒品第二", "vi_title": "Phẩm Phân Biệt Giới Thứ Hai", "zh_marker": "分別戒品第二", "vi_page": 14},
    {"id": "Q02_P03", "vol": 2, "zh_title": "頭陀品第三", "vi_title": "Phẩm Đầu Đà Thứ Ba", "zh_marker": "頭陀品第三", "vi_page": 36},
    {"id": "Q02_P04", "vol": 2, "zh_title": "分別定品第四", "vi_title": "Phẩm Phân Biệt Định Thứ Tư", "zh_marker": "分別定品第四", "vi_page": 51},
    {"id": "Q02_P05", "vol": 2, "zh_title": "覓善知識品第五", "vi_title": "Phẩm Mịch Thiện Tri Thức Thứ Năm", "zh_marker": "覓善知識品第五", "vi_page": 59},
    {"id": "Q03_P06", "vol": 3, "zh_title": "分別行品第六", "vi_title": "Phẩm Phân Biệt Hạnh (việc làm) Thứ 6", "zh_marker": "分別行品第六", "vi_page": 66},
    {"id": "Q03_P07", "vol": 3, "zh_title": "分別行處品第七", "vi_title": "Phẩm Phân Biệt Hành Xứ Thứ 7", "zh_marker": "分別行處品第七", "vi_page": 73},
    {"id": "Q04_P08a", "vol": 4, "zh_title": "行門品第八之一", "vi_title": "Phẩm Hành Môn Thứ 8 - Phần một", "zh_marker": "行門品第八之一", "vi_page": 82},
    {"id": "Q05_P08b", "vol": 5, "zh_title": "行門品之二", "vi_title": "Phẩm Hành Môn Thứ 2", "zh_marker": "行門品之二", "vi_page": 110},
    {"id": "Q06_P08c", "vol": 6, "zh_title": "行門品之三", "vi_title": "Phẩm Hành Môn Thứ 3", "zh_marker": "行門品之三", "vi_page": 138},
    {"id": "Q07_P08d", "vol": 7, "zh_title": "行門品之四", "vi_title": "Phẩm Hành Môn Thứ Tư", "zh_marker": "行門品之四", "vi_page": 164},
    {"id": "Q08_P08e1", "vol": 8, "zh_title": "行門品之五", "vi_title": "Phẩm Hành Môn Thứ 5", "zh_marker": "行門品之五", "vi_page": 190},
    {"id": "Q08_P08e2", "vol": 8, "zh_title": "重明四無量義。", "vi_title": "Thêm vào để làm rõ nghĩa Tứ Vô Lượng", "zh_marker": "重明四無量義。", "vi_page": 204},
    {"id": "Q09_P09", "vol": 9, "zh_title": "五通品第九", "vi_title": "Phẩm Ngũ Thông Thứ 8", "zh_marker": "五通品第九", "vi_page": 222},
    {"id": "Q09_P10", "vol": 9, "zh_title": "解脫道論分別慧品第十", "vi_title": "Phẩm Phân Biệt Huệ thứ 10", "zh_marker": "解脫道論分別慧品第十", "vi_page": 238},
    {"id": "Q10_P11a", "vol": 10, "zh_title": "五方便品第十一之一", "vi_title": "Phẩm Ngũ Phương Tiện thứ 11 Phần thứ nhất", "zh_marker": "五方便品第十一之一", "vi_page": 244},
    {"id": "Q11_P11b", "vol": 11, "zh_title": "五方便品之二", "vi_title": "Năm Phẩm Phương Tiện Phần thứ 2", "zh_marker": "五方便品之二", "vi_page": 274},
    {"id": "Q11_P12a", "vol": 11, "zh_title": "解脫道論分別諦品第十二之一", "vi_title": "Phẩm Phân Biệt Chân Lý Thứ 11 Phần 1", "zh_marker": "解脫道論分別諦品第十二之一", "vi_page": 283},
    {"id": "Q12_P12b", "vol": 12, "zh_title": "分別諦品第十二之二", "vi_title": "Phẩm Phân Biệt Chân Lý thứ 12 Phần thứ 2", "zh_marker": "分別諦品第十二之二", "vi_page": 300},
]

# Các trang bìa riêng của Quyển 2..12 trong bản tiếng Việt (chỉ chứa tiêu đề & ghi chú ngày dịch 2005-2006)
VI_VOLUME_COVER_PAGES = {35, 65, 81, 109, 137, 163, 189, 221, 243, 273, 299}


def is_cjk_char(ch: str) -> bool:
    code = ord(ch)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0x20000 <= code <= 0x2A6DF)


def repair_vi_span_text(font_name: str, text: str) -> str:
    """Sửa lỗi bảng mã CMap ở cấp span cho các font tiếng Việt nhúng trong PDF."""
    fn = font_name.split("+")[-1]
    if fn == "TTFFAC6368t00" and "N" in text:
        text = text.replace("N", "ẩ")
    elif fn == "TTFFAC7490t00" and "\x0f" in text:
        text = text.replace("\x0f", "ẩ")
    text = text.replace("\x01", "")
    return text


def extract_vi_page_lines(page: pymupdf.Page, page_num: int) -> List[Dict[str, Any]]:
    """Trích xuất các dòng nội dung trên một trang PDF Việt, bỏ header và ghép chữ Drop-Cap."""
    d = page.get_text("dict")
    raw_lines: List[Dict[str, Any]] = []
    dropcaps: List[Dict[str, Any]] = []

    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        for line in b["lines"]:
            y0 = line["bbox"][1]
            x0 = line["bbox"][0]
            # Bỏ tiêu đề đầu trang và số trang ở vùng y < 65pt
            if y0 < 65.0:
                continue
            spans = [s for s in line["spans"] if s["text"].strip()]
            if not spans:
                continue

            max_size = max(s["size"] for s in spans)
            is_bold = any(("Bold" in s["font"]) or ("TTFFAC7490t00" in s["font"]) for s in spans)
            text = "".join(repair_vi_span_text(s["font"], s["text"]) for s in line["spans"]).strip()
            if not text:
                continue

            # Phát hiện chữ cái lớn mở đầu chương (Drop-Cap) có cỡ chữ >= 28pt
            if max_size >= 28.0 and len(text) <= 2:
                dropcaps.append({"char": text, "y0": y0, "x0": x0})
                continue

            raw_lines.append({
                "page": page_num,
                "y0": y0,
                "x0": x0,
                "x1": line["bbox"][2],
                "size": max_size,
                "is_bold": is_bold,
                "text": text,
            })

    # Sắp xếp dòng theo thứ tự từ trên xuống dưới
    raw_lines.sort(key=lambda r: (round(r["y0"], 1), round(r["x0"], 1)))

    # Ghép từng Drop-Cap vào dòng thân bài gần nhất theo tọa độ y
    for dc in dropcaps:
        best_idx = None
        best_dist = 9999.0
        for idx, r in enumerate(raw_lines):
            if r["size"] >= 14.0:
                continue
            dist = abs(r["y0"] - dc["y0"])
            if dist < best_dist and r["x0"] >= 85.0:
                best_dist = dist
                best_idx = idx
        if best_idx is not None and best_dist <= 30.0:
            ch = dc["char"]
            old_text = raw_lines[best_idx]["text"]
            # 'Ở' + 'đây tìm cầu...' là hai âm tiết độc lập nên chèn dấu cách
            if ch == "Ở" and old_text.startswith("đây"):
                raw_lines[best_idx]["text"] = f"{ch} {old_text}"
            else:
                raw_lines[best_idx]["text"] = f"{ch}{old_text}"
            raw_lines[best_idx]["had_dropcap"] = True

    return raw_lines


def clean_vi_section_lines(lines: List[Dict[str, Any]], section_id: str) -> str:
    """Làm sạch tiêu đề thừa, gom dòng thành đoạn văn chuẩn và chuẩn hóa khoảng trắng."""
    # Lọc bỏ các dòng bìa sách / kết quyển lặp lại không thuộc chính văn Hán
    filtered: List[Dict[str, Any]] = []
    skip_translit = False

    for r in lines:
        txt = r["text"].strip()
        if not txt:
            continue

        # Bỏ dòng tiêu đề sách lặp lại (size >= 16 hoặc bold cuối quyển)
        if re.match(r"^Luận\s+về\s+con\s+đường\s+giải\s+thoát$", txt, re.IGNORECASE):
            continue
        if re.match(r"^Quyển\s+thứ\s+", txt, re.IGNORECASE) and r["is_bold"]:
            continue
        if re.match(r"^Hết\s+quyển\s+", txt, re.IGNORECASE) and r["is_bold"]:
            continue
        # Bỏ ghi chú ngày dịch của dịch giả ở cuối quyển 6
        if re.match(r"^Dịch\s+xong\s+quyển\s+", txt, re.IGNORECASE) or ("Tu Viện Đa Bảo" in txt and "nhập thất" in txt):
            continue

        # Bỏ các dòng tiêu đề Phẩm ở đầu phân đoạn (chúng ta sẽ ghép tiêu đề Phẩm làm dòng mở đầu riêng)
        if r["size"] >= 15.0 and r["is_bold"]:
            continue

        # Riêng cuối Quyển 12 (trang 325): loại bỏ đoạn phiên âm Hán-Việt 6 câu trước nhãn 'Nghĩa:'
        # vì ngay bên dưới đã có bản dịch nghĩa thuần Việt tương ứng nguyên tác chữ Hán.
        if section_id == "Q12_P12b":
            if txt.startswith("Vô biên, vô xưng bất khả tư"):
                skip_translit = True
                continue
            if skip_translit:
                if txt.startswith("Nghĩa:"):
                    skip_translit = False
                continue

        filtered.append(r)

    # Nối dòng thành đoạn văn theo khoảng cách dọc (y gap) và thụt đầu dòng (x0)
    paragraphs: List[str] = []
    cur_para: List[str] = []
    prev_r = None

    for r in filtered:
        txt = r["text"]
        is_new_para = False
        if prev_r is not None:
            same_page = (r["page"] == prev_r["page"])
            if same_page:
                dy = r["y0"] - prev_r["y0"]
                # Khoảng cách chuẩn giữa 2 dòng cùng đoạn là ~13.8pt; >= 21pt là đoạn mới
                if dy >= 21.0:
                    is_new_para = True
                # Thụt đầu dòng đoạn mới (lề trái trang lẻ ~53.8pt, trang chẵn ~70.8pt; thụt đầu đoạn +28pt)
                elif (r["x0"] - prev_r["x0"]) >= 18.0 and prev_r["text"][-1:] in ".?!:”;)\"'" :
                    is_new_para = True
                elif re.match(r"^(Hỏi\s*(?:rằng)?\s*:|Đáp\s*(?:rằng)?\s*:)", txt):
                    is_new_para = True
            else:
                # Chuyển sang trang mới: tạo đoạn mới nếu dòng mới thụt đầu dòng hoặc là Hỏi/Đáp
                # Lề trái trang lẻ ~53.8pt, trang chẵn ~70.8pt
                left_margin = 53.8 if (r["page"] % 2 == 1) else 70.8
                if (r["x0"] - left_margin) >= 18.0 or re.match(r"^(Hỏi\s*(?:rằng)?\s*:|Đáp\s*(?:rằng)?\s*:)", txt):
                    is_new_para = True

        if is_new_para and cur_para:
            paragraphs.append(" ".join(cur_para))
            cur_para = []

        cur_para.append(txt)
        prev_r = r

    if cur_para:
        paragraphs.append(" ".join(cur_para))

    # Chuẩn hóa văn bản từng đoạn
    cleaned_paras: List[str] = []
    for p in paragraphs:
        p = re.sub(r"\s+", " ", p).strip()
        # Sửa một số lỗi dính chữ/dấu câu do dàn trang PDF
        p = p.replace("ĐứcThế", "Đức Thế")
        p = re.sub(r",(?=[^\s\d])", ", ", p)
        p = re.sub(r"\s+([?!,;:])", r"\1", p)
        p = re.sub(r"\s+\.(?!\.)", ".", p)
        p = re.sub(r"\.-$", ".", p)
        p = re.sub(r"\s+", " ", p).strip()
        if p:
            cleaned_paras.append(p)

    return "\n\n".join(cleaned_paras)


def extract_vietnamese_sections(pdf_path: str) -> Dict[str, Any]:
    """Trích xuất toàn bộ 19 phân đoạn tiếng Việt từ trang 9 đến trang 325."""
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)

    # Phân trang theo ranh giới 19 phân đoạn
    sections_out: Dict[str, Dict[str, Any]] = {}
    for idx, spec in enumerate(SECTION_SPECS):
        start_p = spec["vi_page"]
        if idx + 1 < len(SECTION_SPECS):
            end_p = SECTION_SPECS[idx + 1]["vi_page"] - 1
        else:
            end_p = 325

        # Kiểm tra nếu 2 phân đoạn nằm liền nhau (hoặc kết thúc trước trang bìa quyển)
        sec_lines: List[Dict[str, Any]] = []
        for p in range(start_p, end_p + 1):
            if p in VI_VOLUME_COVER_PAGES:
                continue
            page_lines = extract_vi_page_lines(doc[p - 1], p)
            sec_lines.extend(page_lines)

        body_text = clean_vi_section_lines(sec_lines, spec["id"])
        sections_out[spec["id"]] = {
            "id": spec["id"],
            "vol": spec["vol"],
            "vi_title": spec["vi_title"],
            "vi_pages": f"{start_p}-{end_p}",
            "vi_body": body_text,
        }

    doc.close()
    return {
        "total_pages": total_pages,
        "sections": sections_out,
    }


def extract_chinese_sections(pdf_path: str) -> Dict[str, Any]:
    """Trích xuất toàn bộ 19 phân đoạn chữ Hán từ trang 5 đến trang 115 (CBETA T32n1648)."""
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)

    # Đọc từng dòng trên trang 5..115 và giữ lại ranh giới đoạn văn thực sự của CBETA
    raw_paras: List[str] = []
    cur_buf = ""

    for p in range(4, 115):
        page = doc[p]
        d = page.get_text("dict")
        page_lines = []
        for b in d["blocks"]:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                txt = "".join(s["text"] for s in line["spans"]).strip()
                if not txt:
                    continue
                page_lines.append((line["bbox"][0], line["bbox"][1], line["bbox"][2], txt))

        page_lines.sort(key=lambda r: (round(r[1], 1), round(r[0], 1)))

        for x0, y0, x1, txt in page_lines:
            # Bỏ số trang CBETA (có thể xuất hiện ở đầu hoặc cuối danh sách dòng)
            if re.match(r"^\d+$", txt):
                continue
            # Lọc bỏ tiêu đề quyển và tên tác giả/dịch giả lặp lại ở mỗi quyển
            if txt in ("No. 1648", "阿羅漢優波底沙梁言大光造", "梁扶南三藏僧伽婆羅譯"):
                if cur_buf:
                    raw_paras.append(cur_buf)
                    cur_buf = ""
                continue
            if re.match(r"^解脫道論卷第[一二三四五六七八九十]+$", txt):
                if cur_buf:
                    raw_paras.append(cur_buf)
                    cur_buf = ""
                continue

            # Nếu là tiêu đề Phẩm trong SECTION_SPECS -> tách đoạn riêng
            is_heading = any(txt == s["zh_marker"] for s in SECTION_SPECS)
            if is_heading:
                if cur_buf:
                    raw_paras.append(cur_buf)
                    cur_buf = ""
                raw_paras.append(txt)
                continue

            # Phát hiện bắt đầu đoạn mới (hỏi đáp 問：/問曰： hoặc dòng trước ngắn kết thúc câu)
            if cur_buf and (
                txt.startswith("問：")
                or txt.startswith("問曰：")
                or txt.startswith("問曰。")
                or cur_buf.endswith("已竟)。")
                or cur_buf.endswith("已竟)")
                or cur_buf.endswith("竟)")
                or cur_buf.endswith("已滿)")
            ):
                raw_paras.append(cur_buf)
                cur_buf = ""

            # Nối liền chữ Hán không chèn khoảng trắng giữa các ký tự CJK
            if not cur_buf:
                cur_buf = txt
            else:
                # Giữ khoảng trắng toàn giác trong bài kệ (　) nhưng nối liền văn xuôi
                cur_buf += txt

            # Nếu dòng ngắn đáng kể (x1 < 420 trên trang rộng ~520) và kết thúc bằng dấu ngắt câu/kệ -> hết đoạn
            if x1 < 420.0 and cur_buf[-1:] in "。！？)":
                raw_paras.append(cur_buf)
                cur_buf = ""

    if cur_buf:
        raw_paras.append(cur_buf)

    full_zh = "\n".join(raw_paras)

    # Tách theo 19 dấu mốc chính xác
    marker_positions: List[Tuple[int, Dict[str, Any]]] = []
    for spec in SECTION_SPECS:
        m = spec["zh_marker"]
        pos = full_zh.find(m)
        if pos == -1:
            raise ValueError(f"Không tìm thấy dấu mốc chữ Hán: {m}")
        marker_positions.append((pos, spec))

    sections_out: Dict[str, Dict[str, Any]] = {}
    for idx, (pos, spec) in enumerate(marker_positions):
        start_body = pos + len(spec["zh_marker"])
        end_body = marker_positions[idx + 1][0] if idx + 1 < len(marker_positions) else len(full_zh)
        body = full_zh[start_body:end_body].strip()
        # Chuẩn hóa khoảng trắng toàn giác trong kệ thành dấu phẩy/khoảng trắng gọn
        body = re.sub(r"\u3000+", " ", body)
        body = re.sub(r"[ \t]+", " ", body)
        sections_out[spec["id"]] = {
            "id": spec["id"],
            "vol": spec["vol"],
            "zh_title": spec["zh_title"],
            "zh_body": body,
        }

    doc.close()
    return {
        "total_pages": total_pages,
        "sections": sections_out,
    }


def main() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    nguon_dir = os.path.join(base_dir, "01_nguon")
    out_dir = os.path.join(base_dir, "03_text_sach", "giai_thoat_dao_luan")
    os.makedirs(out_dir, exist_ok=True)

    vi_pdf = os.path.join(nguon_dir, "Giai Thoat Dao Luan_VI_Text_NhuDien.pdf")
    zh_pdf = os.path.join(nguon_dir, "Giai Thoat Dao Luan_ZH_Text_T1648.pdf")

    print("[1/3] Trích xuất & sửa lỗi font/Drop-Cap bản tiếng Việt (341 trang)...")
    vi_data = extract_vietnamese_sections(vi_pdf)

    print("[2/3] Trích xuất & cấu trúc hóa bản chữ Hán CBETA T32n1648 (117 trang)...")
    zh_data = extract_chinese_sections(zh_pdf)

    print("[3/3] Tổng hợp 19 phân đoạn song song & xuất thống kê...")
    merged_sections: List[Dict[str, Any]] = []
    tot_zh_cjk = 0
    tot_vi_words = 0
    tot_vi_chars = 0

    print(f"\n{'ID':<10} {'Vol':<4} {'ZH_CJK':>7} {'VI_Chr':>7} {'Ratio':>6}  {'ZH_Head':<24} | {'VI_Head'}")
    print("-" * 105)
    for spec in SECTION_SPECS:
        sid = spec["id"]
        zh_s = zh_data["sections"][sid]
        vi_s = vi_data["sections"][sid]
        zh_body = zh_s["zh_body"]
        vi_body = vi_s["vi_body"]

        zh_cjk = sum(1 for c in zh_body if is_cjk_char(c))
        vi_chr = len(re.sub(r"[^\w]", "", vi_body))
        vi_words = len(vi_body.split())
        ratio = round(vi_chr / zh_cjk, 2) if zh_cjk > 0 else 0.0

        tot_zh_cjk += zh_cjk
        tot_vi_words += vi_words
        tot_vi_chars += vi_chr

        merged_sections.append({
            "id": sid,
            "vol": spec["vol"],
            "zh_title": spec["zh_title"],
            "vi_title": spec["vi_title"],
            "vi_pages": vi_s["vi_pages"],
            "zh_cjk_chars": zh_cjk,
            "vi_words": vi_words,
            "vi_chars": vi_chr,
            "char_ratio": ratio,
            "zh_body": zh_body,
            "vi_body": vi_body,
        })

        z_prev = zh_body.replace("\n", " ")[:22]
        v_prev = vi_body.replace("\n", " ")[:38]
        print(f"{sid:<10} Q{spec['vol']:<3} {zh_cjk:>7} {vi_chr:>7} {ratio:>6.2f}  {z_prev:<24} | {v_prev}")

    print("-" * 105)
    print(f"{'TOTAL':<10} 12Q  {tot_zh_cjk:>7} {tot_vi_chars:>7} {tot_vi_chars/tot_zh_cjk:>6.2f}")

    # Lưu JSON 19 phân đoạn cấu trúc hóa
    sections_json_path = os.path.join(out_dir, "giai_thoat_dao_luan_sections.json")
    with open(sections_json_path, "w", encoding="utf-8") as f:
        json.dump(merged_sections, f, ensure_ascii=False, indent=2)

    # Lưu toàn văn đơn ngữ đã làm sạch
    han_clean_path = os.path.join(out_dir, "giai_thoat_dao_luan_han_clean.txt")
    viet_clean_path = os.path.join(out_dir, "giai_thoat_dao_luan_viet_clean.txt")
    with open(han_clean_path, "w", encoding="utf-8") as fh, open(viet_clean_path, "w", encoding="utf-8") as fv:
        for sec in merged_sections:
            fh.write(f"=== {sec['id']} | {sec['zh_title']} ===\n{sec['zh_body']}\n\n")
            fv.write(f"=== {sec['id']} | {sec['vi_title']} ===\n{sec['vi_body']}\n\n")

    # Lưu tệp thống kê JSON
    stats = {
        "work_title": "Giải Thoát Đạo Luận (解脫道論 - Vimuttimagga)",
        "files": {
            "vi": {
                "filename": os.path.basename(vi_pdf),
                "size_mb": round(os.path.getsize(vi_pdf) / (1024 * 1024), 2),
                "pages": vi_data["total_pages"],
                "body_pages": "9 - 325",
            },
            "zh": {
                "filename": os.path.basename(zh_pdf),
                "size_mb": round(os.path.getsize(zh_pdf) / (1024 * 1024), 2),
                "pages": zh_data["total_pages"],
                "body_pages": "5 - 115",
            },
        },
        "totals": {
            "volumes": 12,
            "sections": len(merged_sections),
            "zh_cjk_chars": tot_zh_cjk,
            "vi_words": tot_vi_words,
            "vi_chars": tot_vi_chars,
            "char_ratio_vi_to_zh": round(tot_vi_chars / tot_zh_cjk, 2) if tot_zh_cjk > 0 else 0.0,
        },
        "sections_summary": [
            {
                "id": s["id"],
                "vol": s["vol"],
                "zh_title": s["zh_title"],
                "vi_title": s["vi_title"],
                "vi_pages": s["vi_pages"],
                "zh_cjk_chars": s["zh_cjk_chars"],
                "vi_words": s["vi_words"],
                "char_ratio": s["char_ratio"],
            }
            for s in merged_sections
        ],
    }
    stats_path = os.path.join(out_dir, "thong_ke_giai_thoat_dao_luan.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"\n[+] Đã xuất 19 phân đoạn sạch tại: {out_dir}")


if __name__ == "__main__":
    main()
