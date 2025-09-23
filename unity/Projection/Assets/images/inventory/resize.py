from PIL import Image
import sys
import os

if len(sys.argv) < 2:
    print("Usage: drag_and_resize.py <image_file>")
    sys.exit(1)

image_file = sys.argv[1]

try:
    with Image.open(image_file) as img:
        resized_img = img.resize((100, 100))
        resized_img.save(image_file)
except Exception as e:
    print(f"Error: {e}")
