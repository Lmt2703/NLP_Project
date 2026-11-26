"""Bộ điều phối dóng hàng song ngữ Hán - Việt cho Triệu Châu Ngữ Lục (CV09).

Quy trình chuẩn hóa:
1. Nạp văn bản Hán Q14 (CBETA X68n1315) và Việt (Mục 209, Mục 225-525).
   - Tách lọc 15 mục ngoại suy (Mục 210-224) không có trong bản Hán CBETA Q14.
   - Loại bỏ dòng lạc khoản colophon CBETA cuối sách chữ Hán.
2. Làm sạch chú thích chân trang bám dính từ vựng.
3. Tách câu bằng bộ tách câu chuẩn (split_han_sentences, split_viet_sentences).
4. Dóng hàng cấp câu bằng Quy hoạch động (DP) có phân vai đối thoại (Dialogue Role Matching):
   - Nhận diện vai trò: Câu hỏi (問 / Tăng hỏi), Câu đáp (師云 / Sư đáp/bảo/dạy).
   - Phạt nặng (+400) trường hợp râu ông nọ cắm cằm bà kia (Hán Hỏi ghép Việt Đáp hoặc ngược lại).
   - Thưởng điểm (-60) khi đúng vai trò đối thoại.
   - Cho phép các bước chuyển linh hoạt (1-1, 1-2, 1-3, 2-1, 2-2...) không bị cản trở bởi merge penalty cứng.
5. Xuất dữ liệu bàn giao: TSV, Excel (sheet DONG_HANG), văn bản đơn ngữ sạch.
6. Đánh giá kiểm thử chất lượng và cập nhật báo cáo Markdown.
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from typing import List, Tuple

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from aligner import (
    BUDDHIST_DICT,
    export_clean_text_files,
    export_parallel_data,
    split_han_sentences,
    split_viet_sentences,
)
from evaluate import evaluate_parallel_files, print_evaluation_report
from extract_trieu_chau import extract_chinese_pdf, extract_vietnamese_pdf
from trieu_chau_refiner import refine_trieu_chau_pairs


def clean_viet_footnotes(text: str) -> str:
    """Xóa số chỉ mục chú thích dính liền chữ (ví dụ: lỗi122, như123, Thích124...)."""
    pattern = r"(?<=[a-zA-Z\u00C0-\u1EF9\]\"\x27\u201c\u201d\u2018\u2019\)])(\d{1,3})(?=[\s.?!,;:\]\)\x27\"\u201c\u201d\u2018\u2019]|$)"
    return re.sub(pattern, "", text)


def align_dialogue_sentences(
    h_sents: List[str], v_sents: List[str], para_ratio: float = 3.65
) -> List[Tuple[str, str]]:
    """Thuật toán DP dóng hàng thông minh có kiểm soát vai trò đối thoại (Question/Answer)."""
    n_h, n_v = len(h_sents), len(v_sents)
    if n_h == 0 or n_v == 0:
        return [(" ".join(h_sents), " ".join(v_sents))]

    # Làm sạch khoảng trắng CJK
    clean_h = [
        re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", s)
        for s in h_sents
    ]

    h_lens = [len(re.sub(r"[^\w\u4e00-\u9fff]", "", s)) for s in clean_h]
    v_lens = [len(re.sub(r"[^\w]", "", s)) for s in v_sents]

    h_pref = [0] * (n_h + 1)
    for i in range(n_h):
        h_pref[i + 1] = h_pref[i] + h_lens[i]

    v_pref = [0] * (n_v + 1)
    for j in range(n_v):
        v_pref[j + 1] = v_pref[j] + v_lens[j]

    # Nhận diện vai trò đối thoại: 1: Câu hỏi, 2: Câu đáp, 0: Khác
    h_roles = []
    for s in clean_h:
        if s.startswith("問") or "問：" in s or "問:" in s:
            h_roles.append(1)
        elif (
            s.startswith("師云")
            or "師云" in s
            or s.startswith("師乃")
            or s.startswith("師便")
            or s.startswith("師上堂")
            or s.startswith("師示眾")
            or s.startswith("師叱")
            or s.startswith("師呵呵")
            or s.startswith("師代")
        ):
            h_roles.append(2)
        else:
            h_roles.append(0)

    v_roles = []
    for s in v_sents:
        sl = s.lower()
        if (
            "tăng hỏi" in sl
            or "hỏi:" in sl
            or "hỏi：“" in sl
            or "hỏi: “" in sl
            or sl.startswith("hỏi")
            or sl.startswith("- hỏi")
        ):
            v_roles.append(1)
        elif (
            "sư đáp" in sl
            or "sư bảo" in sl
            or "sư nói" in sl
            or "sư dạy" in sl
            or "đáp:" in sl
            or "sư liền" in sl
            or "sư cười" in sl
            or sl.startswith("sư")
        ):
            v_roles.append(2)
        else:
            v_roles.append(0)

    # Từ điển mỏ neo
    h_kw_sets = [
        set(idx for idx, (h_kw, _) in enumerate(BUDDHIST_DICT) if h_kw in s)
        for s in clean_h
    ]
    v_kw_sets = [
        set(idx for idx, (_, v_kw) in enumerate(BUDDHIST_DICT) if v_kw in s.lower())
        for s in v_sents
    ]

    transitions = [
        (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
        (1, 2), (2, 2), (3, 2),
        (1, 3), (2, 3), (1, 4),
    ]

    dp_cost = [[float("inf")] * (n_v + 1) for _ in range(n_h + 1)]
    backtrack = [[None] * (n_v + 1) for _ in range(n_h + 1)]
    dp_cost[0][0] = 0.0

    for i in range(n_h + 1):
        for j in range(n_v + 1):
            if dp_cost[i][j] == float("inf"):
                continue
            for di, dj in transitions:
                ni, nj = i + di, j + dj
                if ni <= n_h and nj <= n_v:
                    sub_len_h = h_pref[ni] - h_pref[i]
                    sub_len_v = v_pref[nj] - v_pref[j]
                    if sub_len_h == 0 or sub_len_v == 0:
                        step_cost = 9999.0
                    else:
                        expected_v = sub_len_h * para_ratio
                        delta = abs(sub_len_v - expected_v) / (expected_v ** 0.5 + 1e-5)
                        len_cost = delta ** 2

                        # Phạt nặng lỗi trôi vai đối thoại (Hỏi ghép Đáp hoặc ngược lại)
                        r_h = h_roles[i]
                        r_v = v_roles[j]
                        role_cost = 0.0
                        if (r_h == 1 and r_v == 2) or (r_h == 2 and r_v == 1):
                            role_cost = 450.0  # Phạt nặng chống lệch dòng
                        elif (r_h == 1 and r_v == 1) or (r_h == 2 and r_v == 2):
                            role_cost = -60.0  # Thưởng điểm khi khớp đúng vai thoại

                        # Khớp từ khóa mỏ neo Phật học
                        kws_h = set()
                        for si in range(i, ni):
                            kws_h.update(h_kw_sets[si])
                        kws_v = set()
                        for sj in range(j, nj):
                            kws_v.update(v_kw_sets[sj])
                        kw_matches = len(kws_h & kws_v)

                        merge_penalty = 6.0 * (dj - 1) if dj > 1 else 0.0
                        step_cost = len_cost + role_cost + merge_penalty - (kw_matches * 50.0)

                    if dp_cost[i][j] + step_cost < dp_cost[ni][nj]:
                        dp_cost[ni][nj] = dp_cost[i][j] + step_cost
                        backtrack[ni][nj] = (i, j)

    results = []
    curr_i, curr_j = n_h, n_v
    while curr_i > 0 or curr_j > 0:
        prev = backtrack[curr_i][curr_j]
        if not prev:
            break
        pi, pj = prev
        results.append((" ".join(h_sents[pi:curr_i]), " ".join(v_sents[pj:curr_j])))
        curr_i, curr_j = pi, pj

    results.reverse()
    return results


def main() -> None:
    start_time = time.time()
    base_folder = os.path.abspath(os.path.join(SRC_DIR, ".."))
    nguon_dir = os.path.join(base_folder, "01_nguon")
    trieu_chau_dir = os.path.join(base_folder, "03_text_sach", "trieu_chau")
    dong_hang_dir = os.path.join(base_folder, "04_dong_hang")

    banner = "=" * 65
    print(f"\n{banner}")
    print("   PIPELINE DÓNG HÀNG CHUẨN XÁC: TRIỆU CHÂU NGỮ LỤC (CV09)")
    print(banner)

    vi_pdf = os.path.join(nguon_dir, "Trieu Chau Ngu Luc_VI_Text_ThongPhuong (1).pdf")
    zh_pdf = os.path.join(nguon_dir, "Trieu Chau Ngu Luc_ZH_Text_X1315.pdf")
    vi_data = extract_vietnamese_pdf(vi_pdf)
    zh_data = extract_chinese_pdf(zh_pdf)

    zh_text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", zh_data["q14_text"])

    colophon_marker = "廬山棲賢寶覺禪院住持傳法賜紫沙門"
    if colophon_marker in zh_text:
        zh_text = zh_text[:zh_text.find(colophon_marker)].strip()

    items = [{"id": k, "text": v} for k, v in sorted(vi_data["items"].items())]
    matched_items = [it for it in items if it["id"] == 209 or 225 <= it["id"] <= 525]

    print(f"[*] Dữ liệu Hán Q14: {len(zh_text):,} ký tự")
    print(f"[*] Dữ liệu Việt Q14 khớp chuẩn: {len(matched_items)} mục (Mục 209 & 225–525)")

    vi_raw = "\n\n".join(it["text"] for it in matched_items)
    vi_clean = clean_viet_footnotes(vi_raw)

    han_sents = split_han_sentences(zh_text)
    viet_sents = split_viet_sentences(vi_clean)

    print(f"[*] Tách câu Hán:  {len(han_sents)} câu")
    print(f"[*] Tách câu Việt: {len(viet_sents)} câu")

    zh_cjk_count = sum(1 for c in zh_text if '\u4e00' <= c <= '\u9fff')
    vi_char_count = len(re.sub(r"[^\w]", "", vi_clean))
    char_ratio = round(vi_char_count / zh_cjk_count, 2) if zh_cjk_count > 0 else 3.65
    print(f"[*] Tỷ lệ ký tự Việt/Hán: {char_ratio}")

    print(f"\n>>> Đang dóng hàng với thuật toán phân vai đối thoại (Anti-Drift DP)...")
    t0 = time.time()
    aligned_pairs = align_dialogue_sentences(han_sents, viet_sents, char_ratio)
    t1 = time.time()
    print(f"    -> Hoàn thành DP thô trong {t1 - t0:.2f} giây ({len(aligned_pairs)} cặp)")

    print(f">>> Đang tinh chỉnh phân đoạn và căn chỉnh chuẩn hóa 100%...")
    aligned_pairs = refine_trieu_chau_pairs(aligned_pairs)
    print(f"    -> Tổng số cặp dóng hàng sau tinh chỉnh: {len(aligned_pairs)} cặp câu")

    pair_dicts = [
        {"tag": f"TC_Q14_s{i+1}", "han": h, "viet": v}
        for i, (h, v) in enumerate(aligned_pairs)
    ]

    os.makedirs(dong_hang_dir, exist_ok=True)
    tsv_path = os.path.join(dong_hang_dir, "TrieuChauNguLuc_parallel.tsv")
    xlsx_path = os.path.join(dong_hang_dir, "TrieuChauNguLuc_parallel.xlsx")
    export_parallel_data(pair_dicts, tsv_path, xlsx_path)
    print(f"\n[+] Xuất TSV:   {tsv_path}")
    print(f"[+] Xuất Excel: {xlsx_path}")

    han_out = os.path.join(trieu_chau_dir, "trieu_chau_han.txt")
    viet_out = os.path.join(trieu_chau_dir, "trieu_chau_viet.txt")
    export_clean_text_files(pair_dicts, han_out, viet_out)

    report = evaluate_parallel_files(tsv_path, xlsx_path)
    print_evaluation_report(report)

    # Cập nhật ngữ liệu tổng hợp 4 quyển và báo cáo hợp nhất
    from build_master_corpus import build_master_and_report
    build_master_and_report()

    elapsed = round(time.time() - start_time, 2)
    print(f"[+] Toàn bộ pipeline Triệu Châu thực thi xong trong: {elapsed} giây.")
    print(f"{banner}\n")


if __name__ == "__main__":
    main()
