import tkinter as tk
from tkinter import ttk

class UrlInput(ttk.Frame):
    def __init__(self, parent, translations):
        super().__init__(parent)
        self.translations = translations
        self.setup_ui()
        
    def setup_ui(self):
        ttk.Label(self, text=self.translations.get("url_label")).pack(side=tk.LEFT)
        
        self.url_entry = ttk.Entry(self, width=30)
        self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.paste_btn = ttk.Button(self, text=self.translations.get("paste_button"), 
                                  width=6)
        self.paste_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # URL validation indicator
        self.url_status = ttk.Label(self, text="", foreground="red")
        self.url_status.pack()