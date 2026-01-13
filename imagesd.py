#!/usr/bin/env python3

import argparse
import pathlib
import sys
import requests

from io import BytesIO
from PIL import Image
from inky.auto import auto
from gpiozero import Button
from time import sleep, time

url = "http://192.168.1.4/py/pics3.cgi"
BUTTON_PIN = 5
TIMEOUT = 30  # seconds

parser = argparse.ArgumentParser()

parser.add_argument("--saturation", "-s", type=float, default=0.5, help="Colour palette saturation")

inky = auto(ask_user=True, verbose=True)

args, _ = parser.parse_known_args()

response = requests.get(url)
img = Image.open(BytesIO(response.content))
#image = Image.open(args.file)

img.save("image.jpg")
resizedimage = img.resize(inky.resolution)

try:
    inky.set_image(resizedimage, saturation=args.saturation)
except TypeError:
    inky.set_image(resizedimage)

inky.show()

button = Button(BUTTON_PIN, pull_up=True)

start = time()

print("Waiting for button press...")

while time() - start < TIMEOUT:
    if button.is_pressed:
        print("Button pressed!")
        # Do whatever you want here
        exit(0)
    sleep(0.05)

print("No button press, shutting down")
#subprocess.run(["sudo", "shutdown", "-h", "now"])

