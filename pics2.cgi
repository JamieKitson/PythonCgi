#!/usr/bin/env python
import os, random, cgi, sys

IMAGE_FOLDER = "/srv/http/192.168.1.4/resized/"

try:
    images = [f for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not images:
        print("Content-Type: text/plain\n")
        print("No images found")
        sys.exit(0)

    filename = random.choice(images)
    filepath = os.path.join(IMAGE_FOLDER, filename)

    print("Content-Type: image/jpeg\n")
    sys.stdout.flush()

    # Stream the file directly
    with open(filepath, "rb") as f:
        sys.stdout.buffer.write(f.read())

except Exception as e:
    print("Content-Type: text/plain\n")
    print(f"Error: {e}")

