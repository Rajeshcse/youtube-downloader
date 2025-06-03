from yt_dlp import YoutubeDL
import os

def download_video(url, progress_hook):
    os.makedirs("videos", exist_ok=True)
    video_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'videos/%(playlist_title)s/%(title)s.%(ext)s',  # Playlist subfolder support
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,  # Skip errored videos
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
    }
    with YoutubeDL(video_opts) as ydl:
        ydl.download([url])

def download_audio(url, progress_hook):
    os.makedirs("audio", exist_ok=True)
    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio/%(playlist_title)s/%(title)s.%(ext)s',  # Playlist subfolder support
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
    }
    with YoutubeDL(audio_opts) as ydl:
        ydl.download([url])
