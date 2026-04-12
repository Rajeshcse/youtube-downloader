from yt_dlp import YoutubeDL
import os
from utils import extract_video_id, is_supported_url

# --- Quality format mapping (shared across functions) ---
# Prefer mp4 video + m4a audio; fall back to any codec and remux to mp4
QUALITY_FORMATS = {
    "2160p": "bestvideo[height<=?2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=?2160]+bestaudio/best",
    "1440p": "bestvideo[height<=?1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=?1440]+bestaudio/best",
    "1080p": "bestvideo[height<=?1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=?1080]+bestaudio/best",
    "720p": "bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=?720]+bestaudio/best",
    "360p": "bestvideo[height<=?360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=?360]+bestaudio/best",
}

# --- Helper: build base yt-dlp options dicts ---

def _get_video_opts(outtmpl, progress_hook, quality="720p", is_playlist=False):
    """Return yt-dlp options for video downloads."""
    opts = {
        'format': QUALITY_FORMATS.get(quality, QUALITY_FORMATS["720p"]),
        'merge_output_format': 'mp4',   # always produce .mp4 files
        'outtmpl': outtmpl,
        'progress_hooks': [progress_hook],
        'ignoreerrors': is_playlist,  # tolerate unavailable videos in playlists
        'no_warnings': False,
    }
    if is_playlist:
        opts.update({'noplaylist': False, 'continuedl': True})
    return opts

def _get_audio_opts(outtmpl, progress_hook, is_playlist=False):
    """Return yt-dlp options for audio downloads."""
    opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'ignoreerrors': is_playlist,
        'no_warnings': False,
    }
    if is_playlist:
        opts.update({'noplaylist': False, 'continuedl': True})
    return opts

def _download_with_playlist_info(ydl, url, progress_hook):
    """Extract playlist metadata to prime the progress hook, then download."""
    info = ydl.extract_info(url, download=False)
    if 'entries' in info:
        available_count = sum(1 for entry in info['entries'] if entry is not None)
        progress_hook.set_playlist_info(available_count)
    ydl.download([url])

# --- Public API ---

def download_video(url, progress_hook, quality="720p"):
    """Download a single video from any yt-dlp supported site (YouTube, Vimeo, etc.)."""
    os.makedirs("videos", exist_ok=True)
    if not is_supported_url(url):
        raise Exception("Invalid or unsupported URL")
    opts = _get_video_opts('videos/%(title)s.%(ext)s', progress_hook, quality)
    with YoutubeDL(opts) as ydl:
        ydl.download([url])

def download_audio(url, progress_hook):
    """Download audio from any yt-dlp supported site (YouTube, Vimeo, etc.)."""
    os.makedirs("audio", exist_ok=True)
    if not is_supported_url(url):
        raise Exception("Invalid or unsupported URL")
    opts = _get_audio_opts('audio/%(title)s.%(ext)s', progress_hook)
    with YoutubeDL(opts) as ydl:
        ydl.download([url])

def download_playlist_video(url, progress_hook, playlist_items=None, quality="720p"):
    """Download playlist videos. playlist_items can be 'all', '1-5', '1,3,5', etc."""
    os.makedirs("videos", exist_ok=True)
    opts = _get_video_opts(
        'videos/%(playlist_title)s/%(playlist_index)02d_%(title)s.%(ext)s',
        progress_hook, quality, is_playlist=True
    )
    if playlist_items and playlist_items.lower() != 'all':
        opts['playlist_items'] = playlist_items
    with YoutubeDL(opts) as ydl:
        _download_with_playlist_info(ydl, url, progress_hook)

def download_playlist_audio(url, progress_hook, playlist_items=None):
    """Download playlist audio. playlist_items can be 'all', '1-5', '1,3,5', etc."""
    os.makedirs("audio", exist_ok=True)
    opts = _get_audio_opts(
        'audio/%(playlist_title)s/%(playlist_index)02d_%(title)s.%(ext)s',
        progress_hook, is_playlist=True
    )
    if playlist_items and playlist_items.lower() != 'all':
        opts['playlist_items'] = playlist_items
    with YoutubeDL(opts) as ydl:
        _download_with_playlist_info(ydl, url, progress_hook) 