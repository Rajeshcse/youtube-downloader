class ProgressHook:
    def __init__(self, progress_var, status_label, download_type="video"):
        self.progress_var = progress_var
        self.status_label = status_label
        self.download_type = download_type
        self.playlist_total = 0
        self.current_video = 0

    def set_playlist_info(self, total_videos):
        """Set playlist information for progress tracking"""
        self.playlist_total = total_videos
        self.current_video = 0

    def __call__(self, d):
        if d['status'] == 'downloading':
            try:
                # Update current video number from playlist index
                if 'playlist_index' in d and d['playlist_index'] is not None:
                    self.current_video = d['playlist_index']

                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    percentage = (downloaded / total) * 100
                    self.progress_var.set(percentage)

                    # Format status message based on whether it's a playlist
                    if self.playlist_total > 0:
                        if self.download_type == "audio":
                            self.status_label.config(text=f"Downloading audio {self.current_video} of {self.playlist_total}... {percentage:.1f}%")
                        else:
                            self.status_label.config(text=f"Downloading video {self.current_video} of {self.playlist_total}... {percentage:.1f}%")
                    else:
                        if self.download_type == "audio":
                            self.status_label.config(text=f"Audio downloading... {percentage:.1f}%")
                        else:
                            self.status_label.config(text=f"Video downloading... {percentage:.1f}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            if self.playlist_total > 0:
                self.status_label.config(text=f"Processing video {self.current_video} of {self.playlist_total}...")
            else:
                self.status_label.config(text="Processing Please wait...") 