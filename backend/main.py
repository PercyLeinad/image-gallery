from pathlib import Path
from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Define base paths
BASE_DIR = Path(__file__).resolve().parent  # backend/
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define directories
BASE_DIR = Path("static/images")
THUMB_DIR = BASE_DIR / "thumbnails"
HD_DIR = BASE_DIR / "hd1080"
FULL_DIR = BASE_DIR / "full"

# Ensure directories exist
FULL_DIR.mkdir(parents=True, exist_ok=True)
THUMB_DIR.mkdir(parents=True, exist_ok=True)
HD_DIR.mkdir(parents=True, exist_ok=True)

# Load images from the full directory
image_data = []
for image in FULL_DIR.glob("*.jpg"):
    match = re.search(r"(\d+)\.jpg", image.name)  # Allow any number of digits
    if match:
        image_id = match.group(1)
        image_data.append({
            "id": image_id,
            "urls": {
                "full": f"/{FULL_DIR}/{image.name}",
                "thumb": f"/{THUMB_DIR}/{image.name}",
                "fhd": f"/{HD_DIR}/{image.name}",
            },
        })

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=FRONTEND_DIR / "templates")

@app.get("/")
async def home(request: Request,
    page: int = Query(1, alias="page", ge=1),
    per_page: int = Query(24, alias="per_page", ge=1)  # No max limit in Query
):
    """Fetch paginated image data from the gallery API."""
    
    # Reset per_page to 20 if it exceeds the limit
    per_page = min(per_page, 24)

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
        "results": [{"id": img["id"], "urls": img["urls"]} for img in results],
        }
    )


@app.get("/api/")
async def get_gallery_api(
    page: int = Query(1, alias="page", ge=1),
    per_page: int = Query(24, alias="per_page", ge=1)  # No max limit in Query
):
    """Fetch paginated image data from the gallery API."""
    
    # Reset per_page to 20 if it exceeds the limit
    per_page = min(per_page, 24)

    total = len(image_data)
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    start = (page - 1) * per_page
    end = start + per_page
    results = image_data[start:end]

    return {
        "total": total,
        "total_pages": total_pages,
        "per_page": per_page,
        "results": [{"id": img["id"], "urls": img["urls"]} for img in results],
    }

