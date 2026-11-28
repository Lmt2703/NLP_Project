"""Script trích xuất, cấu trúc hóa và thống kê dữ liệu song ngữ Triệu Châu Ngữ Lục.
Tác phẩm: Triệu Châu Chân Tế Thiền Sư Ngữ Lục (趙州真際禪師語錄)
Nguồn:
- Bản Việt: Trieu Chau Ngu Luc_VI_Text_ThongPhuong (1).pdf (134 trang)
- Bản Hán: Trieu Chau Ngu Luc_ZH_Text_X1315.pdf (52 trang, CBETA X68n1315)
"""

import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple
import pymupdf


def is_cjk_char(ch: str) -> bool:
    code = ord(ch)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0x20000 <= code <= 0x2A6DF)


def extract_vietnamese_pdf(pdf_path: str) -> Dict[str, Any]:
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)

    full_page_texts = [doc[p].get_text() for p in range(total_pages)]

    # 1. Bìa & Thông tin sách (Trang 0)
    p0_text = full_page_texts[0].strip()

    # 2. Hành trạng (Trang 1 đến trang 6, trước '---o0o--- \n NGỮ LỤC')
    hanh_trang_raw = ""
    for p in range(1, 7):
        txt = full_page_texts[p]
        if p == 6:
            idx = txt.find("---o0o---")
            if idx != -1:
                txt = txt[:idx]
        hanh_trang_raw += txt + "\n"

    # Làm sạch dòng hành trạng
    ht_lines = [l.strip() for l in hanh_trang_raw.splitlines() if l.strip()]
    hanh_trang_clean = "\n".join(ht_lines)

    # 3. Ngữ lục chính văn (Trang 6 đến trang 121, trước '---o0o--- \n Hết')
    ngu_luc_raw = ""
    for p in range(6, 122):
        txt = full_page_texts[p]
        if p == 6:
            idx = txt.find("NGỮ LỤC")
            if idx != -1:
                txt = txt[idx + len("NGỮ LỤC") :]
        if p == 121:
            idx = txt.find("---o0o---")
            if idx != -1:
                txt = txt[:idx]
        ngu_luc_raw += txt + "\n"

    # 4. Chú thích (Trang 121 sau 'Hết' đến trang 133)
    chu_thich_raw = ""
    p121_txt = full_page_texts[121]
    idx_het = p121_txt.find("Hết")
    if idx_het != -1:
        chu_thich_raw += p121_txt[idx_het + len("Hết") :] + "\n"
    for p in range(122, total_pages):
        chu_thich_raw += full_page_texts[p] + "\n"

    # Tách 525 mục trong Ngữ Lục
    item_pattern = re.compile(r"(?:\n|\A)\s*(\d+)\.\s*")
    matches = list(item_pattern.finditer(ngu_luc_raw))

    items: Dict[int, str] = {}
    for i in range(len(matches)):
        num = int(matches[i].group(1))
        start_pos = matches[i].end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(ngu_luc_raw)
        content = ngu_luc_raw[start_pos:end_pos].strip()
        items[num] = content

    # Xử lý trường hợp 455 nằm trong khối 454 (do nhà in sót số thứ tự)
    if 454 in items and 455 not in items:
        t454 = items[454]
        split_m = re.search(r"(.*?\bTọa chủ không đáp được\.\s*)(Một hôm Sư thượng đường.*)", t454, re.DOTALL)
        if split_m:
            items[454] = split_m.group(1).strip()
            items[455] = split_m.group(2).strip()

    # Tách đầy đủ 334 mục chú thích 1 đến 334
    ct_pattern = re.compile(r"(?:\n|\A)\s*(\d{1,3})[\.\s]\s*")
    ct_matches = list(ct_pattern.finditer(chu_thich_raw))
    footnotes: Dict[int, str] = {}
    for i in range(len(ct_matches)):
        num = int(ct_matches[i].group(1))
        if not (1 <= num <= 334):
            continue
        start_pos = ct_matches[i].end()
        end_pos = ct_matches[i + 1].start() if i + 1 < len(ct_matches) else len(chu_thich_raw)
        content = chu_thich_raw[start_pos:end_pos].strip()
        footnotes[num] = content

    doc.close()

    return {
        "total_pages": total_pages,
        "cover_info": p0_text,
        "hanh_trang": hanh_trang_clean,
        "items": items,
        "footnotes": footnotes,
    }


