from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from downloader import download_video, clear_temp_files
import asyncio
import os
from pathlib import Path

app = FastAPI()

# تنظيف temp كل 10 دقائق
async def periodic_cleanup():
    while True:
        await asyncio.sleep(600)  # 10 دقائق
        await clear_temp_files()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_cleanup())

# واجهة الموقع
@app.get("/", response_class=HTMLResponse)
async def home():
    index_path = Path("static/index.html")
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return "<h1>Index file not found</h1>"

# API لبدء التحميل
@app.post("/api/download")
async def api_download(url: str = Form(...)):
    try:
        filepath = await download_video(url)
        filename = os.path.basename(filepath)
        return {"status": "ok", "download_url": f"/temp/{filename}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# تقديم ملفات temp
@app.get("/temp/{filename}")
async def get_temp_file(filename: str):
    path = os.path.join("temp", filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="video/mp4", filename=filename)
    return {"status": "error", "message": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
