import re
import os

def sanitize_filename(title):
    """Làm sạch tên file từ tiêu đề video"""
    if not title:
        return "youtube_video"
    
    # Xóa các ký tự không hợp lệ trong tên file
    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
    return clean_title.strip()

def resource_path(relative_path):
    """Lấy đường dẫn đúng cả khi chạy từ file đóng gói"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)