import os
from yt_dlp import YoutubeDL
import asyncio

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

async def download_video(url: str) -> str:
    """
    Download video using yt-dlp into temp folder.
    Returns local file path.
    """
    ydl_opts = {
        "outtmpl": os.path.join(TEMP_DIR, "%(title)s.%(ext)s"),
        "quiet": True,
    }
    loop = asyncio.get_event_loop()
    def run_yt():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        return os.path.join(TEMP_DIR, f"{info['title']}.{info['ext']}")
    filepath = await loop.run_in_executor(None, run_yt)
    return filepath

async def clear_temp_files():
    """Delete all files in TEMP_DIR"""
    for f in os.listdir(TEMP_DIR):
        try:
            os.remove(os.path.join(TEMP_DIR, f))
        except:
            pass
