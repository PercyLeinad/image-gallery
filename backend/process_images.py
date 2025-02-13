import os

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

IMAGE_DIR = "static/images/full"
THUMB_DIR = "static/images/thumbnails"
HD_DIR = "static/images/hd1080"

os.makedirs(THUMB_DIR, exist_ok=True)
os.makedirs(HD_DIR, exist_ok=True)

for image_name in os.listdir(IMAGE_DIR):
    image_path = os.path.join(IMAGE_DIR, image_name)
    img = Image.open(image_path)

    # Create Thumbnail
    thumb = img.copy()
    thumb.thumbnail((20, 20))
    thumb.save(os.path.join(THUMB_DIR, image_name))

    # Create 1080p version
    hd = img.copy()
    hd.thumbnail((1920, 1080))
    hd.save(os.path.join(HD_DIR, image_name))

print("Images processed successfully.")
