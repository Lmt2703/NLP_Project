"""Module dóng hàng văn bản song ngữ Hán - Việt cấp câu và đoạn.

Phương pháp dóng hàng tối ưu:
1. Tách câu chính xác theo dấu câu Hán (。！？) và dấu câu Việt (.?!), có bảo vệ các từ viết tắt Phật học (HT., TT., ĐĐ., nt., v.v.).
2. Thuật toán quy hoạch động (Dynamic Programming) kết hợp:
   - Tỷ lệ độ dài động theo từng đoạn (Dynamic Paragraph Length Ratio) thay vì gán cứng 4.0.
   - Bảng tiền tố O(1) để tăng tốc độ tính toán DP xuống < 0.1s/đoạn.
   - Đối sánh từ khóa thuật ngữ Phật học (Buddhist Lexical Anchoring) để triệt tiêu hiện tượng lệch dòng dây chuyền.
3. Xuất dữ liệu bàn giao chuẩn TSV (<HÁN>\\t<VIỆT>) và Excel (sheet DONG_HANG, cột 'Hán', 'Việt').
"""

import os
import re
from typing import Dict, List, Set, Tuple
import pandas as pd

from extract_clean import extract_book

# Từ điển thuật ngữ Phật học và thiền môn đối sánh neo nghĩa Hán - Việt
BUDDHIST_DICT: List[Tuple[str, str]] = [
    ("方丈", "phương trượng"),
    ("住持", "trụ trì"),
    ("首座", "thủ tọa"),
    ("西堂", "tây đường"),
    ("後堂", "hậu đường"),
    ("前堂", "tiền đường"),
    ("知事", "tri sự"),
    ("都寺", "đô tự"),
    ("維那", "duy-na"),
    ("維那", "duy na"),
    ("知客", "tri khách"),
    ("典座", "điển tọa"),
    ("直歲", "trực tuế"),
    ("侍者", "thị giả"),
    ("行者", "hành giả"),
    ("僧堂", "tăng đường"),
    ("庫司", "khố ty"),
    ("堂司", "đường ty"),
    ("大眾", "đại chúng"),
    ("和尚", "hòa thượng"),
    ("燒香", "thắp hương"),
    ("燒香", "đốt hương"),
    ("插香", "thắp hương"),
    ("點茶", "đãi trà"),
    ("點茶", "điểm trà"),
    ("點湯", "đãi thang"),
    ("點湯", "điểm thang"),
    ("三拜", "ba lạy"),
    ("一拜", "một lạy"),
    ("巡堂", "tuần hành"),
    ("巡堂", "tuần đường"),
    ("巡寮", "tuần liêu"),
    ("鳴鐘", "đánh chuông"),
    ("鳴板", "đánh bản"),
    ("聖僧", "thánh tăng"),
    ("聖僧", "bàn tổ"),
    ("粥", "cháo"),
    ("飯", "cơm"),
    ("免人事", "miễn việc đảnh lễ"),
    ("掛上堂牌", "treo bảng"),
    ("說法", "thuyết pháp"),
    ("念誦圖", "mô hình tụng niệm"),
    ("展禮", "đảnh lễ"),
    ("喝云", "tuyên bố"),
    ("喝云", "hô lớn"),
    ("謝大眾", "lễ tạ đại chúng"),
    ("五更", "canh năm"),
    ("香几", "bàn hương"),
    ("坐椅", "ghế"),
    ("收盞", "thu chén"),
    ("行茶", "dâng trà"),
    ("結制", "kết chế"),
    ("解制", "giải chế"),
    ("安居", "an cư"),
    ("浴佛", "tắm phật"),
    ("涅槃", "niết-bàn"),
    ("成道", "thành đạo"),
    ("達磨", "đạt-ma"),
    ("達磨", "đạt ma"),
    ("百丈", "bách trượng"),
    ("帝師", "đế sư"),
    ("楞嚴", "lăng nghiêm"),
    ("盆會", "bồn hội"),
    ("盂蘭", "vu lan"),
    ("草單", "thảo đơn"),
    ("板帳", "bản trướng"),
    ("亡僧", "vong tăng"),
    ("亡僧", "người chết"),
    ("衣鉢", "y bát"),
    ("常住", "thường trụ"),
    ("貫", "quan"),
    ("伯", "trăm"),
    ("百", "trăm"),
    ("千", "ngàn"),
    ("正月初一", "tháng giêng"),
    ("二月初一", "tháng hai"),
    ("三月初一", "tháng ba"),
    ("四月初一", "tháng tư"),
    ("五月端午", "tháng năm"),
    ("六月初一", "tháng sáu"),
    ("七月初", "tháng bảy"),
    ("八月初一", "tháng tám"),
    ("九月初一", "tháng chín"),
    ("十月初一", "tháng mười"),
    ("十一月", "tháng mười một"),
    ("十二月", "tháng mười hai"),
]

