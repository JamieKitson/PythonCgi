#!/usr/bin/env python
import os, random, cgi, sys
from PIL import Image, ImageFilter
from io import BytesIO

IMAGE_FOLDER = "/srv/http/192.168.1.4/resized/"

def crop(img, target_w, target_h):

	w, h = img.size

	left = (w - target_w) // 2
	top = (h - target_h) // 2
	right = left + target_w
	bottom = top + target_h

	return img.crop((left, top, right, bottom))


try:
    images = [f for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not images:
        print("Content-Type: text/plain\n")
        print("No images found")
        sys.exit(0)

    filename = random.choice(images)
    filepath = os.path.join(IMAGE_FOLDER, filename)

    # Load image
    img = Image.open(filepath)
    w, h = img.size
    
    # for portraight pictures crop to a square and use width as height
    if h > w:
        img = crop(img, w, w)
        target_h = w
    else:
        target_h = h
        
    # Define target size of final image, 4:3
    target_w = int(4 * target_h / 3)

    # if image is < 4:3 add blurred sides
    if w / h < 4 / 3:
   
        # Create blurred background
        bg = img.resize((target_w, target_h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(50))

        # Paste original image centered
        bg.paste(img, ((target_w - w) // 2, 0))

        img = bg

    # if images is > 4:3 then crop top and bottom
    else:

        img = crop(img, target_w, target_h)

    # scale to desired size
    img = img.resize((1600, 1200), Image.LANCZOS)

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=95)
    buf.seek(0)

    sys.stdout.buffer.write(b"Content-Type: image/jpeg\n\n")    
    sys.stdout.flush()

    sys.stdout.buffer.write(buf.read())

except Exception as e:
    print("Content-Type: text/plain\n")
    print(f"Error: {e}")

