import json
import re

with open('CV09_SacTuBachTruongThanhQuy/03_text_sach/trieu_chau/trieu_chau_viet_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('CV09_SacTuBachTruongThanhQuy/03_text_sach/trieu_chau/trieu_chau_han_q14.txt', 'r', encoding='utf-8') as f:
    zh = f.read()

colophon = '廬山棲賢寶覺禪院住持傳法賜紫沙門'
if colophon in zh:
    zh = zh[:zh.find(colophon)].strip()

# Let's inspect Tắc 440 to 455 in Vietnamese to see their topics
for it in items:
    if 440 <= it['id'] <= 455:
        first_line = it['text'].strip().splitlines()[0][:70]
        print(f"Mục {it['id']}: {first_line}")
