# -*- coding: utf-8 -*-
"""
Module dóng hàng (alignment) văn bản song ngữ Hán - Việt cấp CÂU & ĐOẠN.
Tuân thủ Bước 6 (Tách câu) & Bước 7 (Dóng hàng) theo Guideline đồ án:
- "Ưu tiên đơn vị nhỏ nhất có ý nghĩa đầy đủ."
- "Không chia cơ học theo dấu câu nếu việc chia làm mất quan hệ dịch."
- Hỗ trợ các quan hệ 1-1, n-1, 1-n, n-m.
- Sử dụng thuật toán quy hoạch động (Dynamic Programming - Gale-Church cải tiến cho Hán - Việt)
  để tìm chuỗi ghép câu tối ưu theo tỷ lệ độ dài ngữ nghĩa.
"""

import os
import re
import pandas as pd
from typing import List, Dict, Tuple
from extract_clean import extract_book, is_cjk_char


def split_han_sentences(text: str) -> List[str]:
    """Tách câu Hán theo các dấu ngắt câu chuẩn 。！？"""
    if not text:
        return []
    raw = [s.strip() for s in re.split(r'([。！？])', text) if s.strip()]
    sents = []
    for i in range(0, len(raw), 2):
        s = raw[i]
        p = raw[i+1] if i+1 < len(raw) else ''
        full = (s + p).strip()
        if full:
            sents.append(full)
    return sents


def split_viet_sentences(text: str) -> List[str]:
    """Tách câu tiếng Việt theo các dấu ngắt câu chuẩn .?!"""
    if not text:
        return []
    raw = [s.strip() for s in re.split(r'([.?!])', text) if s.strip()]
    sents = []
    for i in range(0, len(raw), 2):
        s = raw[i]
        p = raw[i+1] if i+1 < len(raw) else ''
        full = (s + p).strip()
        if len(full) > 2:
            sents.append(full)
    return sents


def align_sentences_in_para(h_text: str, v_text: str) -> List[Tuple[str, str]]:
    """
    Dóng hàng cấp câu bên trong một đoạn song ngữ bằng quy hoạch động (DP).
    Tối ưu hóa hàm chi phí dựa trên tỷ lệ độ dài ký tự đặc trưng Hán - Việt (~3.8 - 4.5 ký tự Việt/1 chữ Hán).
    """
    hs = split_han_sentences(h_text)
    vs = split_viet_sentences(v_text)
    
    # Nếu một trong hai vế không có câu hoặc chỉ có 1 câu
    if not hs or not vs:
        return [(h_text, v_text)]
    if len(hs) == 1 and len(vs) == 1:
        return [(hs[0], vs[0])]
    if len(hs) == 1 or len(vs) == 1:
        return [(' '.join(hs), ' '.join(vs))]
        
    # Hệ số tương quan độ dài: 1 ký tự Hán tương đương ~4.0 ký tự tiếng Việt
    C = 4.0
    
    def cost(h_sub: str, v_sub: str) -> float:
        lh = len(re.sub(r'[^\w\u4e00-\u9fff]', '', h_sub))
        lv = len(re.sub(r'[^\w]', '', v_sub))
        if lh == 0 or lv == 0:
            return 9999.0
        expected_lv = lh * C
        # Chuẩn hóa khoảng cách sai lệch bình phương
        diff = abs(lv - expected_lv) / (expected_lv ** 0.5 + 1e-5)
        return float(diff ** 2)
        
    N, M = len(hs), len(vs)
    dp = [[float('inf')] * (M + 1) for _ in range(N + 1)]
    back = [[None] * (M + 1) for _ in range(N + 1)]
    dp[0][0] = 0.0
    
    # Cho phép các bước chuyển linh hoạt: (số câu Hán, số câu Việt)
    # 1-1, 2-1, 3-1, 4-1, 5-1 (Hán ngắt ngắn hơn Việt)
    # 1-2, 2-2, 3-2, 1-3 (Việt ngắt ngắn hơn Hán)
    moves = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (1, 2), (2, 2), (3, 2), (1, 3)]
    
    for i in range(N + 1):
        for j in range(M + 1):
            if dp[i][j] == float('inf'):
                continue
            for di, dj in moves:
                ni, nj = i + di, j + dj
                if ni <= N and nj <= M:
                    h_sub = ' '.join(hs[i:ni])
                    v_sub = ' '.join(vs[j:nj])
                    c = cost(h_sub, v_sub)
                    if dp[i][j] + c < dp[ni][nj]:
                        dp[ni][nj] = dp[i][j] + c
                        back[ni][nj] = (i, j, di, dj)
                        
    # Nếu không tìm thấy đường đi khả dĩ, giữ nguyên 1-1 cấp đoạn
    if dp[N][M] == float('inf'):
        return [(' '.join(hs), ' '.join(vs))]
        
    # Truy vết đường đi tối ưu
    res = []
    curr_i, curr_j = N, M
    while curr_i > 0 or curr_j > 0:
        b = back[curr_i][curr_j]
        if not b:
            break
        pi, pj, di, dj = b
        h_chunk = ' '.join(hs[pi:curr_i])
        v_chunk = ' '.join(vs[pj:curr_j])
        res.append((h_chunk, v_chunk))
        curr_i, curr_j = pi, pj
        
    res.reverse()
    return res