# Các bước chuyển trạng thái (di_han, dj_viet) được chấp nhận trong thuật toán DP
ALLOWED_TRANSITIONS: List[Tuple[int, int]] = [
    (1, 1),  # 1 câu Hán - 1 câu Việt
    (2, 1),  # 2 câu Hán - 1 câu Việt (n-1)
    (3, 1),  # 3 câu Hán - 1 câu Việt (n-1)
    (4, 1),  # 4 câu Hán - 1 câu Việt (n-1)
    (5, 1),  # 5 câu Hán - 1 câu Việt (n-1)
    (1, 2),  # 1 câu Hán - 2 câu Việt (1-n)
    (2, 2),  # 2 câu Hán - 2 câu Việt (n-m)
    (3, 2),  # 3 câu Hán - 2 câu Việt (n-m)
    (4, 2),  # 4 câu Hán - 2 câu Việt (n-m)
    (1, 3),  # 1 câu Hán - 3 câu Việt (1-n)
    (2, 3),  # 2 câu Hán - 3 câu Việt (n-m)
]


def split_han_sentences(text: str) -> List[str]:
    """Tách câu chữ Hán theo các dấu ngắt câu chuẩn: 。！？"""
    if not text:
        return []
    tokens = [s.strip() for s in re.split(r"([。！？])", text) if s.strip()]
    sentences: List[str] = []
    for i in range(0, len(tokens), 2):
        sent = tokens[i]
        punct = tokens[i + 1] if i + 1 < len(tokens) else ""
        combined = (sent + punct).strip()
        if combined:
            sentences.append(combined)
    return sentences


def split_viet_sentences(text: str) -> List[str]:
    """Tách câu tiếng Việt theo các dấu ngắt câu chuẩn (.?!), bảo vệ các từ viết tắt."""
    if not text:
        return []

    protected = {
        "HT.": "HT#DOT#",
        "TT.": "TT#DOT#",
        "ĐĐ.": "ĐĐ#DOT#",
        "nt.": "nt#DOT#",
        "v.v.": "vv#DOT#",
        "v..v..": "vv#DOT#",
        "Tp.": "Tp#DOT#",
        "TP.": "TP#DOT#",
    }
    t = text
    for k, v in protected.items():
        t = t.replace(k, v)

    tokens = [s.strip() for s in re.split(r"([.?!])", t) if s.strip()]
    sentences: List[str] = []
    for i in range(0, len(tokens), 2):
        sent = tokens[i]
        punct = tokens[i + 1] if i + 1 < len(tokens) else ""
        combined = (sent + punct).strip()
        for k, v in protected.items():
            combined = combined.replace(v, k)
        if len(combined) > 1:
            sentences.append(combined)
    return sentences


def fast_align_sentences(han_sents: List[str], viet_sents: List[str], para_ratio: float) -> List[Tuple[str, str]]:
    """Dóng hàng tối ưu cấp câu sử dụng Quy hoạch động với tiền xử lý O(1) và đối sánh từ khóa."""
    n_h, n_v = len(han_sents), len(viet_sents)
    if n_h == 0 or n_v == 0:
        return [(" ".join(han_sents), " ".join(viet_sents))]
    if n_h == 1 and n_v == 1:
        return [(han_sents[0], viet_sents[0])]
    if n_h == 1 or n_v == 1:
        return [(" ".join(han_sents), " ".join(viet_sents))]

    # Tiền tính toán độ dài ký tự thực tế
    h_lens = [len(re.sub(r"[^\w\u4e00-\u9fff]", "", s)) for s in han_sents]
    v_lens = [len(re.sub(r"[^\w]", "", s)) for s in viet_sents]

    # Tiền tính toán mảng cộng dồn tiền tố (prefix sum) để truy vấn độ dài O(1)
    h_pref = [0] * (n_h + 1)
    for i in range(n_h):
        h_pref[i + 1] = h_pref[i] + h_lens[i]

    v_pref = [0] * (n_v + 1)
    for j in range(n_v):
        v_pref[j + 1] = v_pref[j] + v_lens[j]

    # Tiền tính toán tập chỉ số từ khóa Phật học có mặt trong từng câu
    h_kw_sets = [set(idx for idx, (h_kw, _) in enumerate(BUDDHIST_DICT) if h_kw in s) for s in han_sents]
    v_kw_sets = [set(idx for idx, (_, v_kw) in enumerate(BUDDHIST_DICT) if v_kw in s.lower()) for s in viet_sents]

    dp_cost = [[float("inf")] * (n_v + 1) for _ in range(n_h + 1)]
    backtrack = [[None] * (n_v + 1) for _ in range(n_h + 1)]
    dp_cost[0][0] = 0.0

    for i in range(n_h + 1):
        for j in range(n_v + 1):
            if dp_cost[i][j] == float("inf"):
                continue
            for di, dj in ALLOWED_TRANSITIONS:
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

                        # Thưởng điểm cho các cặp có từ khóa Phật học tương ứng
                        kws_h: Set[int] = set()
                        for si in range(i, ni):
                            kws_h.update(h_kw_sets[si])
                        kws_v: Set[int] = set()
                        for sj in range(j, nj):
                            kws_v.update(v_kw_sets[sj])
                        kw_matches = len(kws_h & kws_v)
                        step_cost = max(0.01, len_cost - (kw_matches * 6.0))

                    if dp_cost[i][j] + step_cost < dp_cost[ni][nj]:
                        dp_cost[ni][nj] = dp_cost[i][j] + step_cost
                        backtrack[ni][nj] = (i, j)

    if dp_cost[n_h][n_v] == float("inf"):
        return [(" ".join(han_sents), " ".join(viet_sents))]

    results: List[Tuple[str, str]] = []
    curr_i, curr_j = n_h, n_v
    while curr_i > 0 or curr_j > 0:
        prev = backtrack[curr_i][curr_j]
        if not prev:
            break
        pi, pj = prev
        results.append((" ".join(han_sents[pi:curr_i]), " ".join(viet_sents[pj:curr_j])))
        curr_i, curr_j = pi, pj

    results.reverse()
    return results


