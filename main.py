from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Mount static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Directories
IMAGE_DIR = "static/images"
THUMB_DIR = os.path.join(IMAGE_DIR, "thumbnails")
HD_DIR = os.path.join(IMAGE_DIR, "hd1080")
FULL_DIR = os.path.join(IMAGE_DIR, "full")

@app.get("/", response_class=HTMLResponse)
async def gallery(request: Request):
    images = os.listdir(FULL_DIR)  # List all full-size images
    return templates.TemplateResponse("index.html", {"request": request, "images": images})

@app.get("/image/{size}/{filename}")
async def get_image(size: str, filename: str):
    """Serve images based on requested size (thumbnail, 1080p, full)."""
    if size == "thumbnail":
        return StaticFiles(directory=THUMB_DIR).lookup_path(filename)
    elif size == "hd1080":
        return StaticFiles(directory=HD_DIR).lookup_path(filename)
    elif size == "full":
        return StaticFiles(directory=FULL_DIR).lookup_path(filename)
    return {"error": "Invalid size"}