def extract_chinese_pdf(pdf_path: str) -> Dict[str, Any]:
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)

    full_page_texts = [doc[p].get_text() for p in range(total_pages)]

    # 1. Tựa Cổ Tôn Túc (Trang 0 đến trang 1, trước '古尊宿語錄卷第十四')
    p0_1_text = full_page_texts[0] + "\n" + full_page_texts[1]
    tua_end_idx = p0_1_text.find("古尊宿語錄卷第十四")
    tua_text = p0_1_text[:tua_end_idx].strip() if tua_end_idx != -1 else full_page_texts[0].strip()

    # 2. Quyển 14: Triệu Châu Chân Tế Thiền Sư Ngữ Lục Chi Dư (Trang 1 đến trang 17)
    q14_raw = ""
    for p in range(1, 18):
        txt = full_page_texts[p]
        if p == 1:
            idx = txt.find("古尊宿語錄卷第十四")
            if idx != -1:
                txt = txt[idx:]
        if p == 17:
            idx = txt.find("古尊宿語錄卷第十五")
            if idx != -1:
                txt = txt[:idx]
        q14_raw += txt + "\n"

    # Làm sạch dòng Quyển 14
    q14_clean_lines = []
    for line in q14_raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # Bỏ dòng header lặp lại
        if "古尊宿語錄·趙州真際禪師語錄" in line or line.startswith("古尊宿語錄卷第"):
            continue
        q14_clean_lines.append(line)
    q14_clean = "\n".join(q14_clean_lines)

    # 3. Quyển 15 & 16: Vân Môn Khuông Chân Thiền Sư Quảng Lục (Trang 18 đến 51)
    van_mon_raw = ""
    for p in range(17, total_pages):
        txt = full_page_texts[p]
        if p == 17:
            idx = txt.find("古尊宿語錄卷第十五")
            if idx != -1:
                txt = txt[idx:]
        van_mon_raw += txt + "\n"

    vm_clean_lines = []
    for line in van_mon_raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if "古尊宿語錄·趙州真際禪師語錄" in line:
            continue
        vm_clean_lines.append(line)
    van_mon_clean = "\n".join(vm_clean_lines)

    doc.close()

    return {
        "total_pages": total_pages,
        "tua_text": tua_text,
        "q14_text": q14_clean,
        "van_mon_text": van_mon_clean,
    }


