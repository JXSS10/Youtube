import os
import aiohttp
import asyncio
from pathlib import Path

# تأكد أن مجلد temp موجود
Path("temp").mkdir(parents=True, exist_ok=True)

async def download_video(url: str) -> str:
    """
    تحمل الفيديو من رابط URL وتحفظه في مجلد temp
    """
    filename = f"{hash(url)}.mp4"  # اسم فريد لكل رابط
    filepath = os.path.join("temp", filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to download, status {resp.status}")
            data = await resp.read()
            with open(filepath, "wb") as f:
                f.write(data)

    return filepath

async def clear_temp_files():
    """
    تنظيف ملفات temp الأقدم من ساعة واحدة
    """
    now = asyncio.get_event_loop().time()
    for file in os.listdir("temp"):
        path = os.path.join("temp", file)
        if os.path.isfile(path):
            # حذف الملفات الأكبر من 3600 ثانية (ساعة)
            if now - os.path.getmtime(path) > 3600:
                os.remove(path)
