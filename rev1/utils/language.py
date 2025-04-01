class LanguageManager:
    def __init__(self):
        self.current_language = "vi"
        self.languages = {
            "en": {
                "title": "YouTube Downloader",
                "url_label": "YouTube URL:",
                "paste_button": "Paste",
                "video_title": "Video Title:",
                "download_options": "Download Options",
                "format_label": "Format:",
                "quality_label": "Quality:",
                "bitrate_label": "Bitrate (kbps):",
                "download_button": "Download",
                "reset_button": "Reset",
                "exit_button": "Exit",
                "open_folder_button": "Open Folder",
                "valid_url": "✓ Valid YouTube URL",
                "invalid_url": "✗ Invalid YouTube URL",
                "fetching": "Fetching video info...",
                "fetch_success": "Video info fetched successfully",
                "fetch_error": "Error fetching video info",
                "downloading": "Downloading...",
                "download_complete": "Download completed",
                "download_failed": "Download failed",
                "ready": "Ready",
                "error_title": "Error",
                "invalid_url_msg": "Please enter a valid YouTube URL",
                "no_folder": "No download folder available",
                "success_title": "Success",
                "save_location": "Choose save location",
                "language_menu": "Language",
                "clipboard_empty": "Clipboard is empty or contains no text",
                "about_menu": "About",
                "introduction": "Introduction",
                "copyright": "Copyright",
                "intro_text": "YouTube Downloader\nVersion 1.0\n\nA simple application to download YouTube videos.",
                "copyright_text": "Copyright © 2023\nAll rights reserved."
            },
            "vi": {
                "title": "Trình tải video YouTube",
                "url_label": "Đường dẫn YouTube:",
                "paste_button": "Dán",
                "video_title": "Tiêu đề video:",
                "download_options": "Tùy chọn tải về",
                "format_label": "Định dạng:",
                "quality_label": "Chất lượng:",
                "bitrate_label": "Bitrate (kbps):",
                "download_button": "Tải về",
                "reset_button": "Đặt lại",
                "exit_button": "Thoát",
                "open_folder_button": "Mở thư mục",
                "valid_url": "✓ Đường dẫn hợp lệ",
                "invalid_url": "✗ Đường dẫn không hợp lệ",
                "fetching": "Đang lấy thông tin video...",
                "fetch_success": "Lấy thông tin thành công",
                "fetch_error": "Lỗi khi lấy thông tin",
                "downloading": "Đang tải xuống...",
                "download_complete": "Tải về hoàn tất",
                "download_failed": "Tải về thất bại",
                "ready": "Sẵn sàng",
                "error_title": "Lỗi",
                "invalid_url_msg": "Vui lòng nhập đường dẫn YouTube hợp lệ",
                "no_folder": "Không có thư mục tải về",
                "success_title": "Thành công",
                "save_location": "Chọn nơi lưu",
                "language_menu": "Ngôn ngữ",
                "clipboard_empty": "Clipboard trống hoặc không có văn bản",
                "about_menu": "Giới thiệu",
                "introduction": "Giới thiệu",
                "copyright": "Bản quyền",
                "intro_text": "Trình tải video YouTube\nPhiên bản 1.0\n\nỨng dụng đơn giản để tải video YouTube.",
                "copyright_text": "Bản quyền © 2023\nĐã đăng ký."
            }
        }
    
    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.current_language = lang_code
    
    def get_text(self, key):
        return self.languages[self.current_language].get(key, key)