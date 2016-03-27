#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

for imgpath in os.listdir("images"):
    img = Image.open("images/" + imgpath)
    size = min(img.height, img.width)
    start_x = img.width / 2 - size / 2
    start_y = img.height / 2 - size / 2
    box = (start_x, start_y, start_x + size, start_y + size) #  box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
    img2 = img.crop(box)
    img2.resize((256, 256), Image.ANTIALIAS)
    img2.save('images/' + imgpath, 'JPEG')