def align_book_records(records: List[Dict[str, str]], sentence_level: bool = True) -> List[Dict[str, str]]:
    """
    Dóng hàng toàn bộ các đoạn trong sách:
    1. Gộp neo các đoạn Hán liên tiếp nếu đoạn Việt dịch gộp (quan hệ n-1).
    2. Nếu sentence_level=True: chia nhỏ từng đoạn ra các câu song ngữ tương ứng trọn vẹn nghĩa.
    """
    para_aligned = []
    pending_han = []
    pending_tags = []
    
    for r in records:
        tag = r["tag"]
        han = r["han"].strip()
        viet = r["viet"].strip()
        
        if han and viet:
            if pending_han:
                han = ' '.join(pending_han) + ' ' + han
                tag = f"{pending_tags[0]}-{tag}"
                pending_han = []
                pending_tags = []
                
            para_aligned.append({
                "tag": tag,
                "han": han,
                "viet": viet
            })
        elif han and not viet:
            pending_han.append(han)
            pending_tags.append(tag)
        elif not han and viet:
            if pending_han:
                combined_han = ' '.join(pending_han)
                combined_tag = f"{pending_tags[0]}-{pending_tags[-1]}" if len(pending_tags) > 1 else pending_tags[0]
                para_aligned.append({
                    "tag": combined_tag,
                    "han": combined_han,
                    "viet": viet
                })
                pending_han = []
                pending_tags = []
            else:
                para_aligned.append({
                    "tag": tag,
                    "han": "",
                    "viet": viet
                })
                
    if pending_han:
        combined_han = ' '.join(pending_han)
        combined_tag = f"{pending_tags[0]}-{pending_tags[-1]}" if len(pending_tags) > 1 else pending_tags[0]
        para_aligned.append({
            "tag": combined_tag,
            "han": combined_han,
            "viet": ""
        })
        
    if not sentence_level:
        return para_aligned
        
    # Tách nhỏ xuống cấp câu
    sentence_aligned = []
    for p in para_aligned:
        h = p["han"].strip()
        v = p["viet"].strip()
        tag = p["tag"]
        
        if h and v:
            pairs = align_sentences_in_para(h, v)
            for idx, (sh, sv) in enumerate(pairs, start=1):
                sentence_aligned.append({
                    "tag": f"{tag}_s{idx}",
                    "han": sh,
                    "viet": sv
                })
        else:
            # Khuyết 1 vế
            sentence_aligned.append({
                "tag": tag,
                "han": h,
                "viet": v
            })
            
    return sentence_aligned


def export_parallel_data(all_pairs: List[Dict[str, str]], output_tsv: str, output_xlsx: str):
    """
    Xuất dữ liệu dóng hàng ra file TSV và Excel theo đúng định dạng bắt buộc trong Guideline:
    1. File TSV: mỗi dòng chứa đúng 1 cặp phân cách bằng phím tab (<CÂU_HÁN>\t<CÂU_VIỆT>).
    2. File Excel: Sheet tên 'DONG_HANG', đúng 2 cột 'Hán' và 'Việt'.
    """
    os.makedirs(os.path.dirname(output_tsv), exist_ok=True)
    os.makedirs(os.path.dirname(output_xlsx), exist_ok=True)
    
    # 1. Ghi file TSV
    with open(output_tsv, 'w', encoding='utf-8') as f:
        for p in all_pairs:
            han = p['han'].replace('\t', ' ').replace('\n', ' ').strip()
            viet = p['viet'].replace('\t', ' ').replace('\n', ' ').strip()
            f.write(f"{han}\t{viet}\n")
            
    print(f"[+] Đã xuất file TSV: {output_tsv} ({len(all_pairs)} cặp)")
    
    # 2. Ghi file Excel
    df = pd.DataFrame([
        {
            "Hán": p['han'].replace('\n', ' ').strip(),
            "Việt": p['viet'].replace('\n', ' ').strip()
        }
        for p in all_pairs
    ])
    
    with pd.ExcelWriter(output_xlsx, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='DONG_HANG', index=False)
        
    print(f"[+] Đã xuất file Excel: {output_xlsx} (Sheet: DONG_HANG, {len(df)} dòng)")


def export_clean_text_files(all_pairs: List[Dict[str, str]], han_txt_path: str, viet_txt_path: str):
    """
    Xuất các file văn bản Hán và Việt đã làm sạch vào 03_text_sach/
    theo yêu cầu mục 2 của Guideline.
    """
    os.makedirs(os.path.dirname(han_txt_path), exist_ok=True)
    os.makedirs(os.path.dirname(viet_txt_path), exist_ok=True)
    
    with open(han_txt_path, 'w', encoding='utf-8') as fh:
        for p in all_pairs:
            h = p['han'].replace('\n', ' ').strip()
            if h:
                fh.write(h + '\n')
                
    with open(viet_txt_path, 'w', encoding='utf-8') as fv:
        for p in all_pairs:
            v = p['viet'].replace('\n', ' ').strip()
            if v:
                fv.write(v + '\n')
                
    print(f"[+] Đã xuất văn bản sạch: {han_txt_path} và {viet_txt_path}")
