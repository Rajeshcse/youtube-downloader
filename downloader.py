from yt_dlp import YoutubeDL
import os
from utils import extract_video_id

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
    with YoutubeDL(video_opts) as ydl:
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
    with YoutubeDL(audio_opts) as ydl:
        ydl.download([video_url]) 