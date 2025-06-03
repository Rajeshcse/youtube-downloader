import os
import platform
import subprocess
import re
from urllib.parse import urlparse, parse_qs
import requests

def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])

def is_valid_youtube_url(url):
    """
    Validate if the given URL is a valid YouTube URL.
    Returns (is_valid, error_message)
    """
    if not url:
        return False, "URL cannot be empty"

    # YouTube URL patterns
    patterns = [
        r'^https?:\/\/(?:www\.)?youtube\.com\/watch\?v=[\w-]+',  # Standard watch URLs
        r'^https?:\/\/(?:www\.)?youtube\.com\/playlist\?list=[\w-]+',  # Playlist URLs
        r'^https?:\/\/youtu\.be\/[\w-]+',  # Shortened URLs
        r'^https?:\/\/(?:www\.)?youtube\.com\/shorts\/[\w-]+',  # Shorts URLs
    ]

    # Check if URL matches any valid YouTube pattern
    if not any(re.match(pattern, url) for pattern in patterns):
        return False, "Invalid YouTube URL format"

    try:
        # Try to get the video page to verify it exists
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code != 200:
            return False, f"Video not accessible (Status code: {response.status_code})"
        return True, "Valid YouTube URL"
    except requests.RequestException as e:
        return False, f"Error checking URL: {str(e)}"

def extract_video_id(url):
    """
    Extract video ID from YouTube URL
    """
    if 'youtube.com' in url:
        parsed_url = urlparse(url)
        if 'watch' in url:
            return parse_qs(parsed_url.query).get('v', [None])[0]
        elif 'shorts' in url:
            return parsed_url.path.split('/')[-1]
    elif 'youtu.be' in url:
        return urlparse(url).path[1:]
    return None
