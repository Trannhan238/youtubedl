import re

def sanitize_filename(title: str) -> str:
    """Làm sạch tên file"""
    return re.sub(r'[\\/*?:"<>|]', "", title)

def resource_path(relative_path: str) -> str:
    """Xác định đường dẫn tài nguyên"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)