def compute_statistics(vi_data: Dict[str, Any], zh_data: Dict[str, Any], vi_pdf_path: str, zh_pdf_path: str) -> Dict[str, Any]:
    vi_size_mb = os.path.getsize(vi_pdf_path) / (1024 * 1024)
    zh_size_mb = os.path.getsize(zh_pdf_path) / (1024 * 1024)

    # --- Thống kê Tiếng Việt ---
    ht_text = vi_data["hanh_trang"]
    ht_words = len(ht_text.split())
    ht_chars = len(ht_text)
    ht_sentences = len(re.findall(r"[\.\?\!]+(?:\s+|$)", ht_text))

    items = vi_data["items"]
    sorted_item_ids = sorted(items.keys())
    total_items = len(sorted_item_ids)

    # Phân nhóm theo Quyển tương ứng
    q13_items = {k: v for k, v in items.items() if k <= 208}
    q14_items = {k: v for k, v in items.items() if k >= 209}

    item_word_counts = {k: len(v.split()) for k, v in items.items()}
    item_char_counts = {k: len(v) for k, v in items.items()}

    total_nl_words = sum(item_word_counts.values())
    total_nl_chars = sum(item_char_counts.values())

    max_item_id = max(item_word_counts, key=item_word_counts.get)
    min_item_id = min(item_word_counts, key=item_word_counts.get)

    # Chú thích
    footnotes = vi_data["footnotes"]
    fn_word_counts = {k: len(v.split()) for k, v in footnotes.items()}
    total_fn_words = sum(fn_word_counts.values())
    total_fn_chars = sum(len(v) for v in footnotes.values())

    total_vi_words = ht_words + total_nl_words + total_fn_words
    total_vi_chars = ht_chars + total_nl_chars + total_fn_chars

    # --- Thống kê Chữ Hán ---
    q14_text = zh_data["q14_text"]
    q14_cjk_chars = sum(1 for c in q14_text if is_cjk_char(c))
    q14_punctuation = sum(1 for c in q14_text if c in "。，、：；！？「」『』（）《》")
    q14_lines = len(q14_text.splitlines())
    q14_sentences = len(re.findall(r"[。！？]", q14_text))

    # Cấu trúc đối thoại trong Q14
    q14_questions = len(re.findall(r"問[：:]", q14_text))
    q14_replies = len(re.findall(r"師(?:云|乃|應|代|便|喝|以|不)[：:]?", q14_text))
    q14_shang_tang = len(re.findall(r"師上堂", q14_text))

    # Tựa Cổ Tôn Túc
    tua_text = zh_data["tua_text"]
    tua_cjk = sum(1 for c in tua_text if is_cjk_char(c))

    # Phần Vân Môn (Q15-16)
    vm_text = zh_data["van_mon_text"]
    vm_cjk = sum(1 for c in vm_text if is_cjk_char(c))

    total_zh_cjk = tua_cjk + q14_cjk_chars + vm_cjk

    # Tương quan dóng hàng (Q14 Việt vs Q14 Hán)
    q14_vi_words = sum(item_word_counts[k] for k in q14_items)
    q14_vi_chars = sum(item_char_counts[k] for k in q14_items)
    char_ratio_q14 = q14_vi_chars / q14_cjk_chars if q14_cjk_chars > 0 else 0

    return {
        "files": {
            "vi": {
                "filename": os.path.basename(vi_pdf_path),
                "size_mb": round(vi_size_mb, 2),
                "pages": vi_data["total_pages"],
            },
            "zh": {
                "filename": os.path.basename(zh_pdf_path),
                "size_mb": round(zh_size_mb, 2),
                "pages": zh_data["total_pages"],
            },
        },
        "vietnamese": {
            "total_words": total_vi_words,
            "total_chars": total_vi_chars,
            "hanh_trang": {
                "pages": "1 - 6",
                "words": ht_words,
                "chars": ht_chars,
                "sentences": ht_sentences,
            },
            "ngu_luc": {
                "pages": "6 - 121",
                "total_items": total_items,
                "total_words": total_nl_words,
                "total_chars": total_nl_chars,
                "avg_words_per_item": round(total_nl_words / total_items, 1),
                "max_item": {"id": max_item_id, "words": item_word_counts[max_item_id]},
                "min_item": {"id": min_item_id, "words": item_word_counts[min_item_id]},
                "q13_items_count": len(q13_items),
                "q13_words": sum(item_word_counts[k] for k in q13_items),
                "q14_items_count": len(q14_items),
                "q14_words": q14_vi_words,
            },
            "footnotes": {
                "pages": "121 - 133",
                "total_notes": len(footnotes),
                "words": total_fn_words,
                "chars": total_fn_chars,
            },
        },
        "chinese": {
            "total_pages": zh_data["total_pages"],
            "total_cjk_chars": total_zh_cjk,
            "tua_co_ton_tuc": {
                "pages": "0 - 1",
                "cjk_chars": tua_cjk,
                "author": "Sa môn Vật Sơ Đại Quán (1267)",
            },
            "q14_trieu_chau": {
                "pages": "1 - 17",
                "title": "古尊宿語錄卷第十四 - 趙州真際禪師語錄之餘",
                "cjk_chars": q14_cjk_chars,
                "punctuation_marks": q14_punctuation,
                "lines": q14_lines,
                "sentences": q14_sentences,
                "questions_count": q14_questions,
                "replies_count": q14_replies,
                "shang_tang_count": q14_shang_tang,
            },
            "van_mon_q15_q16": {
                "pages": "18 - 51",
                "title": "雲門匡真禪師廣錄 卷15-16",
                "cjk_chars": vm_cjk,
                "note": "Thuộc ngữ lục của Thiền sư Vân Môn Văn Yển, không thuộc Triệu Châu.",
            },
        },
        "alignment_coverage": {
            "q14_overlap_items": f"Mục 209 đến 525 ({len(q14_items)} mục)",
            "q14_vi_words": q14_vi_words,
            "q14_zh_cjk": q14_cjk_chars,
            "char_ratio_vi_to_zh": round(char_ratio_q14, 2),
            "missing_zh_in_file": f"Mục 1 đến 208 ({len(q13_items)} mục) thuộc Quyển 13",
            "extraneous_zh_in_file": f"Trang 18 đến 51 ({vm_cjk} chữ Hán) thuộc Ngữ lục Vân Môn",
        },
    }


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    nguon_dir = os.path.join(base_dir, "01_nguon")
    out_dir = os.path.join(base_dir, "03_text_sach", "trieu_chau")
    os.makedirs(out_dir, exist_ok=True)

    vi_pdf = os.path.join(nguon_dir, "Trieu Chau Ngu Luc_VI_Text_ThongPhuong.pdf")
    if not os.path.isfile(vi_pdf):
        vi_pdf = os.path.join(nguon_dir, "Trieu Chau Ngu Luc_VI_Text_ThongPhuong (1).pdf")
    zh_pdf = os.path.join(nguon_dir, "Trieu Chau Ngu Luc_ZH_Text_X1315.pdf")

    print("[1/3] Trích xuất dữ liệu tiếng Việt...")
    vi_data = extract_vietnamese_pdf(vi_pdf)

    print("[2/3] Trích xuất dữ liệu chữ Hán...")
    zh_data = extract_chinese_pdf(zh_pdf)

    print("[3/3] Tính toán thống kê chi tiết...")
    stats = compute_statistics(vi_data, zh_data, vi_pdf, zh_pdf)

    # Xuất các tệp văn bản sạch
    with open(os.path.join(out_dir, "trieu_chau_viet_hanh_trang.txt"), "w", encoding="utf-8") as f:
        f.write(vi_data["hanh_trang"])

    with open(os.path.join(out_dir, "trieu_chau_viet_ngu_luc_525.txt"), "w", encoding="utf-8") as f:
        for num in sorted(vi_data["items"].keys()):
            f.write(f"=== MỤC {num} ===\n{vi_data['items'][num]}\n\n")

    with open(os.path.join(out_dir, "trieu_chau_viet_q13.txt"), "w", encoding="utf-8") as f:
        for num in sorted(k for k in vi_data["items"].keys() if k <= 208):
            f.write(f"=== MỤC {num} ===\n{vi_data['items'][num]}\n\n")

    with open(os.path.join(out_dir, "trieu_chau_viet_q14.txt"), "w", encoding="utf-8") as f:
        for num in sorted(k for k in vi_data["items"].keys() if k >= 209):
            f.write(f"=== MỤC {num} ===\n{vi_data['items'][num]}\n\n")

    with open(os.path.join(out_dir, "trieu_chau_viet_chu_thich_334.txt"), "w", encoding="utf-8") as f:
        for num in sorted(vi_data["footnotes"].keys()):
            f.write(f"[{num}] {vi_data['footnotes'][num]}\n")

    items_json = [
        {"id": k, "text": vi_data["items"][k], "word_count": len(vi_data["items"][k].split())}
        for k in sorted(vi_data["items"].keys())
    ]
    with open(os.path.join(out_dir, "trieu_chau_viet_items.json"), "w", encoding="utf-8") as f:
        json.dump(items_json, f, ensure_ascii=False, indent=2)

    with open(os.path.join(out_dir, "trieu_chau_han_tua.txt"), "w", encoding="utf-8") as f:
        f.write(zh_data["tua_text"])

    with open(os.path.join(out_dir, "trieu_chau_han_q14.txt"), "w", encoding="utf-8") as f:
        f.write(zh_data["q14_text"])

    with open(os.path.join(out_dir, "van_mon_han_q15_q16.txt"), "w", encoding="utf-8") as f:
        f.write(zh_data["van_mon_text"])

    with open(os.path.join(out_dir, "thong_ke_trieu_chau.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("        BÁO CÁO THỐNG KÊ TRIỆU CHÂU NGỮ LỤC")
    print("=" * 60)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
