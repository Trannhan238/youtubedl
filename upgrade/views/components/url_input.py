import tkinter as tk
from tkinter import ttk

class UrlInput(ttk.Frame):
    def __init__(self, parent, translations):
        super().__init__(parent)
        self.translations = translations
        self.url_entry = None  # Khởi tạo thuộc tính
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện nhập URL"""
        ttk.Label(self, text=self.translations.get("url_label")).pack(side=tk.LEFT, padx=(0, 10))
        
        # Tạo entry widget và lưu reference
        self.url_entry = ttk.Entry(self, width=30)
        self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Nút Paste
        self.paste_btn = ttk.Button(self, text=self.translations.get("paste_button"), 
                                  width=6, command=self.safe_paste)
        self.paste_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Hiển thị trạng thái URL
        self.url_status = ttk.Label(self, text="", foreground="red")
        self.url_status.pack()
    
    def safe_paste(self):
        """Dán nội dung từ clipboard một cách an toàn"""
        try:
            clipboard_text = self.master.clipboard_get()
            if len(clipboard_text) > 1000:
                self.url_status.config(text=self.translations.get("clipboard_too_large"))
                return
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard_text)
        except tk.TclError:
            self.url_status.config(text=self.translations.get("clipboard_empty"))
    
    def get_url(self):
        """Lấy URL đã nhập"""
        return self.url_entry.get().strip()