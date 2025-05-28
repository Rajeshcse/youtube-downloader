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