import tkinter as tk
from tkinter import ttk, messagebox
import threading
from downloader import download_video, download_audio
from progress import ProgressHook
from utils import open_folder
import os

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="YouTube Downloader", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)
        
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=10)
        
        url_label = ttk.Label(url_frame, text="YouTube URL:")
        url_label.pack(anchor='w')
        
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(fill=tk.X, pady=5)
        self.url_entry.bind('<KeyRelease>', self.check_url_entry)
        
        type_frame = ttk.LabelFrame(main_frame, text="Download Type", padding=10)
        type_frame.pack(fill=tk.X, pady=10)
        
        self.var = tk.StringVar(value="video")
        ttk.Radiobutton(type_frame, text="Video (MP4)", variable=self.var, value="video").pack(anchor='w', pady=2)
        ttk.Radiobutton(type_frame, text="Audio (MP3)", variable=self.var, value="audio").pack(anchor='w', pady=2)
        ttk.Radiobutton(type_frame, text="Both", variable=self.var, value="both").pack(anchor='w', pady=2)
        
        self.download_btn = ttk.Button(main_frame, text="Download", command=self.start_download)
        self.download_btn.pack(pady=10)
        
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.status_label = ttk.Label(self.progress_frame, text="")
        self.status_label.pack()
        self.progress_frame.pack_forget()

    def hide_progress_bar(self):
        self.progress_bar.pack_forget()

    def check_url_entry(self, event=None):
        if self.url_entry.get().strip():
            self.download_btn.config(state='normal')
        else:
            self.download_btn.config(state='disabled')

    def start_download(self):
        url = self.url_entry.get()
        if not url.strip():
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        self.download_btn.config(state='disabled')
        self.progress_var.set(0)
        self.progress_frame.pack(fill=tk.X, pady=10)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.status_label.config(text="Initializing download...")
        def threaded():
            try:
                download_type = self.var.get()
                if download_type == "video":
                    progress_hook = ProgressHook(self.progress_var, self.status_label, download_type="video")
                    download_video(url, progress_hook)
                    self.status_label.config(text="Video downloaded successfully!")
                    self.hide_progress_bar()
                    open_folder(os.path.abspath("videos"))
                elif download_type == "audio":
                    progress_hook = ProgressHook(self.progress_var, self.status_label, download_type="audio")
                    download_audio(url, progress_hook)
                    self.status_label.config(text="Audio downloaded successfully!")
                    self.hide_progress_bar()
                    open_folder(os.path.abspath("audio"))
                elif download_type == "both":
                    progress_hook_video = ProgressHook(self.progress_var, self.status_label, download_type="video")
                    download_video(url, progress_hook_video)
                    progress_hook_audio = ProgressHook(self.progress_var, self.status_label, download_type="audio")
                    download_audio(url, progress_hook_audio)
                    self.status_label.config(text="Both video and audio downloaded!")
                    self.hide_progress_bar()
                    open_folder(os.path.abspath("videos"))
                    open_folder(os.path.abspath("audio"))
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