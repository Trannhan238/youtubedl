import tkinter as tk
from tkinter import ttk, Menu, messagebox, filedialog
from controllers.downloader import YouTubeDownloader
from utils.language import LanguageManager
from utils.helpers import sanitize_filename
import webbrowser
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.language_manager = LanguageManager()
        self.downloader = YouTubeDownloader(self.language_manager)
        self.last_download_path = ""
        self.setup_ui()

        # Liên kết Ctrl + V với phương thức paste_url
        self.root.bind("<Control-v>", lambda event: self.paste_url())
        
    def setup_ui(self):
        self.root.title(self._("title"))
        self.root.geometry("550x450")
        self.root.resizable(False, False)
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(self.main_frame, text=self._("title"), style='Header.TLabel').pack(pady=(0, 20))
        
        # URL Section
        self.create_url_section()
        
        # Video Info
        self.video_title = tk.StringVar()
        ttk.Label(self.main_frame, text=self._("video_title")).pack(anchor=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.video_title, state="readonly", width=60).pack(fill=tk.X, pady=5)
        
        # Format Options
        self.create_format_options()
        
        # Buttons
        self.create_buttons()
        
        # Status Bar
        self.status_var = tk.StringVar(value=self._("ready"))
        ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, pady=(10, 0))
        
        # Menus
        self.setup_menus()
        
        # Style
        self.setup_styles()
    
    def create_url_section(self):
        url_frame = ttk.Frame(self.main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text=self._("url_label")).pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        ttk.Button(url_frame, text=self._("paste_button"), command=self.paste_url, width=8).pack(side=tk.LEFT)
    
    def create_format_options(self):
        frame = ttk.LabelFrame(self.main_frame, text=self._("download_options"), padding=10)
        frame.pack(fill=tk.X, pady=10)
        
        # Format selection
        self.format_var = tk.StringVar(value="mp4")
        ttk.Label(frame, text=self._("format_label")).grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(frame, textvariable=self.format_var, values=["mp4", "mp3"], state="readonly", width=8).grid(row=0, column=1, sticky=tk.W)
        
        # Quality selection
        self.quality_var = tk.StringVar(value="720p")
        ttk.Label(frame, text=self._("quality_label")).grid(row=1, column=0, sticky=tk.W)
        self.quality_combo = ttk.Combobox(frame, textvariable=self.quality_var, state="readonly", width=8)
        self.quality_combo.grid(row=1, column=1, sticky=tk.W)
        self.update_quality_options()
        
        self.format_var.trace_add("write", lambda *args: self.update_quality_options())
    
    def create_buttons(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(pady=10)
        
        ttk.Button(frame, text=self._("download_button"), command=self.start_download).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text=self._("reset_button"), command=self.reset_fields).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text=self._("exit_button"), command=self.root.quit).grid(row=0, column=2, padx=5)
        self.open_folder_btn = ttk.Button(frame, text=self._("open_folder_button"), command=self.open_download_folder, state=tk.DISABLED)
        self.open_folder_btn.grid(row=0, column=3, padx=5)
    
    def setup_menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Language menu
        lang_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self._("language_menu"), menu=lang_menu)
        lang_menu.add_command(label="English", command=lambda: self.change_language("en"))
        lang_menu.add_command(label="Tiếng Việt", command=lambda: self.change_language("vi"))
        
        # About menu
        about_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self._("about_menu"), menu=about_menu)
        about_menu.add_command(label=self._("introduction"), command=self.show_intro)
        about_menu.add_command(label=self._("copyright"), command=self.show_copyright)
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Accent.TButton', foreground='white', background='#4CAF50')
    
    def _(self, key):
        return self.language_manager.get_text(key)
    
    def paste_url(self):
        try:
            self.url_entry.delete(0, tk.END)
            url = self.root.clipboard_get()  # Lấy nội dung từ clipboard
            self.url_entry.insert(0, url)  # Chèn URL vào ô nhập liệu
            self.fetch_video_info(url)  # Gọi phương thức lấy thông tin video
        except tk.TclError:
            self.status_var.set(self._("clipboard_empty"))  # Hiển thị lỗi nếu clipboard trống
    
    def update_quality_options(self):
        if self.format_var.get() == "mp4":
            self.quality_combo['values'] = ["1080p", "720p", "480p"]
            self.quality_var.set("720p")
        else:
            self.quality_combo['values'] = ["320", "256", "192", "160", "128", "96", "64"]
            self.quality_var.set("128")
    
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status_var.set(self._("invalid_url_msg"))
            return

        # Lấy thông tin video để lấy tiêu đề
        try:
            video_info = self.downloader.get_video_info(url)
            video_title = sanitize_filename(video_info.get("title", "youtube_video"))
        except Exception as e:
            self.status_var.set(f"{self._('fetch_error')}: {str(e)}")
            return

        # Hiển thị hộp thoại để chọn nơi lưu file
        save_path = filedialog.asksaveasfilename(
            initialfile=f"{video_title}.mp4" if self.format_var.get() == "mp4" else f"{video_title}.mp3",
            defaultextension=".mp4" if self.format_var.get() == "mp4" else ".mp3",
            filetypes=[("MP4 files", "*.mp4"), ("MP3 files", "*.mp3")],
            title=self._("save_location")
        )

        if not save_path:  # Nếu người dùng hủy hộp thoại
            self.status_var.set(self._("no_folder"))
            return

        # Gọi lớp YouTubeDownloader để tải video
        success, error = self.downloader.download_video(
            url=url,
            format_type=self.format_var.get(),
            quality=self.quality_var.get(),
            save_path=save_path
        )

        if success:
            self.status_var.set(self._("download_complete"))
            self.last_download_path = os.path.dirname(save_path)  # Lưu thư mục cuối cùng
            self.open_folder_btn.config(state=tk.NORMAL)  # Kích hoạt nút "Mở thư mục"
        else:
            self.status_var.set(f"{self._('download_failed')}: {error}")
    
    def open_download_folder(self):
        if self.last_download_path and os.path.isdir(self.last_download_path):
            webbrowser.open(self.last_download_path)
    
    def reset_fields(self):
        self.url_entry.delete(0, tk.END)
        self.video_title.set("")
        self.format_var.set("mp4")
        self.quality_var.set("720p")
        self.status_var.set(self._("ready"))
        self.open_folder_btn.config(state=tk.DISABLED)
    
    def show_intro(self):
        """Hiển thị thông tin giới thiệu về ứng dụng"""
        messagebox.showinfo(
            self._("introduction"),
            self._("intro_text")
        )
    
    def show_copyright(self):
        """Hiển thị thông tin bản quyền"""
        messagebox.showinfo(
            self._("copyright"),
            self._("copyright_text")
        )

    def fetch_video_info(self, url):
        """Lấy thông tin video từ URL và hiển thị tiêu đề"""
        try:
            self.status_var.set(self._("fetching"))  # Hiển thị trạng thái "Đang lấy thông tin video..."
            info = self.downloader.get_video_info(url)  # Gọi phương thức lấy thông tin video từ YouTubeDownloader
            self.video_title.set(info.get("title", self._("fetch_error")))  # Hiển thị tiêu đề video
            self.status_var.set(self._("fetch_success"))  # Hiển thị trạng thái "Lấy thông tin thành công"
        except Exception as e:
            self.video_title.set("")
            self.status_var.set(f"{self._('fetch_error')}: {str(e)}")  # Hiển thị lỗi