import tkinter as tk
from tkinter import messagebox
from downloader import YouTubeDownloader

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")

        # Giao diện nhập URL
        self.label = tk.Label(root, text="Nhập URL YouTube:")
        self.label.pack(pady=5)

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.download_button = tk.Button(root, text="Tải Video", command=self.start_download)
        self.download_button.pack(pady=10)

        self.info_label = tk.Label(root, text="", fg="blue")
        self.info_label.pack(pady=5)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Lỗi", "Vui lòng nhập URL!")
            return

        downloader = YouTubeDownloader(url)
        info = downloader.fetch_video_info()

        if "error" in info:
            messagebox.showerror("Lỗi", info["error"])
            return
        
        self.info_label.config(text=f"Đang tải: {info['title']} ({info['length']} giây)")
        result = downloader.download_video()
        messagebox.showinfo("Hoàn thành", result)

