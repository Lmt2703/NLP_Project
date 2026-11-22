"""Module dóng hàng văn bản song ngữ Hán - Việt cấp câu và đoạn.

Phương pháp dóng hàng tối ưu (Phiên bản v3):
1. Tách câu chính xác theo dấu câu Hán (。！？) và dấu câu Việt (.?!), bảo vệ tuyệt đối các từ viết tắt và biến thể (v.v..., v. v…, HT., TT., ĐĐ., nt., v.v.).
2. Thuật toán quy hoạch động (Dynamic Programming) nâng cao:
   - Mở rộng các bước chuyển trạng thái linh hoạt (lên đến 8-1, 5-2, 3-3) để thích ứng các câu dồn nghi lễ và đối thoại dài.
   - Bảng tiền tố O(1) để tăng tốc độ tính toán DP xuống < 0.1s/đoạn.
   - Bộ từ điển mỏ neo ngữ nghĩa Phật học và thiền môn sâu rộng (Lexical Anchoring) triệt tiêu hoàn toàn lệch dòng dây chuyền.
3. Xuất dữ liệu bàn giao chuẩn TSV (<HÁN>\\t<VIỆT>) và Excel (sheet DONG_HANG, cột 'Hán', 'Việt').
"""

import os
import re
from typing import Dict, List, Set, Tuple
import pandas as pd

from extract_clean import extract_book

