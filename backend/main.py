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
BASE_DIR = Path('static/images')
THUMB_DIR = BASE_DIR / "thumbnails"
HD_DIR = BASE_DIR / "hd1080"
FULL_DIR = BASE_DIR / "full"



# Load images from the full directory
image_data = []
for image in FULL_DIR.glob("*.jpg"):
    match = re.search(r"(.*)\.jpg", image.name)  # Allow any number of digits
    if match:
        image_id = match.group(1)
        image_data.append({
            "id": image_id,
            "caption": image_id,
            "urls": {
                "full": f"/{FULL_DIR}/{image.name}",
                "thumb": f"/{THUMB_DIR}/{image.name}",
                "fhd": f"/{HD_DIR}/{image.name}",
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
###############################
def check(i):
    return bool(re.search(r'^Caption',i))

@app.get("/photo/{image_id}")
async def view_image(request: Request, image_id):
    """Render image_view.html with a masked URL."""
    image_url = f"/backend/static/images/full/{image_id}.jpg"  # Masked URL (no direct static path)
    
    caption = ''
    if check(image_id):
        caption = image_id
    else:
        new_name = re.findall(r'[A-Z][a-z]+',image_id)
        caption = ' '.join(new_name)
    return templates.TemplateResponse("image_view.html", {
        "caption":caption,
        "request": request,
        "image_url": image_url,
    })


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

