#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import matplotlib.pyplot as plt
import numpy as np
from tool.auto_binarizer import *

def ccc(name):
    if name.lower() == 'windows-31j':
        return codecs.lookup('utf-8')
codecs.register(ccc)

arrA = np.load("parsed/12_C.npy")

from PIL import Image


def pilToNumPy(pilImg):
    imgArray = np.asarray(pilImg)
    imgArray.flags.writeable = True
    return imgArray

def numPyToPIL(imgArr):
    return Image.fromarray(np.uint8(imgArr))

def toGrayScale(pilImg):
    return pilImg.convert("L")

tgt = arrA[3]

grayed = pilToNumPy(toGrayScale(numPyToPIL(tgt)))
print grayed

plt.imshow( grayed , interpolation='none' )
plt.gray()
plt.savefig("grayscale.png")
plt.clf()

grayed = binarize(grayed)

print grayed
plt.imshow( grayed , interpolation='none' )
plt.gray()
plt.savefig("grayed.png")

