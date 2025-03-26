import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import threading
from tkinter import Menu

# Resource path function
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# FFmpeg path
ffmpeg_path = resource_path("FFmpeg/bin/ffmpeg.exe")

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional YouTube Downloader")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Variables
        self.video_title = tk.StringVar()
        self.download_format = tk.StringVar(value="mp4")
        self.quality = tk.StringVar(value="720p")
        self.bitrate = tk.StringVar(value="128")
        
        self.create_widgets()
        self.setup_context_menu()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(main_frame, text="YouTube Video Downloader", style='Header.TLabel')
        header.pack(pady=(0, 20))
        
        # URL Entry with Paste button
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="YouTube URL:").pack(side=tk.LEFT, padx=(0, 10))
        
        # URL Entry
        self.url_entry = ttk.Entry(url_frame, width=30)
        self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Paste button
        paste_btn = ttk.Button(url_frame, text="Paste", command=self.paste_from_clipboard, width=6)
        paste_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Video Info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text="Video Title:").pack(side=tk.LEFT, padx=(0, 10))
        title_entry = ttk.Entry(info_frame, textvariable=self.video_title, state="readonly", width=40)
        title_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Format Options
        format_frame = ttk.LabelFrame(main_frame, text="Download Options", padding=10)
        format_frame.pack(fill=tk.X, pady=10)
        
        # Format selection
        ttk.Label(format_frame, text="Format:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.format_options = ttk.Combobox(format_frame, textvariable=self.download_format, 
                                        values=["mp4", "mp3"], state="readonly", width=10)
        self.format_options.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.format_options.bind("<<ComboboxSelected>>", self.update_quality_options)
        
        # Quality selection frame
        self.quality_frame = ttk.Frame(format_frame)
        self.quality_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Initialize quality options
        self.update_quality_options()
        
        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Buttons
        ttk.Button(button_frame, text="Get Video Info", command=self.fetch_video_info, 
                  style='Accent.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Download", command=self.download_video, 
                  style='Accent.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_fields).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).grid(row=0, column=3, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Configure styles
        self.style.configure('Accent.TButton', foreground='white', background='#4CAF50')
        self.style.map('Accent.TButton', 
                      background=[('active', '#45a049'), ('pressed', '#39843f')])
        
        # Set focus to URL entry
        self.url_entry.focus()
    
    def setup_context_menu(self):
        # Create a context menu
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Paste", command=self.paste_from_clipboard)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        
        # Bind right-click event
        self.url_entry.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def paste_from_clipboard(self):
        try:
            # Get clipboard content
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                # Clear current selection if any
                self.url_entry.selection_clear()
                # Insert at cursor position
                self.url_entry.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            # Clipboard might be empty or contains non-text data
            pass
    
    def cut_text(self):
        self.url_entry.event_generate("<<Cut>>")
    
    def copy_text(self):
        self.url_entry.event_generate("<<Copy>>")
    
    def update_quality_options(self, event=None):
        # Clear existing widgets
        for widget in self.quality_frame.winfo_children():
            widget.destroy()
        
        format_type = self.download_format.get()
        
        if format_type == "mp4":
            ttk.Label(self.quality_frame, text="Quality:").pack(side=tk.LEFT, padx=(0, 10))
            quality_options = ttk.Combobox(self.quality_frame, textvariable=self.quality, 
                                         values=["1080p", "720p", "480p"], state="readonly", width=10)
            quality_options.pack(side=tk.LEFT)
            self.quality.set("720p")  # Default for mp4
        else:
            ttk.Label(self.quality_frame, text="Bitrate (kbps):").pack(side=tk.LEFT, padx=(0, 10))
            bitrate_options = ttk.Combobox(self.quality_frame, textvariable=self.bitrate, 
                                         values=["64", "96", "128", "160", "192", "256", "320"], 
                                         state="readonly", width=10)
            bitrate_options.pack(side=tk.LEFT)
            self.bitrate.set("128")  # Default for mp3
    
    def fetch_video_info(self):
        link = self.url_entry.get()
        if not link:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        self.status_var.set("Fetching video info...")
        self.root.update()
        
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=False)
                self.video_title.set(info_dict.get('title', 'No title available'))
                self.status_var.set("Video info fetched successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch video info.\nDetails: {e}")
            self.status_var.set("Error fetching video info")
    
    def download_video(self):
        def download_task():
            link = self.url_entry.get()
            if not link:
                messagebox.showerror("Error", "Please enter a valid YouTube URL")
                return

            try:
                # Set default extension based on format
                ext = self.download_format.get()
                file_types = [(f"{ext.upper()} files", f"*.{ext}")]
                
                save_path = filedialog.asksaveasfilename(
                    title="Choose save location",
                    defaultextension=f".{ext}",
                    filetypes=file_types,
                )
                
                if not save_path:
                    messagebox.showerror("Error", "Please select a save location")
                    return

                # Configure download options
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

                self.status_var.set("Downloading...")
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                messagebox.showinfo("Success", f"Download completed!\nSaved to: {save_path}")
                self.status_var.set("Download completed")
            except Exception as e:
                messagebox.showerror("Error", f"Download failed.\nDetails: {e}")
                self.status_var.set("Download failed")

        threading.Thread(target=download_task, daemon=True).start()
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            self.status_var.set(f"Downloading: {percent} at {speed}")
            self.root.update()
    
    def reset_fields(self):
        self.url_entry.delete(0, tk.END)
        self.video_title.set("")
        self.download_format.set("mp4")
        self.quality.set("720p")
        self.bitrate.set("128")
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()