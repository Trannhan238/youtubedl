import os
import sys
import re
import customtkinter as ctk
from tkinter import messagebox, filedialog, Menu
import yt_dlp
import threading
import webbrowser

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Can be "System", "Dark", or "Light"
ctk.set_default_color_theme("blue")  # Can be "blue", "green", or "dark-blue"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ffmpeg_path = resource_path("FFmpeg/bin/ffmpeg.exe")

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.current_language = "vi"  # Default to Vietnamese
        self.languages = {
            "en": {
                "title": "Professional YouTube Downloader",
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
                "intro_text": "YouTube Downloader\nVersion 1.0\n\nA simple application to download YouTube videos in various formats and qualities.",
                "copyright_text": "Copyright © 2023\nAll rights reserved\n\nThis software is provided for personal use only.",
                "clipboard_too_large": "Clipboard content is too large (max 1000 characters)",
                "invalid_url_format": "The pasted content doesn't look like a YouTube URL"
            },
            "vi": {
                "title": "Youtube Downloader",
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
                "introduction": "Hướng dẫn",
                "copyright": "Bản quyền",
                "intro_text": "Dán link video vào ô Đường dẫn youtube\nChương trình sẽ tự động lấy phát hiện link\nKhi thấy tiêu đề video thì nhấn Tải về\nChọn định dạng phù hợp (mp4 với video, mp3 với nhạc)\nChọn chất lượng video (1080p, 720p, 480p)\n Nhấn Tải về để tải video về máy\nTải xong nhấn Mở thư mục để xem video\nChúc bạn tải video thành công",
                "copyright_text": "Bản quyền © 2025\n\nMáy tính Trần Nhân\nChuyên cung cấp, sửa chữa máy tính, Laptop, Máy in, Lắp đặt Camera, Hệ thống mạng\nĐịa chỉ: Diễn Mỹ - Diễn Châu -Nghệ AN\n\nPhần mềm chỉ dành cho mục đích sử dụng cá nhân.",
                "clipboard_too_large": "Nội dung clipboard quá lớn (tối đa 1000 ký tự)",
                "invalid_url_format": "Nội dung dán vào không giống đường dẫn YouTube"
            }
        }
        
        # Initialize UI with default language
        self.initialize_ui()
    
    def _(self, key):
        """Get translated string for current language"""
        return self.languages[self.current_language].get(key, key)
    
    def initialize_ui(self):
        """Initialize or reinitialize UI components with current language"""
        self.root.title(self._("title"))
        self.root.geometry("650x400")
        self.root.resizable(False, False)
        
        # Clear existing widgets if any
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.video_title = ctk.StringVar()
        self.download_format = ctk.StringVar(value="mp4")
        self.quality = ctk.StringVar(value="720p")
        self.bitrate = ctk.StringVar(value="128")
        self.url_valid = False
        self.auto_fetch_enabled = True
        self.last_download_path = ""
        
        self.create_widgets()
        self.setup_context_menu()
        self.setup_menus()
    
    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header = ctk.CTkLabel(main_frame, text=self._("title"), font=("Arial", 16, "bold"))
        header.pack(pady=(0, 20))
        
        # URL Entry with validation
        url_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        url_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(url_frame, text=self._("url_label")).pack(side="left", padx=(0, 10))
        
        self.url_entry = ctk.CTkEntry(url_frame, width=300)
        self.url_entry.pack(side="left", expand=True, fill="x")
        self.url_entry.bind("<FocusOut>", self.validate_and_fetch)
        self.url_entry.bind("<Return>", self.validate_and_fetch)
        
        self.paste_btn = ctk.CTkButton(url_frame, text=self._("paste_button"), 
                                     command=self.safe_paste_and_fetch, width=60)
        self.paste_btn.pack(side="left", padx=(5, 0))
        
        # URL validation indicator
        self.url_status = ctk.CTkLabel(main_frame, text="", text_color="red")
        self.url_status.pack()
        
        # Video Info
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(info_frame, text=self._("video_title")).pack(side="left", padx=(0, 10))
        title_entry = ctk.CTkEntry(info_frame, textvariable=self.video_title, state="readonly", width=300)
        title_entry.pack(side="left", expand=True, fill="x")
        
        # Format Options
        self.format_frame = ctk.CTkFrame(main_frame)
        self.format_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(self.format_frame, text=self._("download_options"), font=("Arial", 12)).pack(anchor="w", pady=(0, 10))
        
        format_row = ctk.CTkFrame(self.format_frame, fg_color="transparent")
        format_row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(format_row, text=self._("format_label")).pack(side="left", padx=(0, 10))
        self.format_options = ctk.CTkComboBox(format_row, variable=self.download_format, 
                                           values=["mp4", "mp3"], state="readonly", width=100)
        self.format_options.pack(side="left")
        self.format_options.bind("<<ComboboxSelected>>", self.update_quality_options)
        
        self.quality_frame = ctk.CTkFrame(self.format_frame, fg_color="transparent")
        self.quality_frame.pack(fill="x", pady=5)
        self.update_quality_options()
        
        # Button Frame
        self.button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)
        
        self.download_btn = ctk.CTkButton(self.button_frame, text=self._("download_button"), 
                                       command=self.download_video, fg_color="#4CAF50", hover_color="#45a049")
        self.download_btn.grid(row=0, column=0, padx=5)
        
        self.reset_btn = ctk.CTkButton(self.button_frame, text=self._("reset_button"), 
                                    command=self.reset_fields)
        self.reset_btn.grid(row=0, column=1, padx=5)
        
        self.exit_btn = ctk.CTkButton(self.button_frame, text=self._("exit_button"), 
                                    command=self.root.quit)
        self.exit_btn.grid(row=0, column=2, padx=5)
        
        # Open Folder Button
        self.open_folder_btn = ctk.CTkButton(self.button_frame, text=self._("open_folder_button"), 
                                          command=self.open_download_folder, state="disabled")
        self.open_folder_btn.grid(row=0, column=3, padx=5)
        
        self.status_var = ctk.StringVar(value=self._("ready"))
        self.status_bar = ctk.CTkLabel(main_frame, textvariable=self.status_var, 
                                     anchor="w", fg_color=("gray85", "gray25"), corner_radius=0)
        self.status_bar.pack(fill="x", pady=(10, 0), side="bottom")
        
        self.url_entry.focus()
    
    def setup_menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Language menu
        self.language_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self._("language_menu"), menu=self.language_menu)
        self.language_menu.add_command(label="English", command=lambda: self.change_language("en"))
        self.language_menu.add_command(label="Tiếng Việt", command=lambda: self.change_language("vi"))
        
        # About menu
        self.about_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self._("about_menu"), menu=self.about_menu)
        self.about_menu.add_command(label=self._("introduction"), command=self.show_introduction)
        self.about_menu.add_command(label=self._("copyright"), command=self.show_copyright)
    
    def setup_context_menu(self):
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label=self._("paste_button"), command=self.safe_paste_and_fetch)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.url_entry.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def safe_paste_and_fetch(self):
        """Safe version of paste with size and format validation"""
        try:
            # First check if clipboard contains text
            clipboard_text = self.root.clipboard_get()
            
            # Validate clipboard size (max 1000 characters)
            if len(clipboard_text) > 1000:
                self.status_var.set(self._("clipboard_too_large"))
                return
                
            # Validate basic URL format before processing
            if not any(c in clipboard_text for c in ["youtube.com", "youtu.be"]):
                self.status_var.set(self._("invalid_url_format"))
                return
                
            # Process the URL
            self.url_entry.selection_clear()
            self.url_entry.delete(0, "end")
            self.url_entry.insert("insert", clipboard_text)
            self.validate_and_fetch()
            
        except tk.TclError:
            self.status_var.set(self._("clipboard_empty"))
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def validate_and_fetch(self, event=None):
        url = self.url_entry.get().strip()
        
        # Additional validation for very long strings
        if len(url) > 1000:
            self.url_status.configure(text=self._("invalid_url"), text_color="red")
            self.url_valid = False
            self.status_var.set(self._("invalid_url_format"))
            return False
            
        # YouTube URL patterns
        patterns = [
            r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+',
            r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(https?://)?(www\.)?youtu\.be/[\w-]+'
        ]
        
        if not url:
            self.url_status.configure(text="", text_color="red")
            self.url_valid = False
            return False
        
        for pattern in patterns:
            if re.match(pattern, url):
                self.url_status.configure(text=self._("valid_url"), text_color="green")
                self.url_valid = True
                if self.auto_fetch_enabled:
                    self.fetch_video_info()
                return True
        
        self.url_status.configure(text=self._("invalid_url"), text_color="red")
        self.url_valid = False
        return False
    
    def cut_text(self):
        self.url_entry.event_generate("<<Cut>>")
    
    def copy_text(self):
        self.url_entry.event_generate("<<Copy>>")
    
    def update_quality_options(self, event=None):
        for widget in self.quality_frame.winfo_children():
            widget.destroy()
        
        format_type = self.download_format.get()
        
        if format_type == "mp4":
            ctk.CTkLabel(self.quality_frame, text=self._("quality_label")).pack(side="left", padx=(0, 10))
            quality_options = ctk.CTkComboBox(self.quality_frame, variable=self.quality, 
                                           values=["1080p", "720p", "480p"], state="readonly", width=100)
            quality_options.pack(side="left")
            self.quality.set("720p")
        else:
            ctk.CTkLabel(self.quality_frame, text=self._("bitrate_label")).pack(side="left", padx=(0, 10))
            bitrate_options = ctk.CTkComboBox(self.quality_frame, variable=self.bitrate, 
                                           values=["64", "96", "128", "160", "192", "256", "320"], 
                                           state="readonly", width=100)
            bitrate_options.pack(side="left")
            self.bitrate.set("128")
    
    def fetch_video_info(self):
        if not self.url_valid:
            self.status_var.set(self._("invalid_url_msg"))
            return
        
        link = self.url_entry.get()
        self.status_var.set(self._("fetching"))
        self.root.update()
        
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=False)
                clean_title = re.sub(r'[\\/*?:"<>|]', "", info_dict.get('title', 'video'))
                self.video_title.set(clean_title)
                self.status_var.set(self._("fetch_success"))
        except Exception as e:
            self.status_var.set(f"{self._('fetch_error')}: {str(e)}")
            self.url_status.configure(text=self._("invalid_url"), text_color="red")
            self.url_valid = False
    
    def get_safe_filename(self):
        title = self.video_title.get()
        if not title or title == "No title available":
            return "youtube_video"
        
        safe_name = re.sub(r'[\\/*?:"<>|]', "", title)
        return safe_name.strip()
    
    def download_video(self):
        if not self.url_valid:
            self.status_var.set(self._("invalid_url_msg"))
            return
        
        def download_task():
            link = self.url_entry.get()

            try:
                ext = self.download_format.get()
                default_filename = f"{self.get_safe_filename()}.{ext}"
                
                save_path = filedialog.asksaveasfilename(
                    title=self._("save_location"),
                    initialfile=default_filename,
                    defaultextension=f".{ext}",
                    filetypes=[(f"{ext.upper()} files", f"*.{ext}")],
                )
                
                if not save_path:
                    return

                self.last_download_path = os.path.dirname(save_path)
                ydl_opts = {
                    'outtmpl': save_path,
                    'ffmpeg_location': ffmpeg_path,
                    'progress_hooks': [self.progress_hook],
                }

                if self.download_format.get() == "mp3":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': self.bitrate.get(),
                        }],
                    })
                else:
                    quality = self.quality.get()
                    if quality == "1080p":
                        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                    elif quality == "720p":
                        ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                    elif quality == "480p":
                        ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
                    
                    ydl_opts['merge_output_format'] = 'mp4'

                self.status_var.set(self._("downloading"))
                self.open_folder_btn.configure(state="disabled")
                self.root.update()
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                messagebox.showinfo(self._("success_title"), f"Download completed!\nSaved to: {save_path}")
                self.status_var.set(self._("download_complete"))
                self.open_folder_btn.configure(state="normal")
            except Exception as e:
                self.status_var.set(f"{self._('download_failed')}: {str(e)}")
                self.open_folder_btn.configure(state="disabled")

        threading.Thread(target=download_task, daemon=True).start()
    
    def open_download_folder(self):
        if self.last_download_path and os.path.isdir(self.last_download_path):
            try:
                webbrowser.open(self.last_download_path)
            except Exception as e:
                self.status_var.set(f"Cannot open folder: {e}")
        else:
            self.status_var.set(self._("no_folder"))
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            self.status_var.set(f"{self._('downloading')}: {percent} at {speed}")
            self.root.update()
    
    def reset_fields(self):
        self.url_entry.delete(0, "end")
        self.video_title.set("")
        self.download_format.set("mp4")
        self.quality.set("720p")
        self.bitrate.set("128")
        self.status_var.set(self._("ready"))
        self.url_status.configure(text="")
        self.url_valid = False
        self.open_folder_btn.configure(state="disabled")
    
    def change_language(self, lang_code):
        """Change application language and refresh UI"""
        self.current_language = lang_code
        # Rebuild the UI with new language
        self.initialize_ui()
    
    def show_introduction(self):
        messagebox.showinfo(self._("introduction"), self._("intro_text"))
    
    def show_copyright(self):
        messagebox.showinfo(self._("copyright"), self._("copyright_text"))

if __name__ == "__main__":
    root = ctk.CTk()
    app = YouTubeDownloader(root)
    root.mainloop()