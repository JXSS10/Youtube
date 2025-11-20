from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from downloader import download_video, clear_temp_files
import asyncio
import os

app = FastAPI()

# تنظيف TEMP كل 4 دقائق
async def periodic_cleanup():
    while True:
        await asyncio.sleep(240)  # 4 دقائق
        await clear_temp_files()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_cleanup())

# واجهة الموقع
@app.get("/", response_class=HTMLResponse)
async def home():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
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

# تقديم ملفات TEMP
@app.get("/temp/{filename}")
async def get_temp_file(filename: str):
    path = os.path.join("/tmp", filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="video/mp4", filename=filename)
    return {"status": "error", "message": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
