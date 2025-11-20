from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from downloader import extract_video

app = FastAPI()

# واجهة الموقع
@app.get("/")
async def home():
    return FileResponse("static/index.html")

# API عام لأي رابط yt-dlp (YouTube / VK / وغيرها)
@app.get("/api/download")
async def download(url: str = Query(...)):
    try:
        data = extract_video(url)
        if not data["formats"]:
            return JSONResponse({"error": "No downloadable links found"}, status_code=404)
        return {"status": "ok", "data": data}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
