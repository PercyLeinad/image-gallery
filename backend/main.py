from pathlib import Path
from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import re
import random

app = FastAPI()

# Define base paths
BACKEND_DIR = Path(__file__).resolve().parent  # backend/
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"

# Mount static files
app.mount("/backend", StaticFiles(directory=BACKEND_DIR), name="backend")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.mount("/static", StaticFiles(directory=BACKEND_DIR / "static"), name="static")

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define directories
BASE_DIR = Path('static/photos')
THUMB_DIR = BASE_DIR / "thumbnails"
HD_DIR = BASE_DIR / "hd"
FULL_DIR = BASE_DIR / "original"

def check(i):
    return bool(re.search(r'^Caption',i))
# Load images from the full directory
image_data = []
for image in FULL_DIR.glob("*.jpg"):
    file_name = re.search(r"(.*)\.jpg|", image.name).group(1)  # Allow any number of digits
    caption = ''
    if check(file_name):
        caption = file_name
    else:
        new_name = re.findall(r'[A-Z][a-z]+',file_name)
        caption = ' '.join(new_name)

    if file_name:
        image_id = file_name
        image_data.append({
            "id": image_id,
            "caption": caption,
            "urls": {
                "original": f"/{FULL_DIR}/{file_name}.jpg",
                "thumb": f"/{THUMB_DIR}/{file_name}.webp",
                "hd": f"/{HD_DIR}/{file_name}.webp",
            },
        })
random.shuffle(image_data)
# Initialize Jinja2 templates
templates = Jinja2Templates(directory=FRONTEND_DIR / "templates")

@app.get("/")
async def home(request: Request,
    page: int = Query(1, alias="page", ge=1),
    per_page: int = Query(20, alias="per_page", ge=1)  # No max limit in Query
):
    """Fetch paginated image data from the gallery API."""
    
    # Reset per_page to 20 if it exceeds the limit
    per_page = min(per_page, 20)

    total = len(image_data)
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    start = (page - 1) * per_page
    end = start + per_page
    results = image_data[start:end]
    """Render the homepage with a gallery of images."""
    return templates.TemplateResponse("index.html", {"request": request,                                        
        "page":page , 
        "total": total,
        "total_pages": total_pages,
        "per_page": per_page,
        "results": results
        }
    )

# API
@app.get("/api/")
async def get_gallery_api(
    page: int = Query(1, alias="page", ge=1),
    per_page: int = Query(20, alias="per_page", ge=1)  # No max limit in Query
):
    """Fetch paginated image data from the gallery API."""
    
    # Reset per_page to 20 if it exceeds the limit
    per_page = min(per_page, 20)

    total = len(image_data)
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    start = (page - 1) * per_page
    end = start + per_page
    results = image_data[start:end]

    return {
        "total": total,
        "total_pages": total_pages,
        "per_page": per_page,
        "results": results,
    }

