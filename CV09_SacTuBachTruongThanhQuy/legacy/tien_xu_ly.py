import fitz  # PyMuPDF
import re
import os

# 1. TỪ ĐIỂN CHUYỂN MÃ VNI SANG UNICODE
# (Bao gồm các tổ hợp VNI Windows thường gặp trong file)
vni_to_unicode = {
    'aù': 'á', 'aø': 'à', 'aû': 'ả', 'aõ': 'ã', 'aï': 'ạ',
    'aâ': 'â', 'aá': 'ấ', 'aà': 'ầ', 'aå': 'ẩ', 'aö': 'ẫ', 'aä': 'ậ',
    'aê': 'ă', 'aé': 'ắ', 'aè': 'ằ', 'aë': 'ẳ', 'aö': 'ẵ', 'aë': 'ặ', # Lưu ý: VNI dùng aê cho ă
    'eù': 'é', 'eø': 'è', 'eû': 'ẻ', 'eõ': 'ẽ', 'eï': 'ẹ',
    'eâ': 'ê', 'eá': 'ế', 'eà': 'ề', 'eå': 'ể', 'eö': 'ễ', 'eä': 'ệ',
    'í': 'í', 'ì': 'ì', 'æ': 'ỉ', 'ó': 'ĩ', 'ò': 'ị', # Một số ký tự i VNI
    'où': 'ó', 'oø': 'ò', 'oû': 'ỏ', 'oõ': 'õ', 'oï': 'ọ',
    'oâ': 'ô', 'oá': 'ố', 'oà': 'ồ', 'oå': 'ổ', 'oö': 'ỗ', 'oä': 'ộ',
    'ô': 'ơ', 'ôù': 'ớ', 'ôø': 'ờ', 'ôû': 'ở', 'ôõ': 'ỡ', 'ôï': 'ợ',
    'uù': 'ú', 'uø': 'ù', 'uû': 'ủ', 'uõ': 'ũ', 'uï': 'ụ',
    'ö': 'ư', 'öù': 'ứ', 'öø': 'ừ', 'öû': 'ử', 'öõ': 'ữ', 'öï': 'ự',
    'yù': 'ý', 'yø': 'ỳ', 'yû': 'ỷ', 'yõ': 'ỹ', 'yï': 'ỵ',
    'ñ': 'đ', 'Ñ': 'Đ',
    # Phiên bản in hoa
    'AÙ': 'Á', 'AØ': 'À', 'AÛ': 'Ả', 'AÕ': 'Ã', 'AÏ': 'Ạ',
    'AÂ': 'Â', 'AÁ': 'Ấ', 'AÀ': 'Ầ', 'AÅ': 'Ẩ', 'AÖ': 'Ẫ', 'AÄ': 'Ậ',
    'EÙ': 'É', 'EØ': 'È', 'EÛ': 'Ẻ', 'EÕ': 'Ẽ', 'EÏ': 'Ẹ',
    'EÂ': 'Ê', 'EÁ': 'Ế', 'EÀ': 'Ề', 'EÅ': 'Ể', 'EÖ': 'Ễ', 'EÄ': 'Ệ',
    'OÙ': 'Ó', 'OØ': 'Ò', 'OÛ': 'Ỏ', 'OÕ': 'Õ', 'OÏ': 'Ọ',
    'OÂ': 'Ô', 'OÁ': 'Ố', 'OÀ': 'Ồ', 'OÅ': 'Ổ', 'OÖ': 'Ỗ', 'OÄ': 'Ộ',
    'OÂ': 'Ơ', 'ÔÙ': 'Ớ', 'ÔØ': 'Ờ', 'ÔÛ': 'Ở', 'ÔÕ': 'Ỡ', 'ÔÏ': 'Ợ',
    'UÙ': 'Ú', 'UØ': 'Ù', 'UÛ': 'Ủ', 'UÕ': 'Ũ', 'UÏ': 'Ụ',
    'Ö': 'Ư', 'ÖÙ': 'Ứ', 'ÖØ': 'Ừ', 'ÖÛ': 'Ử', 'ÖÕ': 'Ữ', 'ÖÏ': 'Ự',
}

def convert_vni_to_unicode(text):
    """Thay thế chuỗi VNI bằng Unicode dựa trên Dictionary."""
    # Sắp xếp key theo độ dài giảm dần để replace chuỗi dài trước (tránh lỗi đè chuỗi ngắn)
    for vni, uni in sorted(vni_to_unicode.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(vni, uni)
    return text

def clean_noise(text):
    """Xóa bỏ header, footer, số trang và các đoạn Lời bàn."""
    # 1. Xóa số trang (Các dòng chỉ chứa con số)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # 2. Xóa Header lặp lại (bao gồm cả bản VNI chưa chuyển mã nếu có sót)
    headers_to_remove = [
        r'SẮC TU BÁCH TRƯỢNG THANH QUI.*',
        r'Saéc tu Baùch Tröôïng thanh qui.*',
        r'Quyển thứ \d+',
        r'Quyển \d+',
        r'Quyeån \d+',
        r'卷第.*', # Quyển chữ Hán
        r'勅修百丈清規卷第.*'
    ]
    for header in headers_to_remove:
        text = re.sub(header, '', text, flags=re.IGNORECASE)
    
    # 3. Xóa các đoạn "LỜI BÀN" (bắt đầu bằng LỜI BÀN, kết thúc bằng các dấu ***)
    # Lời bàn trong sách gốc thường được kẹp giữa chữ LỜI BÀN (hoặc LÔØI BAØN) và cụm * * *
    text = re.sub(r'LỜI BÀN.*?(?=\[11\d{2}[a-z]\d{2}\]|$|\* \*)', '', text, flags=re.DOTALL)
    text = re.sub(r'\*\s*\*\s*\*|\*\s*\*', '', text) # Xóa nốt các dấu sao phân cách
    
    # 4. Xóa khoảng trắng thừa và dòng trống
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def process_pdf(pdf_path, output_path):
    """Đọc PDF, xử lý và lưu ra file txt."""
    print(f"Đang xử lý: {pdf_path}...")
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        
        # Chuyển mã VNI trước để dễ dàng dọn rác bằng regex Unicode
        text_unicode = convert_vni_to_unicode(text)
        full_text += text_unicode + "\n"
        
    # Dọn dẹp rác (Header, số trang, Lời bàn)
    cleaned_text = clean_noise(full_text)
    
    # Lưu file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    
    print(f"Đã lưu thành công: {output_path}")

# THỰC THI
if __name__ == "__main__":
    # Thay đổi đường dẫn cho phù hợp với cấu trúc thư mục của bạn
    pdf_files = [
        ("01_nguon/SacTuBachTruongThanhQuy-q4.pdf", "03_text_sach/q4_cleaned.txt"),
        ("01_nguon/SacTuBachTruongThanhQuy-q7.pdf", "03_text_sach/q7_cleaned.txt")
    ]
    
    for pdf_in, txt_out in pdf_files:
        if os.path.exists(pdf_in):
            process_pdf(pdf_in, txt_out)
        else:
            print(f"Không tìm thấy file: {pdf_in}")