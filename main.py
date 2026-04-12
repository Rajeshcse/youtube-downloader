import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from downloader import download_video, download_audio, download_playlist_video, download_playlist_audio
from progress import ProgressHook
from utils import open_folder, is_playlist_url, is_supported_url, is_youtube_url, extract_video_id
import os

class PlaylistDialog:
    def __init__(self, parent):
        self.result = None
        self.range_value = "all"

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Playlist Detected")
        self.dialog.geometry("400x280")
        self.dialog.resizable(False, False)

        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()

        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Playlist Detected!", font=('Helvetica', 12, 'bold'))
        title_label.pack(pady=10)

        info_label = ttk.Label(main_frame, text="What would you like to download?")
        info_label.pack(pady=5)

        self.choice_var = tk.StringVar(value="all")
        self.choice_var.trace_add("write", lambda *_: self._toggle_range())

        ttk.Radiobutton(main_frame, text="Download entire playlist", variable=self.choice_var, value="all").pack(anchor='w', pady=5)
        ttk.Radiobutton(main_frame, text="Download specific range", variable=self.choice_var, value="range").pack(anchor='w', pady=5)
        ttk.Radiobutton(main_frame, text="Download just this video", variable=self.choice_var, value="single").pack(anchor='w', pady=5)

        self.range_frame = ttk.Frame(main_frame)
        # Do NOT pack yet — hidden until "range" is selected

        range_label = ttk.Label(self.range_frame, text="Range (e.g., 1-5 or 1,3,5):")
        range_label.pack(side=tk.LEFT, padx=(0, 5))

        self.range_entry = ttk.Entry(self.range_frame, width=15)
        self.range_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.range_entry.insert(0, "1-10")

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)

    def _toggle_range(self):
        """Show the range input only when 'Download specific range' is selected."""
        if self.choice_var.get() == "range":
            self.range_frame.pack(fill=tk.X, pady=10, before=self.range_frame.master.winfo_children()[-1])
            self.dialog.geometry("400x320")
        else:
            self.range_frame.pack_forget()
            self.dialog.geometry("400x280")

    def ok_clicked(self):
        choice = self.choice_var.get()
        if choice == "range":
            self.result = ("range", self.range_entry.get().strip())
        else:
            self.result = (choice, None)
        self.dialog.destroy()

    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("600x620")
        self.root.configure(bg='#f0f0f0')
        
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Video Downloader", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)
        
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=10)
        
        url_label = ttk.Label(url_frame, text="Video URL (YouTube, Vimeo, and more):")
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

        quality_frame = ttk.LabelFrame(main_frame, text="Video Quality", padding=10)
        quality_frame.pack(fill=tk.X, pady=10)

        self.quality_var = tk.StringVar(value="1080p")
        ttk.Radiobutton(quality_frame, text="4K (2160p)", variable=self.quality_var, value="2160p").pack(anchor='w', pady=2)
        ttk.Radiobutton(quality_frame, text="2K (1440p)", variable=self.quality_var, value="1440p").pack(anchor='w', pady=2)
        ttk.Radiobutton(quality_frame, text="1080p (Full HD) - Recommended", variable=self.quality_var, value="1080p").pack(anchor='w', pady=2)
        ttk.Radiobutton(quality_frame, text="720p (HD)", variable=self.quality_var, value="720p").pack(anchor='w', pady=2)
        ttk.Radiobutton(quality_frame, text="360p (Mobile)", variable=self.quality_var, value="360p").pack(anchor='w', pady=2)

        self.download_btn = ttk.Button(main_frame, text="Download", command=self.start_download)
        self.download_btn.pack(pady=10)
        
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.status_label = ttk.Label(self.progress_frame, text="")
        self.status_label.pack()

        self.folder_btn = ttk.Button(self.progress_frame, text="Open Download Folder", command=self.open_download_folder)
        self.folder_btn.pack(pady=10)
        self.folder_btn.pack_forget()

        self.download_folder_path = None
        self.progress_frame.pack_forget()

    # --- Helpers ---

    def hide_progress_bar(self):
        self.progress_bar.pack_forget()

    def _on_download_complete(self, status_text, folder):
        """Called after a successful download to update UI state."""
        self.status_label.config(text=status_text)
        self.hide_progress_bar()
        self.download_folder_path = os.path.abspath(folder)
        self.folder_btn.pack(pady=10)

    def open_download_folder(self):
        if self.download_folder_path:
            open_folder(self.download_folder_path)

    def check_url_entry(self, event=None):
        if self.url_entry.get().strip():
            self.download_btn.config(state='normal')
        else:
            self.download_btn.config(state='disabled')

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return
        if not is_supported_url(url):
            messagebox.showerror("Error", "Please enter a valid http/https URL.")
            return

        # Playlist detection only applies to YouTube
        is_playlist = is_youtube_url(url) and is_playlist_url(url)
        playlist_choice = None
        playlist_items = None

        if is_playlist:
            # Show playlist dialog
            dialog = PlaylistDialog(self.root)
            self.root.wait_window(dialog.dialog)

            if dialog.result is None:
                # User cancelled
                return

            playlist_choice, playlist_items = dialog.result

            if playlist_choice == "single":
                # Strip playlist parameters — pass only the video part of the URL
                video_id = extract_video_id(url)
                if video_id:
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    is_playlist = False
                else:
                    # Fallback: use URL as-is (non-YouTube playlist edge case)
                    is_playlist = False

        self.download_btn.config(state='disabled')
        self.progress_var.set(0)
        self.folder_btn.pack_forget()
        self.progress_frame.pack(fill=tk.X, pady=10)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.status_label.config(text="Initializing download...")

        def threaded():
            try:
                download_type = self.var.get()

                quality = self.quality_var.get()

                if is_playlist:
                    # Playlist download
                    if download_type == "video":
                        hook = ProgressHook(self.progress_var, self.status_label, download_type="video")
                        download_playlist_video(url, hook, playlist_items, quality)
                        self._on_download_complete("Playlist videos downloaded successfully!", "videos")
                    elif download_type == "audio":
                        hook = ProgressHook(self.progress_var, self.status_label, download_type="audio")
                        download_playlist_audio(url, hook, playlist_items)
                        self._on_download_complete("Playlist audio downloaded successfully!", "audio")
                    elif download_type == "both":
                        hook_v = ProgressHook(self.progress_var, self.status_label, download_type="video")
                        download_playlist_video(url, hook_v, playlist_items, quality)
                        hook_a = ProgressHook(self.progress_var, self.status_label, download_type="audio")
                        download_playlist_audio(url, hook_a, playlist_items)
                        self._on_download_complete("Playlist video and audio downloaded!", "videos")
                else:
                    # Single video download
                    if download_type == "video":
                        hook = ProgressHook(self.progress_var, self.status_label, download_type="video")
                        download_video(url, hook, quality)
                        self._on_download_complete("Video downloaded successfully!", "videos")
                    elif download_type == "audio":
                        hook = ProgressHook(self.progress_var, self.status_label, download_type="audio")
                        download_audio(url, hook)
                        self._on_download_complete("Audio downloaded successfully!", "audio")
                    elif download_type == "both":
                        hook_v = ProgressHook(self.progress_var, self.status_label, download_type="video")
                        download_video(url, hook_v, quality)
                        hook_a = ProgressHook(self.progress_var, self.status_label, download_type="audio")
                        download_audio(url, hook_a)
                        self._on_download_complete("Both video and audio downloaded!", "videos")

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