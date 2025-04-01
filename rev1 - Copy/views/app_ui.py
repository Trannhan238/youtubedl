import tkinter as tk
from tkinter import ttk, Menu, messagebox
from controllers.downloader import YouTubeDownloader
from utils.language import LanguageManager
import webbrowser
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.language_manager = LanguageManager()
        self.downloader = YouTubeDownloader(self.language_manager)
        self.last_download_path = ""
        self.setup_ui()
        
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
            self.url_entry.insert(0, self.root.clipboard_get())
        except tk.TclError:
            self.status_var.set(self._("clipboard_empty"))
    
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
        
        # Lấy đường dẫn lưu file
        ext = self.format_var.get()
        save_path = filedialog.asksaveasfilename(
            title=self._("save_location"),
            defaultextension=f".{ext}",
            filetypes=[(f"{ext.upper()} files", f"*.{ext}")]
        )
        
        if not save_path:
            return
            
        self.last_download_path = os.path.dirname(save_path)
        self.status_var.set(self._("downloading"))
        self.open_folder_btn.config(state=tk.DISABLED)
        
        # Gọi controller để xử lý tải video
        success, error = self.downloader.download_video(
            url=url,
            format_type=self.format_var.get(),
            quality=self.quality_var.get(),
            save_path=save_path
        )
        
        if success:
            self.status_var.set(self._("download_complete"))
            self.open_folder_btn.config(state=tk.NORMAL)
            messagebox.showinfo(self._("success_title"), self._("download_complete"))
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