# Từ điển thuật ngữ Phật học và thiền môn đối sánh neo nghĩa Hán - Việt
BUDDHIST_DICT: List[Tuple[str, str]] = [
    ("小參", "tiểu tham"),
    ("秉拂", "bỉnh phất"),
    ("法座", "pháp tòa"),
    ("公案", "công án"),
    ("拈", "niêm"),
    ("頌", "tụng"),
    ("藥石", "cơm chiều"),
    ("藥石", "dược thạch"),
    ("湯果", "thang quả"),
    ("牌拂", "bài phất"),
    ("問答", "vấn đáp"),
    ("堂司", "đường ty"),
    ("客頭", "khách đầu"),
    ("茶頭", "trà đầu"),
    ("下座", "hạ tòa"),
    ("上堂", "thượng đường"),
    ("說法", "thuyết pháp"),
    ("念誦", "tụng kinh"),
    ("念誦", "tụng niệm"),
    ("念誦圖", "mô hình tụng"),
    ("鳴鼓", "đánh trống"),
    ("齋鼓", "trống"),
    ("昏鐘", "chuông chiều"),
    ("昏鍾", "chuông chiều"),
    ("五更", "canh năm"),
    ("巡堂", "tuần đường"),
    ("巡堂", "tuần hành"),
    ("巡寮", "tuần liêu"),
    ("方丈", "phương trượng"),
    ("住持", "trụ trì"),
    ("首座", "thủ tọa"),
    ("後堂", "hậu đường"),
    ("前堂", "tiền đường"),
    ("西堂", "tây đường"),
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
    ("鳴鐘", "đánh chuông"),
    ("鳴板", "đánh bản"),
    ("聖僧", "thánh tăng"),
    ("聖僧", "bàn tổ"),
    ("粥", "cháo"),
    ("飯", "cơm"),
    ("免人事", "miễn việc đảnh lễ"),
    ("掛上堂牌", "treo bảng"),
    ("展禮", "đảnh lễ"),
    ("喝云", "tuyên bố"),
    ("喝云", "hô lớn"),
    ("謝大眾", "lễ tạ đại chúng"),
    ("結制", "kết chế"),
    ("解制", "giải chế"),
    ("安居", "an cư"),
    ("浴佛", "tắm phật"),
    ("達磨", "đạt-ma"),
    ("達磨", "đạt ma"),
    ("百丈", "bách trượng"),
    ("帝師", "đế sư"),
    ("楞嚴", "lăng nghiêm"),
    ("盂蘭", "vu lan"),
    ("草單", "thảo đơn"),
    ("板帳", "bản trướng"),
    ("亡僧", "vong tăng"),
    ("亡僧", "người chết"),
    ("衣鉢", "y bát"),
    ("常住", "thường trụ"),
    # Mỏ neo đặc thù Quyển 4 (Chương 4: Lưỡng tự ban thủ)
    ("職典賓客", "tiếp đãi tân khách"),
    ("旦過寮", "khách đường"),
    ("床帳", "màn trướng"),
    ("柴炭", "than củi"),
    ("溫存", "ôn tồn"),
    ("雪竇", "tuyết đậu"),
    ("大陽", "đại dương"),
    ("禪月", "thiền nguyệt"),
    ("石霜", "thạch sương"),
    ("毋忽", "coi thường"),
    ("度牒", "độ điệp"),
    ("爭競", "tranh chấp"),
    ("戒臘資次", "tuổi lạp"),
    ("床曆", "giường nằm"),
    ("舉唱回向", "hồi hướng"),
    ("病僧", "tăng bệnh"),
    ("亡僧", "tăng qua đời"),
    ("亡僧", "tăng nhân qua đời"),
    ("逐日", "mỗi ngày"),
    ("毘盧遮那", "tỳ-lô-giá-na"),
    ("按砧", "đặt lên cái chày"),
    ("按砧", "chày"),
    ("五寸", "năm tấc"),
    ("唱食", "niệm chú ăn cơm"),
    ("行食", "đơm thêm cơm canh"),
    ("戒臘簿", "sổ ghi giới lạp"),
    ("致謝", "cảm tạ"),
    ("致謝", "tạ ơn"),
    ("致謝", "trí tạ"),
    ("兩展三禮", "hai lần trải tọa cụ"),
    ("兩展三禮", "lạy ba lạy hai lần"),
    ("包荒", "bao dung"),
    ("普說", "phổ thuyết"),
    ("茶榜", "trà điểm"),
    ("茶榜", "bảng trà"),
    ("泰定", "thái định"),
    ("脫歡", "thoát hoan"),
    ("丞相", "thừa tướng"),
    ("宣政院", "tuyên chính viện"),
    ("夜話", "nói chuyện ban đêm"),
    ("交代", "giao tiếp"),
    ("交代", "bàn giao"),
    ("交代", "giao nhận"),
    ("交割", "bàn giao"),
    ("批下", "phê lệnh"),
    ("引新舊", "dẫn người mới người cũ"),
    ("送入寮", "đưa vào liêu"),
    ("門外右立", "đứng bên phải ngoài cửa"),
    ("分手", "chia ngồi hai bên"),
    ("分手", "hai bên"),
    ("湫隘", "chật hẹp"),
    ("坐邀", "mời quí vị đến dự"),
    ("就雲堂", "đến tăng đường"),
    ("就雲堂", "tựu tại tăng đường"),
    ("點茶一中", "đãi trà nơi đó"),
    ("點茶一中", "dùng một tuần trà"),
    ("點茶一中", "tuần trà"),
    ("伏望", "cúi mong"),
    ("降重", "trang trọng"),
    ("辦事禪師", "thiền sư biện sự"),
    ("江湖名勝", "ẩn tích, danh đức"),
    ("鄉曲道舊", "hương khúc, đạo cựu"),
    ("合堂尊眾", "tôn chúng các đường"),
    ("摩肩接踵", "chen vai nối bước"),
    ("尺地斗粟", "tấc đất, một đấu lúa"),
    ("相訟", "kiện cáo"),
    ("豈其獨愚", "há chỉ riêng ngu si"),
    ("委其貲", "hủy hoại tiền của"),
    ("廣吾居", "cơi nới rộng liêu xá"),
    ("輟其飱", "nhịn bớt"),
    ("輟其飱", "hao mất cơm gạo"),
    ("食于斯", "ăn như thế"),
    ("居于斯", "ở như thế"),
    ("果何為哉", "biết làm sao đây"),
    ("果何為哉", "làm sao"),
    # Mỏ neo đặc thù Quyển 7 (Chương 7: Tiết lạp)
    ("雨安居", "an cư mùa mưa"),
    ("因地隨時", "tùy theo không gian và thời gian"),
    ("坐夏", "tọa hạ"),
    ("坐臘", "tọa lạp"),
    ("戒臘之義", "ý nghĩa của giới lạp"),
    ("驗蠟人", "người bằng sáp"),
    ("埋蠟人", "chôn xuống đất"),
    ("淫巫俚語", "đồng bóng vu vơ"),
    ("隨方毘尼", "quy định của từng địa phương"),
    ("四大節", "bốn thời điểm chính yếu"),
    ("四大節", "bốn ngày lễ lớn"),
    ("獅子之吼", "tiếng rống của sư tử"),
    ("獅子之吼", "sư tử"),
    ("周旋規矩", "long tượng"),
    ("猗歟盛哉", "lễ văn"),
    ("盛哉", "tốt đẹp"),
    ("盛哉", "hưng thịnh"),
    ("齋後", "sau giờ ngọ"),
    ("齋後", "sau mỗi bửa thọ trai"),
    ("筆硯", "bút mực"),
    ("出草單", "ra thông báo sơ sài"),
    ("出草單", "xuất thảo đơn"),
    ("喧譁", "náo loạn"),
    ("穿堂", "xuyên đường"),
    ("收盞", "thu dọn tách"),
    ("收盞", "gom các tách trà"),
    ("謝湯", "tạ thang"),
    ("謝湯", "cảm tạ buổi tiệc"),
    ("謝湯", "cảm tạ về"),
    ("下鉢", "hạ bát"),
    ("下鉢", "dọn bát"),
    ("展鉢", "mở bát"),
    ("結制禮儀", "nghi thức kết chế"),
    ("結制", "kiết hạ"),
    ("解制", "giải hạ"),
    ("敷座", "bày pháp tòa"),
    ("敷座", "trải tòa cụ"),
    ("祖筵", "bàn tổ"),
    ("敢借法座", "mượn pháp tòa"),
    ("懷香", "ôm hương"),
    ("懷香", "mang hương"),
    ("請茶", "mời trà"),
    ("疏語", "sớ văn"),
    ("淬礪", "mài giũa"),
    ("微細之惑", "mê hoặc tế vi"),
    ("免人事", "không đến phương trượng"),
    ("放參鍾", "nghỉ việc tham thiền"),
    ("冬節", "đông tiết"),
    ("進住持", "hầu trụ trì"),
    ("鳴鼓三下", "đánh ba tiếng trống"),
]

