import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp
import os
import re
import subprocess
import platform

def extract_video_id(url):
    """Extract video ID from YouTube URL or playlist URL"""
    # Regular expressions for different YouTube URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard video URL
        r'(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)',  # Video URL with parameters
        r'youtu\.be\/([0-9A-Za-z_-]{11})',  # Short URL
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

class ProgressHook:
    def __init__(self, progress_var, status_label, download_type="video"):
        self.progress_var = progress_var
        self.status_label = status_label
        self.download_type = download_type

    def __call__(self, d):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    percentage = (downloaded / total) * 100
                    self.progress_var.set(percentage)
                    if self.download_type == "audio":
                        self.status_label.config(text=f"Audio downloading... {percentage:.1f}%")
                    else:
                        self.status_label.config(text=f"Video downloading... {percentage:.1f}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.status_label.config(text="Processing Please wait...")

def download_video(url, progress_hook):
    os.makedirs("videos", exist_ok=True)
    video_id = extract_video_id(url)
    if not video_id:
        raise Exception("Invalid YouTube URL")
        
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
    }
    with yt_dlp.YoutubeDL(video_opts) as ydl:
        ydl.download([video_url])

def download_audio(url, progress_hook):
    os.makedirs("audio", exist_ok=True)
    video_id = extract_video_id(url)
    if not video_id:
        raise Exception("Invalid YouTube URL")
        
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
    }
    with yt_dlp.YoutubeDL(audio_opts) as ydl:
        ydl.download([video_url])

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Downloader", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)
        
        # URL Frame
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=10)
        
        url_label = ttk.Label(url_frame, text="YouTube URL:")
        url_label.pack(anchor='w')
        
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(fill=tk.X, pady=5)
        self.url_entry.bind('<KeyRelease>', self.check_url_entry)
        
        # Download Type Frame
        type_frame = ttk.LabelFrame(main_frame, text="Download Type", padding=10)
        type_frame.pack(fill=tk.X, pady=10)
        
        self.var = tk.StringVar(value="video")
        ttk.Radiobutton(type_frame, text="Video (MP4)", variable=self.var, value="video").pack(anchor='w', pady=2)
        ttk.Radiobutton(type_frame, text="Audio (MP3)", variable=self.var, value="audio").pack(anchor='w', pady=2)
        ttk.Radiobutton(type_frame, text="Both", variable=self.var, value="both").pack(anchor='w', pady=2)
        
        # Download Button
        self.download_btn = ttk.Button(main_frame, text="Download", command=self.start_download)
        self.download_btn.pack(pady=10)
        
        # Progress Frame
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(self.progress_frame, text="")
        self.status_label.pack()
        
        # Initially hide progress frame
        self.progress_frame.pack_forget()

    def check_url_entry(self, event=None):
        """Enable download button if URL entry is not empty"""
        if self.url_entry.get().strip():
            self.download_btn.config(state='normal')
        else:
            self.download_btn.config(state='disabled')

    def open_folder(self, path):
        """Open folder in file explorer"""
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", path])
        else:  # Linux
            subprocess.run(["xdg-open", path])

    def hide_progress_bar(self):
        """Hide the progress bar widget"""
        self.progress_bar.pack_forget()

    def start_download(self):
        url = self.url_entry.get()
        if not url.strip():
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
            
        self.download_btn.config(state='disabled')
        self.progress_var.set(0)
        self.progress_frame.pack(fill=tk.X, pady=10)
        self.progress_bar.pack(fill=tk.X, pady=5)  # Always show at start
        self.status_label.config(text="Initializing download...")
        
        def threaded():
            try:
                download_type = self.var.get()
                if download_type == "video":
                    progress_hook = ProgressHook(self.progress_var, self.status_label, download_type="video")
                    download_video(url, progress_hook)
                    self.status_label.config(text="Video downloaded successfully!")
                    self.hide_progress_bar()
                    self.open_folder(os.path.abspath("videos"))
                elif download_type == "audio":
                    progress_hook = ProgressHook(self.progress_var, self.status_label, download_type="audio")
                    download_audio(url, progress_hook)
                    self.status_label.config(text="Audio downloaded successfully!")
                    self.hide_progress_bar()
                    self.open_folder(os.path.abspath("audio"))
                elif download_type == "both":
                    progress_hook_video = ProgressHook(self.progress_var, self.status_label, download_type="video")
                    download_video(url, progress_hook_video)
                    progress_hook_audio = ProgressHook(self.progress_var, self.status_label, download_type="audio")
                    download_audio(url, progress_hook_audio)
                    self.status_label.config(text="Both video and audio downloaded!")
                    self.hide_progress_bar()
                    self.open_folder(os.path.abspath("videos"))
                    self.open_folder(os.path.abspath("audio"))
                
                # Clear input and disable button after successful download
                self.url_entry.delete(0, tk.END)
                self.download_btn.config(state='disabled')
                
            except Exception as e:
                self.status_label.config(text=f"Error: {e}")
                messagebox.showerror("Download Failed", str(e))
                self.download_btn.config(state='normal')
                self.progress_frame.pack_forget()
        
        threading.Thread(target=threaded).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
