#!/bin/env python

from PIL import Image, UnidentifiedImageError
from os import listdir
from os.path import isfile, isdir
from random import choice
import argparse

parser = argparse.ArgumentParser(description="Choose what image to display")
parser.add_argument("path", type=str, default="./", nargs="?", help="select image or folder to get image from")
args = parser.parse_args()

file = args.path

if (isfile(file)):
    pass
elif (isdir(file)):
    potential = [elem for elem in listdir(file) if elem.endswith(".png")]
    if (potential):
        file = file+"/"*(1-file.endswith("/"))+choice(potential)
    else:
        print(f"No png files found in directory '{file}'")
        exit()
else:
    print("invalid path")
    exit()
try:
    im = Image.open(file)
except UnidentifiedImageError:
    print("invalid image file")
    exit()
pix = im.load()
width, height = im.size
skip = True
prev = 0
for y in range(height):
    if ([1 for i in [pix[i, y] for i in range(width)] if i[3]]):
        skip = False
    if (not skip):
        for x in range(width):
            color = [str(c) for c in pix[x, y]]
            if (color == prev):
                print("  ", end="")
            elif (color[3] != "0"):
                print("\N{ESCAPE}[48;2;" + color[0] + ";" + color[1] + ";" + color[2] + "m  ", end="")
            else:
                print("\u001b[0m  ", end="")
            prev = color
        prev = 0;
        print("\u001b[0m")