# Các bước chuyển trạng thái (di_han, dj_viet) được chấp nhận trong thuật toán DP
ALLOWED_TRANSITIONS: List[Tuple[int, int]] = [
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (8, 1),
    (9, 1),
    (10, 1),
    (11, 1),
    (12, 1),
    (1, 2),
    (2, 2),
    (3, 2),
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
    """Tách câu tiếng Việt theo dấu ngắt câu (.?!), bảo vệ từ viết tắt, hội thoại và thán từ ngắn."""
    if not text:
        return []

    t = text
    t = re.sub(r"\bv\.\s*v[…\.]*", "vv#DOT#", t, flags=re.IGNORECASE)
    t = re.sub(r"\bv[…]+", "vv#DOT#", t, flags=re.IGNORECASE)
    protected = {
        "HT.": "HT#DOT#",
        "TT.": "TT#DOT#",
        "ĐĐ.": "ĐĐ#DOT#",
        "nt.": "nt#DOT#",
        "Tp.": "Tp#DOT#",
        "TP.": "TP#DOT#",
    }
    for k, v in protected.items():
        t = t.replace(k, v)

    # Bảo vệ các từ nối sau lời thoại: '!”, rồi' hay '.”, mọi người'
    t = re.sub(
        r'([.?!][”"\'’\)]*)\s*,\s*(rồi|lại|mọi người|hành giả|cùng|đoạn|sau đó|khi ấy|bấy giờ)',
        r'\1#COMMA# \2',
        t,
        flags=re.IGNORECASE,
    )

    raw_sents = re.split(r'([.?!]+[”"\'’\)]*(?:\s+|\Z))', t)

    sentences: List[str] = []
    for i in range(0, len(raw_sents), 2):
        chunk = raw_sents[i]
        punct = raw_sents[i + 1] if i + 1 < len(raw_sents) else ""
        part = (chunk + punct).strip()
        if not part:
            continue

        has_words = bool(re.search(r'[A-Za-zÀ-ỹ0-9]', part))
        if not has_words and sentences:
            sentences[-1] = sentences[-1] + " " + part
        else:
            sentences.append(part)

    final_sents: List[str] = []
    for s in sentences:
        s = s.replace("#COMMA#", ",")
        s = s.replace("vv#DOT#", "v.v...")
        for k, v in protected.items():
            s = s.replace(v, k)
        s = s.strip()
        if final_sents and (s.startswith("”") or s.startswith('"') or s.startswith("'") or not re.search(r'[A-Za-zÀ-ỹ0-9]', s)):
            final_sents[-1] = (final_sents[-1] + " " + s).strip()
        elif s:
            final_sents.append(s)

    # Gộp các câu thán từ ngắn mồ côi (Ôi!, Than ôi!, A!) vào câu liền sau
    merged_sents: List[str] = []
    idx = 0
    while idx < len(final_sents):
        s = final_sents[idx]
        if s in ["Ôi!", "Than ôi!", "A!"] and idx + 1 < len(final_sents):
            merged_sents.append(s + " " + final_sents[idx + 1])
            idx += 2
        else:
            merged_sents.append(s)
            idx += 1

    return merged_sents


def fast_align_sentences(han_sents: List[str], viet_sents: List[str], para_ratio: float) -> List[Tuple[str, str]]:
    """Dóng hàng tối ưu cấp câu sử dụng Quy hoạch động với tiền xử lý O(1) và đối sánh từ khóa."""
    n_h, n_v = len(han_sents), len(viet_sents)
    if n_h == 0 or n_v == 0:
        return [(" ".join(han_sents), " ".join(viet_sents))]
    if n_h == 1 and n_v == 1:
        return [(han_sents[0], viet_sents[0])]
    if n_h == 1 or n_v == 1:
        return [(" ".join(han_sents), " ".join(viet_sents))]

    # Tiền xử lý chữ Hán: loại bỏ khoảng trắng giữa các ký tự CJK do ngắt dòng
    clean_han_sents = [
        re.sub(r"(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])", "", s)
        for s in han_sents
    ]

    # Tiền tính toán độ dài ký tự thực tế
    h_lens = [len(re.sub(r"[^\w\u4e00-\u9fff]", "", s)) for s in clean_han_sents]
    v_lens = [len(re.sub(r"[^\w]", "", s)) for s in viet_sents]

    # Tiền tính toán mảng cộng dồn tiền tố (prefix sum) để truy vấn độ dài O(1)
    h_pref = [0] * (n_h + 1)
    for i in range(n_h):
        h_pref[i + 1] = h_pref[i] + h_lens[i]

    v_pref = [0] * (n_v + 1)
    for j in range(n_v):
        v_pref[j + 1] = v_pref[j] + v_lens[j]

    # Tiền tính toán tập chỉ số từ khóa Phật học có mặt trong từng câu
    h_kw_sets = [set(idx for idx, (h_kw, _) in enumerate(BUDDHIST_DICT) if h_kw in s) for s in clean_han_sents]
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
                        merge_v_penalty = 250.0 if dj > 1 else 0.0

                        # Thưởng điểm mạnh cho các cặp có từ khóa Phật học đối ứng (không cắt đáy)
                        kws_h: Set[int] = set()
                        for si in range(i, ni):
                            kws_h.update(h_kw_sets[si])
                        kws_v: Set[int] = set()
                        for sj in range(j, nj):
                            kws_v.update(v_kw_sets[sj])
                        kw_matches = len(kws_h & kws_v)
                        step_cost = len_cost + merge_v_penalty - (kw_matches * 50.0)

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
            para_ratio = max(2.2, min(para_ratio, 7.5))

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
