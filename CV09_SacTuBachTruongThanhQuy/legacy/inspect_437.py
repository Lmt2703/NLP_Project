import json
import re

with open('CV09_SacTuBachTruongThanhQuy/03_text_sach/trieu_chau/trieu_chau_viet_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('CV09_SacTuBachTruongThanhQuy/03_text_sach/trieu_chau/trieu_chau_han_q14.txt', 'r', encoding='utf-8') as f:
    zh = f.read()

colophon = '廬山棲賢寶覺禪院住持傳法賜紫沙門'
if colophon in zh:
    zh = zh[:zh.find(colophon)].strip()

matched_items = [it for it in items if it['id'] == 209 or 225 <= it['id'] <= 525]

# Let's inspect Tắc 437 to 442 in VI
for it in matched_items:
    if 437 <= it['id'] <= 442:
        print(f"=== MỤC {it['id']} ===")
        print(it['text'])
