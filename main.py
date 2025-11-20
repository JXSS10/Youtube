from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from downloader import ytdlp_download
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/")
async def home():
    return FileResponse("static/index.html")


# --------------------------------------------------------------------
# ▶ 1) VK Downloader
# --------------------------------------------------------------------
@app.get("/api/vk")
async def vk_downloader(url: str = Query(...)):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return JSONResponse({"error": "Failed to fetch VK page"}, status_code=400)

        soup = BeautifulSoup(r.text, "html.parser")
        scripts = soup.find_all("script")

        links = {}

        for s in scripts:
            txt = s.text
            if "url1080" in txt:
                def grab(label):
                    if label in txt:
                        return txt.split(label + '":"')[1].split('"')[0].replace("\\", "")
                links["1080p"] = grab("url1080")
                links["720p"]  = grab("url720")
                links["480p"]  = grab("url480")
                links["360p"]  = grab("url360")
                links["240p"]  = grab("url240")

        clean = {k: v for k, v in links.items() if v}

        if not clean:
            return JSONResponse({"error": "No VK video URLs found"}, status_code=404)

        return {"status": "ok", "links": clean}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# --------------------------------------------------------------------
# ▶ 2) Generic Downloader via yt-dlp
# --------------------------------------------------------------------
@app.get("/api/ytdlp")
async def api_ytdlp(url: str = Query(...)):
    try:
        data = ytdlp_download(url)
        return {"status": "ok", "data": data}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
