import re
import os
import platform
import subprocess
from urllib.parse import urlparse

def is_supported_url(url):
    """Return True if the URL looks like a valid http/https video URL."""
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
    except Exception:
        return False

def is_youtube_url(url):
    """Return True if the URL belongs to YouTube or youtu.be."""
    try:
        host = urlparse(url.strip()).netloc.lower()
        return any(h in host for h in ('youtube.com', 'youtu.be'))
    except Exception:
        return False

def is_playlist_url(url):
    """Check if URL is a YouTube playlist"""
    playlist_patterns = [
        r'[?&]list=([^&]+)',
        r'youtube\.com/playlist\?list=([^&]+)'
    ]
    for pattern in playlist_patterns:
        if re.search(pattern, url):
            return True
    return False

def extract_playlist_id(url):
    """Extract playlist ID from YouTube URL"""
    pattern = r'[?&]list=([^&]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def extract_video_id(url):
    """Extract video ID from YouTube URL or playlist URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path]) 