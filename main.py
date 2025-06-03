import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from downloader import download_video, download_audio
from utils import is_valid_youtube_url
from progress import ProgressHook
from utils import open_folder
import os

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("700x600")
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
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100, length=600)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.status_label = ttk.Label(self.progress_frame, text="")
        self.status_label.pack()
        self.progress_frame.pack_forget()

        # Add the log area
        self.log_text = ScrolledText(main_frame, height=10, state='disabled', font=("Courier", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def hide_progress_bar(self):
        self.progress_bar.pack_forget()

    def check_url_entry(self, event=None):
        url = self.url_entry.get().strip()
        is_valid, error_message = is_valid_youtube_url(url)
        
        if is_valid:
            self.download_btn.config(state='normal')
            self.status_label.config(text="Valid YouTube URL")
            self.status_label.config(foreground="green")
        else:
            self.download_btn.config(state='disabled')
            if url:  # Only show error if there's some input
                self.status_label.config(text=error_message)
                self.status_label.config(foreground="red")
            else:
                self.status_label.config(text="")

    def append_log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def start_download(self):
        url = self.url_entry.get().strip()
        
        # Validate URL before starting download
        is_valid, error_message = is_valid_youtube_url(url)
        if not is_valid:
            messagebox.showerror("Invalid URL", error_message)
            return
            
        self.append_log(f"URL validation passed: {error_message}")
        self.download_btn.config(state='disabled')
        self.progress_var.set(0)
        self.progress_frame.pack(fill=tk.X, pady=10)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.status_label.config(text="Initializing download...")
        self.append_log("Starting download for URL: " + url)

        def threaded():
            try:
                download_type = self.var.get()
                if download_type == "video":
                    progress_hook = ProgressHook(self.progress_var, self.status_label, download_type="video", log_func=self.append_log)
                    download_video(url, progress_hook)
                    self.status_label.config(text="Video downloaded successfully!")
                    self.append_log("Video downloaded successfully!")
                    self.hide_progress_bar()
                    open_folder(os.path.abspath("videos"))
                elif download_type == "audio":
                    progress_hook = ProgressHook(self.progress_var, self.status_label, download_type="audio", log_func=self.append_log)
                    download_audio(url, progress_hook)
                    self.status_label.config(text="Audio downloaded successfully!")
                    self.append_log("Audio downloaded successfully!")
                    self.hide_progress_bar()
                    open_folder(os.path.abspath("audio"))
                elif download_type == "both":
                    progress_hook_video = ProgressHook(self.progress_var, self.status_label, download_type="video", log_func=self.append_log)
                    download_video(url, progress_hook_video)
                    self.append_log("Video downloaded successfully!")
                    progress_hook_audio = ProgressHook(self.progress_var, self.status_label, download_type="audio", log_func=self.append_log)
                    download_audio(url, progress_hook_audio)
                    self.append_log("Audio downloaded successfully!")
                    self.status_label.config(text="Both video and audio downloaded!")
                    self.hide_progress_bar()
                    open_folder(os.path.abspath("videos"))
                    open_folder(os.path.abspath("audio"))
                self.url_entry.delete(0, tk.END)
                self.download_btn.config(state='disabled')
            except Exception as e:
                error_msg = f"Error: {e}"
                self.status_label.config(text=error_msg)
                self.append_log(error_msg)
                messagebox.showerror("Download Failed", str(e))
                self.download_btn.config(state='normal')
                self.progress_frame.pack_forget()

        threading.Thread(target=threaded).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
