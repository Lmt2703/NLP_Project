"""Module dóng hàng văn bản song ngữ Hán - Việt cấp câu và đoạn.

Triển khai thuật toán quy hoạch động (Dynamic Programming) dựa trên hàm
khoảng cách tương quan độ dài ký tự đặc trưng Hán - Việt để ghép câu tối ưu.
Hỗ trợ linh hoạt các quan hệ dóng hàng 1-1, 1-n, n-1, n-m theo quy chuẩn NLP.
"""

import os
import re
from typing import Dict, List, Tuple
import pandas as pd

from extract_clean import extract_book

# Tỷ lệ ký tự trung bình: 1 chữ Hán tương đương khoảng 4.0 ký tự tiếng Việt có dấu
DEFAULT_LENGTH_RATIO = 4.0

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
    (1, 3),  # 1 câu Hán - 3 câu Việt (1-n)
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
    """Tách câu tiếng Việt theo các dấu ngắt câu chuẩn: .?!"""
    if not text:
        return []
    tokens = [s.strip() for s in re.split(r"([.?!])", text) if s.strip()]
    sentences: List[str] = []
    for i in range(0, len(tokens), 2):
        sent = tokens[i]
        punct = tokens[i + 1] if i + 1 < len(tokens) else ""
        combined = (sent + punct).strip()
        if len(combined) > 2:
            sentences.append(combined)
    return sentences


def align_sentences_in_para(h_text: str, v_text: str) -> List[Tuple[str, str]]:
    """Dóng hàng cấp câu bên trong một đoạn song ngữ bằng quy hoạch động."""
    han_sents = split_han_sentences(h_text)
    viet_sents = split_viet_sentences(v_text)

    if not han_sents or not viet_sents:
        return [(h_text, v_text)]
    if len(han_sents) == 1 and len(viet_sents) == 1:
        return [(han_sents[0], viet_sents[0])]
    if len(han_sents) == 1 or len(viet_sents) == 1:
        return [(" ".join(han_sents), " ".join(viet_sents))]

    def alignment_cost(h_sub: str, v_sub: str) -> float:
        len_h = len(re.sub(r"[^\w\u4e00-\u9fff]", "", h_sub))
        len_v = len(re.sub(r"[^\w]", "", v_sub))
        if len_h == 0 or len_v == 0:
            return 9999.0
        expected_v = len_h * DEFAULT_LENGTH_RATIO
        delta = abs(len_v - expected_v) / (expected_v ** 0.5 + 1e-5)
        return float(delta ** 2)

    n_h, n_v = len(han_sents), len(viet_sents)
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
                    sub_h = " ".join(han_sents[i:ni])
                    sub_v = " ".join(viet_sents[j:nj])
                    step_cost = alignment_cost(sub_h, sub_v)
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
    paragraph_pairs: List[Dict[str, str]] = []
    pending_han: List[str] = []
    pending_tags: List[str] = []

    for r in records:
        tag = r["tag"]
        han = r["han"].strip()
        viet = r["viet"].strip()

        if han and viet:
            if pending_han:
                han = " ".join(pending_han) + " " + han
                tag = f"{pending_tags[0]}-{tag}"
                pending_han.clear()
                pending_tags.clear()
            paragraph_pairs.append({"tag": tag, "han": han, "viet": viet})
        elif han and not viet:
            pending_han.append(han)
            pending_tags.append(tag)
        elif not han and viet:
            if pending_han:
                combined_han = " ".join(pending_han)
                combined_tag = f"{pending_tags[0]}-{pending_tags[-1]}" if len(pending_tags) > 1 else pending_tags[0]
                paragraph_pairs.append({"tag": combined_tag, "han": combined_han, "viet": viet})
                pending_han.clear()
                pending_tags.clear()
            else:
                paragraph_pairs.append({"tag": tag, "han": "", "viet": viet})

    if pending_han:
        combined_han = " ".join(pending_han)
        combined_tag = f"{pending_tags[0]}-{pending_tags[-1]}" if len(pending_tags) > 1 else pending_tags[0]
        paragraph_pairs.append({"tag": combined_tag, "han": combined_han, "viet": ""})

    if not sentence_level:
        return paragraph_pairs

    sentence_pairs: List[Dict[str, str]] = []
    for pair in paragraph_pairs:
        h = pair["han"].strip()
        v = pair["viet"].strip()
        tag = pair["tag"]

        if h and v:
            aligned_sents = align_sentences_in_para(h, v)
            for idx, (sh, sv) in enumerate(aligned_sents, start=1):
                sentence_pairs.append({
                    "tag": f"{tag}_s{idx}",
                    "han": sh,
                    "viet": sv,
                })
        else:
            sentence_pairs.append({"tag": tag, "han": h, "viet": v})

    return sentence_pairs


def export_parallel_data(all_pairs: List[Dict[str, str]], output_tsv: str, output_xlsx: str) -> None:
    """Xuất tập dữ liệu dóng hàng ra file TSV và Excel theo định dạng bàn giao chuẩn."""
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
