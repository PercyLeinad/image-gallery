from pathlib import Path
import re

def check(i):
    return bool(re.search(r'^\d',i))

TARGET = Path.cwd() 
for image in TARGET.glob('*.jpg'):
    if check(image.name):
          Path.rename(image,'Caption'+' '+image.name)
    
