import re
import pandas as pd
import os

def anchor_alignment(input_txt, output_excel):
    print(f"Đang xử lý {input_txt}...")
    with open(input_txt, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex tìm tất cả các khối text bắt đầu bằng mã [xxxxxxx]
    pattern = r'(\[\d{4}[a-z]\d{2}\])(.*?)(?=\[\d{4}[a-z]\d{2}\]|$)'
    matches = re.findall(pattern, content, re.DOTALL)

    # Gom nhóm các đoạn text theo mã số
    blocks_by_id = {}
    for tag, text in matches:
        text = text.strip()
        if tag not in blocks_by_id:
            blocks_by_id[tag] = []
        blocks_by_id[tag].append(text)

    aligned_data = []
    for tag, blocks in blocks_by_id.items():
        han_text = ""
        viet_text = ""
        
        # Xử lý linh hoạt dựa trên số lượng đoạn bắt được của mỗi mã
        if len(blocks) >= 3:
            han_text = blocks[0]   # Hán
            viet_text = blocks[-1] # Dịch nghĩa (Bỏ phần Âm ở giữa)
        elif len(blocks) == 2:
            han_text = blocks[0]
            viet_text = blocks[1]  # Có thể Âm Hán Việt bị thiếu trong file gốc
        elif len(blocks) == 1:
            han_text = blocks[0]
            viet_text = ""         # Để trống cột Việt cho người dùng tự kéo thả
            print(f"Lưu ý: Mã {tag} bị khuyết bản dịch/phiên âm trong file gốc.")

        # Xóa các dấu xuống dòng bên trong đoạn để text nằm gọn trong 1 ô Excel
        han_text = han_text.replace('\n', ' ')
        viet_text = viet_text.replace('\n', ' ')
        
        aligned_data.append({
            "Mã đoạn": tag,
            "Hán": han_text,
            "Việt": viet_text
        })

    # Xuất ra file Excel
    df = pd.DataFrame(aligned_data)
    os.makedirs(os.path.dirname(output_excel), exist_ok=True)
    df.to_excel(output_excel, index=False)
    print(f"-> Đã ghép sơ bộ {len(df)} cặp đoạn và lưu tại {output_excel}\n")

# THỰC THI
if __name__ == "__main__":
    anchor_alignment("03_text_sach/q4_cleaned.txt", "04_dong_hang/q4_ghep_so_bo.xlsx")
    anchor_alignment("03_text_sach/q7_cleaned.txt", "04_dong_hang/q7_ghep_so_bo.xlsx")