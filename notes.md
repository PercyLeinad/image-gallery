# am aiming to create an image gallery

### Gallery features:

- Thumbnails <for lazyloading>
- Light/modal view <view 1080p image>
- Image captioning
- Image downloading <download the full size image>

note: create 3 sets of images Thumbnails,1080,full image

## Requirements (open to use the below)

- python : flask, jinja
- javascript
- html & css
## Project structure

/flask_image_gallery
│── app.py # Main Flask app
│── config.py # Configuration settings (optional)
│── static/
│ ├── images/ # Store original & processed images
│ │ ├── full/ # Full-size images
│ │ ├── 1080p/ # 1080p images
│ │ ├── thumbnails/ # Thumbnail images
│ ├── css/
│ │ ├── styles.css # Custom styling
│ ├── js/
│ │ ├── scripts.js # JavaScript for lazy loading & modal
│── templates/
│ ├── index.html # Gallery homepage
│── process_images.py # Script to generate thumbnails & 1080p images
│── requirements.txt # Python dependencies
│── README.md # Documentation
