#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs,os
import matplotlib.pyplot as plt
import numpy as np
from tool.auto_binarizer import *
from PIL import Image


def pilToNumPy(pilImg):
    imgArray = np.asarray(pilImg)
    imgArray.flags.writeable = True
    return imgArray

def numPyToPIL(imgArr):
    return Image.fromarray(np.uint8(imgArr))

def toGrayScale(pilImg):
    return pilImg.convert("L")

def invert(binaryArr):
    f = np.vectorize(lambda x : 1 - x)
    return f(binaryArr)

fileNames = os.listdir("parsed")

for fileName in fileNames:
    print "let's go to " + fileName
    res = []
    images = np.load("parsed/" + fileName)
    for img in images:
        grayed = pilToNumPy(toGrayScale(numPyToPIL(img)))
        grayed = binarize(grayed) # 戻り値はndarray
        if np.count_nonzero(grayed) < grayed.size / 2:
            grayed = invert(grayed)
        res.append(grayed)
    binarized = np.array(res)
    np.save("binarized/" + fileName, binarized)


