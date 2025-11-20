import os
import re
import threading
from yt_dlp import YoutubeDL

TEMP_DIR = "/tmp"  # المسار المسموح في Railway

def safe_filename(title):
    # إزالة الأحرف الغير آمنة
    title = re.sub(r'[^\w\-_. ]', '', title)
    title = title.strip()
    if len(title) > 100:
        title = title[:100]
    return title + ".mp4"

def delete_file_later(path, delay=240):
    def _delete():
        try:
            threading.Event().wait(delay)
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
    threading.Thread(target=_delete).start()

def download_video(url):
    # استخراج info للحصول على العنوان
    with YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "video")

    filename = os.path.join(TEMP_DIR, safe_filename(title))

    ydl_opts = {
        "outtmpl": filename,
        "quiet": True,
        "no_warnings": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    delete_file_later(filename)  # مسح بعد 4 دقائق
    return filename
