#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import numpy
from PIL import Image
import six.moves.cPickle as pickle

train_image_dir = "images/"


# ---------------------------------------------------
# resize
print "====================================="
print "start resize!"
print "====================================="
for i, imgpath in enumerate(os.listdir(train_image_dir)):
    exts = [".jpg" , ".png"]
    ext = os.path.splitext(imgpath)[1].lower()
    if not ext in exts:
        print "not image file!:%s" % imgpath
        continue
    print i
    img = Image.open(train_image_dir + imgpath)
    size = min(img.size) # img.size は、(width, height)というタプルを返す。PILのバージョンによっては、img.width, img.heightも使えるが。
    start_x = img.size[0] / 2 - size / 2
    start_y = img.size[1] / 2 - size / 2
    box = (start_x, start_y, start_x + size, start_y + size) #  box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
    img2 = img.crop(box).resize((96, 96), Image.ANTIALIAS)
    img2.save("images/" + imgpath, 'png')

# -----------------------------------------------------
