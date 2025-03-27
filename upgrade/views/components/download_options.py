import tkinter as tk
from tkinter import ttk
from utils.constants import SUPPORTED_FORMATS, QUALITY_OPTIONS

class DownloadOptions(ttk.LabelFrame):
    def __init__(self, parent, translations):
        super().__init__(parent, text=translations.get("download_options"), padding=10)
        self.translations = translations
        self.format_var = tk.StringVar(value="mp4")
        self.quality_var = tk.StringVar(value="720p")
        self.bitrate_var = tk.StringVar(value="128")
        self.setup_ui()
        
    def setup_ui(self):
        # Format selection
        ttk.Label(self, text=self.translations.get("format_label")).grid(row=0, column=0, sticky=tk.W)
        format_combo = ttk.Combobox(self, textvariable=self.format_var, 
                                  values=SUPPORTED_FORMATS, state="readonly", width=10)
        format_combo.grid(row=0, column=1, sticky=tk.W)
        format_combo.bind("<<ComboboxSelected>>", self.update_quality_options)
        
        # Quality options frame
        self.quality_frame = ttk.Frame(self)
        self.quality_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.update_quality_options()
    
    def update_quality_options(self, event=None):
        # Clear existing widgets
        for widget in self.quality_frame.winfo_children():
            widget.destroy()
        
        format_type = self.format_var.get()
        
        if format_type == "mp4":
            ttk.Label(self.quality_frame, text=self.translations.get("quality_label")).pack(side=tk.LEFT)
            quality_combo = ttk.Combobox(self.quality_frame, textvariable=self.quality_var, 
                                       values=QUALITY_OPTIONS["mp4"], state="readonly", width=10)
            quality_combo.pack(side=tk.LEFT)
        else:
            ttk.Label(self.quality_frame, text=self.translations.get("bitrate_label")).pack(side=tk.LEFT)
            bitrate_combo = ttk.Combobox(self.quality_frame, textvariable=self.bitrate_var, 
                                       values=QUALITY_OPTIONS["mp3"], state="readonly", width=10)
            bitrate_combo.pack(side=tk.LEFT)
    
    def get_options(self):
        """Trả về các tùy chọn download dưới dạng dict"""
        return {
            "format": self.format_var.get(),
            "quality": self.quality_var.get() if self.format_var.get() == "mp4" else None,
            "bitrate": self.bitrate_var.get() if self.format_var.get() == "mp3" else None
        }