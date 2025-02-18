#!/bin/bash
cd "$(dirname "$PWD")/backend/static/photos"
# Define directories
SOURCE_DIR="original/"
DEST_DIR="$(pwd)"

# Create destination folders if they don't exist
mkdir -p "$DEST_DIR/original" "$DEST_DIR/hd" "$DEST_DIR/thumbnails"

# Process images using Python
python3 - <<EOF
import subprocess
from pathlib import Path
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define directories
SOURCE_DIR = Path("original/")
DEST_DIR = Path(".")

# Create necessary directories
(DEST_DIR / "original").mkdir(parents=True, exist_ok=True)
(DEST_DIR / "hd").mkdir(parents=True, exist_ok=True)
(DEST_DIR / "thumbnails").mkdir(parents=True, exist_ok=True)


# Function to process images
def process_image(image_path):
    try:
        with Image.open(image_path) as img:
            filename = image_path.stem  # Get filename without extension

            # Save original copy
            img.save(DEST_DIR / "original" / f"{filename}.jpg", "JPEG")

            # Create 720p HD image
            hd_img = img.copy()
            hd_img.thumbnail((hd_img.width, 720))  # Maintain aspect ratio
            hd_jpg_path = DEST_DIR / "hd" / f"{filename}.jpg"
            hd_img.save(hd_jpg_path, "JPEG")

            # Create Thumbnail (200px width, auto height)
            thumb_img = img.copy()
            thumb_img.thumbnail((200, thumb_img.height))  # Maintain aspect ratio
            thumb_jpg_path = DEST_DIR / "thumbnails" / f"{filename}.jpg"
            thumb_img.save(thumb_jpg_path, "JPEG")

            print(f"Processed: {filename}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Process all JPG images in the source directory
for image_file in SOURCE_DIR.glob("*.jpg"):
    process_image(image_file)

print("Processing complete!")
EOF

# Loop through all .jpg files in the source directory
for file in "$SOURCE_DIR"/*.jpg; do
    # Check if the file exists
    if [ -f "$file" ]; then
        # Extract filename
        filename=$(basename "$file")
        filename_without_ext="${filename%.*}"

        # Move the original file
        cp "$file" "$DEST_DIR/original/$filename"

        # Convert HD image to WebP
        cwebp "$DEST_DIR/hd/${filename_without_ext}.jpg" -o "$DEST_DIR/hd/${filename_without_ext}.webp"

        # Convert thumbnail to WebP
        cwebp "$DEST_DIR/thumbnails/${filename_without_ext}.jpg" -o "$DEST_DIR/thumbnails/${filename_without_ext}.webp"

        # Remove JPG files from HD and thumbnails folders
        rm "$DEST_DIR/hd/${filename_without_ext}.jpg"
        rm "$DEST_DIR/thumbnails/${filename_without_ext}.jpg"
    fi
done

echo 'Done'
