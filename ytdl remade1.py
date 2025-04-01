import os
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import threading
from tkinter import Menu
import webbrowser

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
                "intro_text": "Trình tải video YouTube\nPhiên bản 1.0\n\nỨng dụng đơn giản để tải video YouTube với nhiều định dạng và chất lượng khác nhau.",
                "copyright_text": "Bản quyền © 2023\nĐã đăng ký\n\nPhần mềm chỉ dành cho mục đích sử dụng cá nhân.",
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
        self.root.geometry("550x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Clear existing widgets if any
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Error.TEntry', foreground='red')
        
        self.video_title = tk.StringVar()
        self.download_format = tk.StringVar(value="mp4")
        self.quality = tk.StringVar(value="720p")
        self.bitrate = tk.StringVar(value="128")
        self.url_valid = False
        self.auto_fetch_enabled = True
        self.last_download_path = ""
        
        self.create_widgets()
        self.setup_context_menu()
        self.setup_menus()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header = ttk.Label(main_frame, text=self._("title"), style='Header.TLabel')
        header.pack(pady=(0, 20))
        
        # URL Entry with validation
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text=self._("url_label")).pack(side=tk.LEFT, padx=(0, 10))
        
        self.url_entry = ttk.Entry(url_frame, width=30)
        self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.url_entry.bind("<FocusOut>", self.validate_and_fetch)
        self.url_entry.bind("<Return>", self.validate_and_fetch)
        
        self.paste_btn = ttk.Button(url_frame, text=self._("paste_button"), 
                                  command=self.safe_paste_and_fetch, width=6)
        self.paste_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # URL validation indicator
        self.url_status = ttk.Label(main_frame, text="", foreground="red")
        self.url_status.pack()
        
        # Video Info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text=self._("video_title")).pack(side=tk.LEFT, padx=(0, 10))
        title_entry = ttk.Entry(info_frame, textvariable=self.video_title, state="readonly", width=40)
        title_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Format Options
        self.format_frame = ttk.LabelFrame(main_frame, text=self._("download_options"), padding=10)
        self.format_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.format_frame, text=self._("format_label")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.format_options = ttk.Combobox(self.format_frame, textvariable=self.download_format, 
                                        values=["mp4", "mp3"], state="readonly", width=10)
        self.format_options.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.format_options.bind("<<ComboboxSelected>>", self.update_quality_options)
        
        self.quality_frame = ttk.Frame(self.format_frame)
        self.quality_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.update_quality_options()
        
        # Button Frame
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(pady=20)
        
        self.download_btn = ttk.Button(self.button_frame, text=self._("download_button"), 
                                     command=self.download_video, style='Accent.TButton')
        self.download_btn.grid(row=0, column=0, padx=5)
        
        self.reset_btn = ttk.Button(self.button_frame, text=self._("reset_button"), 
                                  command=self.reset_fields)
        self.reset_btn.grid(row=0, column=1, padx=5)
        
        self.exit_btn = ttk.Button(self.button_frame, text=self._("exit_button"), 
                                 command=self.root.quit)
        self.exit_btn.grid(row=0, column=2, padx=5)
        
        # Open Folder Button
        self.open_folder_btn = ttk.Button(self.button_frame, text=self._("open_folder_button"), 
                                        command=self.open_download_folder, state=tk.DISABLED)
        self.open_folder_btn.grid(row=0, column=3, padx=5)
        
        self.status_var = tk.StringVar(value=self._("ready"))
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.style.configure('Accent.TButton', foreground='white', background='#4CAF50')
        self.style.map('Accent.TButton', 
                      background=[('active', '#45a049'), ('pressed', '#39843f')])
        
        self.url_entry.focus()
    
    def setup_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Language menu
        self.language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self._("language_menu"), menu=self.language_menu)
        self.language_menu.add_command(label="English", command=lambda: self.change_language("en"))
        self.language_menu.add_command(label="Tiếng Việt", command=lambda: self.change_language("vi"))
        
        # About menu
        self.about_menu = tk.Menu(menubar, tearoff=0)
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
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(tk.INSERT, clipboard_text)
            self.validate_and_fetch()
            
        except tk.TclError:
            self.status_var.set(self._("clipboard_empty"))
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def validate_and_fetch(self, event=None):
        url = self.url_entry.get().strip()
        
        # Additional validation for very long strings
        if len(url) > 1000:
            self.url_status.config(text=self._("invalid_url"), foreground="red")
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
            self.url_status.config(text="", foreground="red")
            self.url_valid = False
            return False
        
        for pattern in patterns:
            if re.match(pattern, url):
                self.url_status.config(text=self._("valid_url"), foreground="green")
                self.url_valid = True
                if self.auto_fetch_enabled:
                    self.fetch_video_info()
                return True
        
        self.url_status.config(text=self._("invalid_url"), foreground="red")
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
            ttk.Label(self.quality_frame, text=self._("quality_label")).pack(side=tk.LEFT, padx=(0, 10))
            quality_options = ttk.Combobox(self.quality_frame, textvariable=self.quality, 
                                         values=["1080p", "720p", "480p"], state="readonly", width=10)
            quality_options.pack(side=tk.LEFT)
            self.quality.set("720p")
        else:
            ttk.Label(self.quality_frame, text=self._("bitrate_label")).pack(side=tk.LEFT, padx=(0, 10))
            bitrate_options = ttk.Combobox(self.quality_frame, textvariable=self.bitrate, 
                                         values=["64", "96", "128", "160", "192", "256", "320"], 
                                         state="readonly", width=10)
            bitrate_options.pack(side=tk.LEFT)
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
            self.url_status.config(text=self._("invalid_url"), foreground="red")
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
                self.open_folder_btn.config(state=tk.DISABLED)
                self.root.update()
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                messagebox.showinfo(self._("success_title"), f"Download completed!\nSaved to: {save_path}")
                self.status_var.set(self._("download_complete"))
                self.open_folder_btn.config(state=tk.NORMAL)
            except Exception as e:
                self.status_var.set(f"{self._('download_failed')}: {str(e)}")
                self.open_folder_btn.config(state=tk.DISABLED)

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
        self.url_entry.delete(0, tk.END)
        self.video_title.set("")
        self.download_format.set("mp4")
        self.quality.set("720p")
        self.bitrate.set("128")
        self.status_var.set(self._("ready"))
        self.url_status.config(text="")
        self.url_valid = False
        self.open_folder_btn.config(state=tk.DISABLED)
    
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
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()