# YouTube Downloader - Distribution Guide

## Overview
This guide explains how to share and use the standalone YouTube Downloader executable (`YouTubeDownloader.exe`) on any Windows PC.

## What's Included
The `YouTubeDownloader.exe` file is a **self-contained executable** that includes:
- Complete Python runtime
- All required Python libraries (yt-dlp, tkinter, etc.)
- FFmpeg and FFprobe binaries (for video/audio processing)
- Application code and GUI

## File Information
- **File Name:** `YouTubeDownloader.exe`
- **File Size:** ~90 MB
- **Location:** `dist/YouTubeDownloader.exe`
- **Type:** Single file executable with console window

## System Requirements
- **Operating System:** Windows 7 or later (Windows 10/11 recommended)
- **Architecture:** 64-bit Windows
- **Internet Connection:** Required for downloading videos
- **Disk Space:** At least 500 MB free (for downloaded videos)

## How to Share the Application

### Option 1: Direct File Sharing
1. Navigate to: `C:\Users\LAVANNIA\mycode\youtube-downloader\dist\`
2. Copy the `YouTubeDownloader.exe` file
3. Share via:
   - USB drive
   - Email (if file size permits)
   - Cloud storage (Google Drive, OneDrive, Dropbox)
   - Network file share

### Option 2: Compressed Archive (Recommended)
For easier sharing, compress the executable:

```powershell
# Using PowerShell
Compress-Archive -Path "dist\YouTubeDownloader.exe" -DestinationPath "YouTubeDownloader.zip"
```

Or right-click the file → "Send to" → "Compressed (zipped) folder"

## How to Use (For End Users)

### First Time Setup
1. Download/receive the `YouTubeDownloader.exe` file
2. Move it to a permanent location (e.g., `C:\Programs\YouTubeDownloader\`)
3. **Important:** Windows may show a security warning on first run:
   - Click "More info"
   - Click "Run anyway"
   - This is normal for unsigned executables

### Running the Application
1. Double-click `YouTubeDownloader.exe`
2. You'll see:
   - A **console window** (black terminal window - shows download progress)
   - The **main application window** (GUI for entering URLs and settings)
3. Both windows are normal and expected

### Using the Application
1. Copy a video URL from YouTube, Vimeo, or other supported sites
2. Paste the URL into the application
3. Select your preferences:
   - Download type: Video, Audio, or Both
   - Video quality: 360p, 720p, 1080p, 1440p, or 2160p (4K)
4. Click "Download"
5. Downloaded files will be saved to:
   - **Videos:** `videos/` folder (created next to the .exe)
   - **Audio:** `audio/` folder (created next to the .exe)

### Playlist Support
- The application automatically detects YouTube playlists
- Options:
  - Download entire playlist
  - Download specific range (e.g., 1-5)
  - Download specific videos (e.g., 1,3,5)
  - Download just the single video from the URL

## Supported Platforms
The application can download from 1000+ websites including:
- YouTube (videos and playlists)
- Vimeo
- DailyMotion
- Facebook
- Instagram
- TikTok
- And many more (powered by yt-dlp)

## Troubleshooting

### "Windows protected your PC" Warning
- This is normal for unsigned executables
- Click "More info" → "Run anyway"
- Or: Right-click → Properties → Check "Unblock" → Apply

### Application Won't Start
- Ensure you're running on 64-bit Windows
- Check if antivirus is blocking the file (add exception if needed)
- Try running as Administrator (right-click → "Run as administrator")

### Downloads Failing
- Check your internet connection
- Some videos may be region-restricted or private
- YouTube may temporarily block downloads if too many are made quickly

### Console Window Shows Errors
- FFmpeg errors: The bundled FFmpeg should work automatically
- yt-dlp errors: May indicate the video URL is invalid or restricted
- Network errors: Check firewall/internet connection

## Advanced Information

### How It Works
The executable uses:
- **PyInstaller** to bundle Python and all dependencies
- **yt-dlp** for downloading videos from multiple platforms
- **FFmpeg** (bundled) for video/audio processing and conversion
- **Tkinter** for the graphical user interface

### No Installation Required
- The .exe is **portable** - no installation needed
- Can run from USB drive, network share, or any folder
- Creates `videos/` and `audio/` folders where it's located
- No registry modifications
- No system files created outside the application folder

### Security Notes
- The application does not:
  - Collect personal data
  - Connect to any servers except the video hosting sites
  - Modify Windows system files
  - Install background services
- All downloads are saved locally in the videos/audio folders

## Building from Source

If you want to rebuild the executable yourself:

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Ensure FFmpeg binaries are in bin/ folder
# (ffmpeg.exe and ffprobe.exe)

# 3. Build the executable
pyinstaller YouTubeDownloader.spec --clean

# 4. Find the executable in dist/ folder
```

## License & Credits
- **Application:** Created by Rajesh
- **yt-dlp:** Open source video downloader (https://github.com/yt-dlp/yt-dlp)
- **FFmpeg:** Open source multimedia framework (https://ffmpeg.org)

## Support
For issues or questions:
1. Check the Troubleshooting section above
2. Ensure you're using the latest version
3. Report issues to the developer

---

**Version:** 1.0
**Last Updated:** April 2026
**Build Date:** April 12, 2026
