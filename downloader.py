import os
import asyncio
import aiohttp

# مجلد مؤقت للملفات
TEMP_DIR = "/tmp"

async def download_video(url: str) -> str:
    """
    تحميل الفيديو من رابط وحفظه في TEMP_DIR
    """
    filename = url.split("/")[-1]  # اسم الملف من الرابط
    filepath = os.path.join(TEMP_DIR, filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                content = await resp.read()
                with open(filepath, "wb") as f:
                    f.write(content)
                return filepath
            else:
                raise Exception(f"Failed to download video. Status code: {resp.status}")

async def clear_temp_files():
    """
    مسح كل الملفات في TEMP_DIR
    """
    for filename in os.listdir(TEMP_DIR):
        path = os.path.join(TEMP_DIR, filename)
        try:
            os.remove(path)
        except Exception:
            pass
