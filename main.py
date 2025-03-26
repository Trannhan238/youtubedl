import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import threading

# Hàm xác định đường dẫn tài nguyên
def resource_path(relative_path):
    """Trả về đường dẫn đầy đủ khi chạy file đã đóng gói."""
    try:
        base_path = sys._MEIPASS  # Path tạm khi chạy file exe
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Đường dẫn đến FFmpeg
ffmpeg_path = resource_path("FFmpeg/bin/ffmpeg.exe")

def download_video():
    def download_task():
        link = url_entry.get()
        if not link:
            messagebox.showerror("Lỗi!", "Hãy nhập đường dẫn YouTube hợp lệ")
            return

        try:
            save_path = filedialog.asksaveasfilename(
                title="Chọn nơi lưu video",
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4")],
            )
            if not save_path:
                messagebox.showerror("Lỗi!", "Hãy chọn nơi lưu video")
                return

            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': save_path,
                'merge_output_format': 'mp4',
                'ffmpeg_location': ffmpeg_path,  # Chỉ định FFmpeg
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            messagebox.showinfo("Hoàn thành", f"Tải video hoàn thành!\nLưu tại: {save_path}")
        except Exception as e:
            messagebox.showerror("Lỗi:", f"Không thể tải video.\nChi tiết: {e}")

    # Chạy tải video trong một luồng riêng để không làm treo giao diện
    threading.Thread(target=download_task, daemon=True).start()

def fetch_video_info():
    link = url_entry.get()
    if not link:
        messagebox.showerror("Lỗi!", "Chưa nhập đường dẫn video")
        return

    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_title.set(info_dict.get('title', 'Không có tiêu đề'))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lấy thông tin video.\nChi tiết: {e}")

def reset_fields():
    url_entry.delete(0, tk.END)
    video_title.set("")

def exit_app():
    root.quit()

# Giao diện chính
root = tk.Tk()
root.title("YouTube Downloader By Trần Nhân")
root.geometry("400x400")
root.resizable(False, False)

video_title = tk.StringVar()

# Nhập URL
tk.Label(root, text="Nhập đường dẫn video YouTube :").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Hiển thị tiêu đề
tk.Label(root, text="Tên video:").pack(pady=5)
tk.Entry(root, textvariable=video_title, state="readonly", width=50).pack(pady=5)

# Nút kiểm tra và tải
tk.Button(root, text="Kiểm tra", command=fetch_video_info, bg="orange", fg="white").pack(pady=5)
tk.Button(root, text="Download", command=download_video, bg="green", fg="white").pack(pady=10)

# Nút reset và thoát
tk.Button(root, text="Reset", command=reset_fields, bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Thoát", command=exit_app, bg="red", fg="white").pack(pady=5)

# Vòng lặp giao diện
root.mainloop()
