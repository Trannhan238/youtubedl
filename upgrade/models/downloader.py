import yt_dlp
import threading
from typing import Dict, Callable

class YouTubeDownloader:
    def __init__(self, ffmpeg_path: str):
        self.ffmpeg_path = ffmpeg_path
        
    def download(self, url: str, options: Dict, progress_hook: Callable = None) -> None:
        """Xử lý tải video với các tùy chọn"""
        if progress_hook:
            options['progress_hooks'] = [progress_hook]
            
        def download_task():
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
                
        threading.Thread(target=download_task, daemon=True).start()
    
    def get_video_info(self, url: str) -> Dict:
        """Lấy thông tin video từ URL"""
        ydl_opts = {'quiet': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            raise Exception(f"Failed to fetch video info: {str(e)}")