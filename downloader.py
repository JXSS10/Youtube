import yt_dlp

def ytdlp_download(url: str):
    """
    Extract video info & formats using yt-dlp
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # extract formats
    formats = {}
    for f in info.get("formats", []):
        if f.get("filesize") and f.get("url"):
            quality = f"{f.get('height', 'Unknown')}p"
            formats[quality] = f["url"]

    return {
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "formats": formats
    }