def align_book_records(records: List[Dict[str, str]], sentence_level: bool = True) -> List[Dict[str, str]]:
    """Dóng hàng các bản ghi của một quyển sách ở cấp câu hoặc cấp đoạn."""
    if not sentence_level:
        return [
            {"tag": r["tag"], "han": r["han"].strip(), "viet": r["viet"].strip()}
            for r in records
        ]

    sentence_pairs: List[Dict[str, str]] = []
    for r in records:
        h = r["han"].strip()
        v = r["viet"].strip()
        tag = r["tag"]

        if h and v:
            h_sents = split_han_sentences(h)
            v_sents = split_viet_sentences(v)

            len_h = len(re.sub(r"[^\w\u4e00-\u9fff]", "", h))
            len_v = len(re.sub(r"[^\w]", "", v))
            para_ratio = (len_v / len_h) if len_h > 0 else 4.0
            para_ratio = max(2.5, min(para_ratio, 7.0))

            aligned = fast_align_sentences(h_sents, v_sents, para_ratio)
            for idx, (sh, sv) in enumerate(aligned, start=1):
                sentence_pairs.append({
                    "tag": f"{tag}_s{idx}",
                    "han": sh,
                    "viet": sv,
                })
        else:
            sentence_pairs.append({"tag": tag, "han": h, "viet": v})

    return sentence_pairs


def export_parallel_data(all_pairs: List[Dict[str, str]], output_tsv: str, output_xlsx: str) -> None:
    """Xuất tập dữ liệu dóng hàng ra file TSV và Excel theo chuẩn nghiệm thu đề tài."""
    os.makedirs(os.path.dirname(output_tsv), exist_ok=True)
    os.makedirs(os.path.dirname(output_xlsx), exist_ok=True)

    with open(output_tsv, "w", encoding="utf-8") as f:
        for p in all_pairs:
            h = p["han"].replace("\t", " ").replace("\n", " ").strip()
            v = p["viet"].replace("\t", " ").replace("\n", " ").strip()
            f.write(f"{h}\t{v}\n")

    dataframe = pd.DataFrame([
        {
            "Hán": p["han"].replace("\n", " ").strip(),
            "Việt": p["viet"].replace("\n", " ").strip(),
        }
        for p in all_pairs
    ])

    with pd.ExcelWriter(output_xlsx, engine="openpyxl") as writer:
        dataframe.to_excel(writer, sheet_name="DONG_HANG", index=False)


def export_clean_text_files(all_pairs: List[Dict[str, str]], han_path: str, viet_path: str) -> None:
    """Xuất văn bản đơn ngữ Hán và Việt đã làm sạch sang thư mục 03_text_sach/."""
    os.makedirs(os.path.dirname(han_path), exist_ok=True)
    os.makedirs(os.path.dirname(viet_path), exist_ok=True)

    with open(han_path, "w", encoding="utf-8") as fh:
        for p in all_pairs:
            h = p["han"].replace("\n", " ").strip()
            if h:
                fh.write(h + "\n")

    with open(viet_path, "w", encoding="utf-8") as fv:
        for p in all_pairs:
            v = p["viet"].replace("\n", " ").strip()
            if v:
                fv.write(v + "\n")
