import json
import os
from typing import Dict, Optional

class AppSettings:
    def __init__(self, config_file: str = "settings.json"):
        self.config_file = config_file
        self.settings = {
            "language": "vi",
            "last_download_dir": os.path.expanduser("~"),
            "ffmpeg_path": "FFmpeg/bin/ffmpeg.exe"
        }
        self.load_settings()
    
    def load_settings(self) -> None:
        """Tải cài đặt từ file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.settings.update(json.load(f))
            except Exception:
                pass
    
    def save_settings(self) -> None:
        """Lưu cài đặt vào file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key: str, default=None) -> Optional[Dict]:
        """Lấy giá trị cài đặt"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value) -> None:
        """Thiết lập giá trị cài đặt"""
        self.settings[key] = value
        self.save_settings()