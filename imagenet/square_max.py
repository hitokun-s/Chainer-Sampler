#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PIL import Image

for i, imgpath in enumerate(os.listdir("images")):
    if not imgpath.endswith(".jpg"):
        print "not image file!:%s" % imgpath
        continue
    print i
    img = Image.open("images/" + imgpath)
    size = min(img.size) # img.size は、(width, height)というタプルを返す。PILのバージョンによっては、img.width, img.heightも使えるが。
    start_x = img.size[0] / 2 - size / 2
    start_y = img.size[1] / 2 - size / 2
    box = (start_x, start_y, start_x + size, start_y + size) #  box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
    img2 = img.crop(box).resize((256, 256), Image.ANTIALIAS)
    img2.save('images/' + imgpath, 'JPEG')