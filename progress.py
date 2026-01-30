class ProgressHook:
    def __init__(self, progress_var, status_label, download_type="video", log_func=None, counter_func=None):
        self.progress_var = progress_var
        self.status_label = status_label
        self.download_type = download_type
        self.log_func = log_func
        self.counter_func = counter_func
        self.total_videos = None
        self.current_video = 0

    def __call__(self, d):
        # Detect playlist size and index
        if '_total_playlist_videos' in d:
            self.total_videos = d['_total_playlist_videos']
        if '_playlist_index' in d:
            self.current_video = d['_playlist_index']

        if d['status'] == 'downloading':
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                pct = (downloaded / total) * 100
                if self.total_videos:
                    overall = 100 * (self.current_video - 1 + pct / 100) / self.total_videos
                    self.progress_var.set(overall)
                    status = f"{self.download_type.title()} downloading... {self.current_video}/{self.total_videos} ({pct:.1f}%)"
                else:
                    self.progress_var.set(pct)
                    status = f"{self.download_type.title()} downloading... ({pct:.1f}%)"

                self.status_label.config(text=status)
                if self.log_func:
                    self.log_func(status)

        elif d['status'] == 'finished':
            if self.total_videos:
                msg = f"{self.download_type.title()} completed {self.current_video}/{self.total_videos}"
                if self.counter_func:
                    self.counter_func(self.current_video, self.total_videos)
            else:
                msg = "Processing, please wait..."
            self.status_label.config(text=msg)
            if self.log_func:
                self.log_func(msg)
            self.progress_var.set(100)
