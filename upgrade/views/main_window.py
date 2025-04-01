import tkinter as tk
from tkinter import ttk, Menu, filedialog
from ..models.downloader import YouTubeDownloader
from ..models.settings import AppSettings
from ..languages.translations import Translations
from .components.url_input import UrlInput
from .components.download_options import DownloadOptions


class MainWindow:
    def __init__(self, root: tk.Tk, settings: AppSettings):
        self.root = root
        self.settings = settings
        self.translations = Translations()
        self.translations.set_language(settings.get("language", "vi"))
        self.downloader = YouTubeDownloader(settings.get("ffmpeg_path"))
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title(self.translations.get("title"))
        self.root.geometry("550x450")
        self.root.resizable(False, False)
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(self.main_frame, text=self.translations.get("title"), 
                          style='Header.TLabel')
        header.pack(pady=(0, 20))
        
        # URL Input component
        self.url_input = UrlInput(self.main_frame, self.translations)
        self.url_input.pack(fill=tk.X, pady=5)
        self.url_entry = self.url_input.url_entry  # Lấy reference từ UrlInput
        
        # Video title display
        self.video_title = tk.StringVar()
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=5)
        ttk.Label(title_frame, text=self.translations.get("video_title")).pack(side=tk.LEFT)
        ttk.Entry(title_frame, textvariable=self.video_title, state="readonly", width=40).pack()
        
        # Download Options component
        self.download_options = DownloadOptions(self.main_frame, self.translations)
        self.download_options.pack(fill=tk.X, pady=10)
        
        # Setup các thành phần khác
        self.setup_menus()
        self.setup_control_buttons()
        self.setup_status_bar()
        self.setup_context_menu()
        
        self.url_entry.focus()
    
    def setup_menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        language_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translations.get("language_menu"), menu=language_menu)
        language_menu.add_command(label="English", command=lambda: self.change_language("en"))
        language_menu.add_command(label="Tiếng Việt", command=lambda: self.change_language("vi"))
        
    def change_language(self, lang_code: str):
        self.translations.set_language(lang_code)
        self.root.title(self.translations.get("title"))
        # Cần cập nhật thêm các thành phần UI khác ở đây
    
    def setup_control_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=self.translations.get("download_button"),
                 command=self.start_download, style='Accent.TButton').grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text=self.translations.get("reset_button"),
                 command=self.reset_fields).grid(row=0, column=1, padx=5)
        
        ttk.Button(button_frame, text=self.translations.get("exit_button"),
                 command=self.root.quit).grid(row=0, column=2, padx=5)
        
        self.open_folder_btn = ttk.Button(button_frame, 
                                       text=self.translations.get("open_folder_button"),
                                       state=tk.DISABLED)
        self.open_folder_btn.grid(row=0, column=3, padx=5)
    
    def setup_status_bar(self):
        self.status_var = tk.StringVar(value=self.translations.get("ready"))
        ttk.Label(self.main_frame, textvariable=self.status_var, 
                relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, pady=(10, 0))
    
    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label=self.translations.get("paste_button"),
                                    command=self.safe_paste)
        self.url_entry.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def safe_paste(self):
        try:
            clipboard_text = self.root.clipboard_get()
            if len(clipboard_text) > 1000:
                self.status_var.set(self.translations.get("clipboard_too_large"))
                return
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard_text)
            self.validate_url()
        except tk.TclError:
            self.status_var.set(self.translations.get("clipboard_empty"))
    
    def validate_url(self):
        url = self.url_entry.get().strip()
        # Thêm logic validate URL ở đây
        pass
    
    def start_download(self):
        if not self.validate_url():
            return
            
        options = self.download_options.get_options()
        options.update({
            'ffmpeg_location': self.downloader.ffmpeg_path,
            'progress_hooks': [self.update_progress]
        })
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{options['format']}",
            filetypes=[(f"{options['format'].upper()} files", f"*.{options['format']}")]
        )
        
        if save_path:
            self.downloader.download(self.url_entry.get(), options)
    
    def update_progress(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            self.status_var.set(f"{self.translations.get('downloading')}: {percent} at {speed}")
    
    def reset_fields(self):
        self.url_entry.delete(0, tk.END)
        self.video_title.set("")
        self.download_options.reset()
        self.status_var.set(self.translations.get("ready"))