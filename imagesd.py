#!/usr/bin/env python3

import argparse
import requests
import subprocess

from io import BytesIO
from PIL import Image
from inky.auto import auto
from gpiozero import Button

url = "http://192.168.1.4/py/pics3.cgi"
BUTTON_PIN = 5
TIMEOUT = 30  # seconds

parser = argparse.ArgumentParser()

parser.add_argument("--saturation", "-s", type=float, default=0.5, help="Colour palette saturation")

inky = auto()

args, _ = parser.parse_known_args()

response = requests.get(url)
img = Image.open(BytesIO(response.content))

img.save("/home/jamie/inky/examples/spectra6/image.jpg")
resizedimage = img.resize(inky.resolution)

try:
    inky.set_image(resizedimage, saturation=args.saturation)
except TypeError:
    inky.set_image(resizedimage)

inky.show()

print("Waiting for button press...")

button = Button(BUTTON_PIN) 

if button.wait_for_press(timeout=TIMEOUT):
    print("Button was pressed!")
    exit(0)

print("No button press, shutting down")
subprocess.run(["sudo", "shutdown", "-h", "now"])

