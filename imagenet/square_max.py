#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PIL import Image

for i, imgpath in enumerate(os.listdir("images")):
    print i
    img = Image.open("images/" + imgpath)
    size = min(img.height, img.width)
    start_x = img.width / 2 - size / 2
    start_y = img.height / 2 - size / 2
    box = (start_x, start_y, start_x + size, start_y + size) #  box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
    img2 = img.crop(box).resize((256, 256), Image.ANTIALIAS)
    img2.save('images/' + imgpath, 'JPEG')