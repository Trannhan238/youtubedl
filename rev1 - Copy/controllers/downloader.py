import yt_dlp
import threading
from utils.helpers import sanitize_filename

class YouTubeDownloader:
    def __init__(self, language_manager):
        self.language_manager = language_manager
    
    def download_video(self, url, format_type, quality, save_path):
        def download_task():
            try:
                ydl_opts = self._get_ydl_options(format_type, quality, save_path)
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    ydl.download([url])
                
                return True, None
            except Exception as e:
                return False, str(e)
        
        # Chạy trong luồng riêng để không làm treo UI
        thread = threading.Thread(target=download_task, daemon=True)
        thread.start()
        thread.join()  # Chờ luồng hoàn thành để trả kết quả
        
        return thread.is_alive() == False, None
    
    def _get_ydl_options(self, format_type, quality, save_path):
        options = {
            'outtmpl': save_path,
            'progress_hooks': [self._progress_hook],
        }
        
        if format_type == "mp3":
            options.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }],
            })
        else:
            # Video options
            if quality == "1080p":
                options['format'] = 'bestvideo[height<=1080]+bestaudio/best'
            elif quality == "720p":
                options['format'] = 'bestvideo[height<=720]+bestaudio/best'
            else:  # 480p
                options['format'] = 'bestvideo[height<=480]+bestaudio/best'
            
            options['merge_output_format'] = 'mp4'
        
        return options
    
    def _progress_hook(self, d):
        # Có thể thêm xử lý hiển thị tiến trình nếu cần
        pass