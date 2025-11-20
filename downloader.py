from yt_dlp import YoutubeDL

def extract_video(url: str):
    """
    Extract video info & formats using yt-dlp
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = {}
    for f in info.get("formats", []):
        if f.get("url"):
            q = f.get("height") or f.get("resolution") or "unknown"
            formats[f"{q}p"] = f["url"]

    return {
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "formats": formats
    }
