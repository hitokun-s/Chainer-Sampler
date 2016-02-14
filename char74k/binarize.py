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

# 中心から最大サイズの正方形を切り出して、所定サイズに変形
def standardize(pilImg):
    width, height = pilImg.size
    # ex. crop((left, top, right, bottom)) => crop((450, 516, 1011, 872))
    target_size = width if width < height else height
    left = width / 2 - target_size / 2
    right = width / 2 + target_size / 2
    top = height / 2 - target_size / 2
    bottom = height / 2 + target_size / 2
    if right >= width:
        right = width - 1
    if bottom >= height:
        bottom = height - 1
    pilImg.crop((left, top, right, bottom))
    return pilImg.resize((50, 50))

# 白黒反転
def invert(binaryArr):
    f = np.vectorize(lambda x : 1 - x) # 全要素に作用する関数を作成（xは各要素の値）
    return f(binaryArr)

# 白黒反転すべきか
def should_invert(ndArr):
    assert ndArr.shape == (50,50)
    arr = []
    for i,v in np.ndenumerate(ndArr):
        if i[0] in [0,49] or i[1] in [0,49]:
            arr.append(v)
    arr = np.array(arr)
    # 外周要素の半数以上が１なら反転の必要がある
    return np.count_nonzero(arr) > arr.size / 2

fileNames = os.listdir("parsed")

for fileName in fileNames:
    print "let's go to " + fileName
    res = []
    images = np.load("parsed/" + fileName)
    for img in images:
        grayScaled = toGrayScale(numPyToPIL(img))
        standardized = standardize(grayScaled)
        grayed = pilToNumPy(standardized)
        grayed = binarize(grayed) # 戻り値はndarray
        if should_invert(grayed):
            grayed = invert(grayed)
        res.append(grayed)
    binarized = np.array(res)
    np.save("binarized/" + fileName, binarized)


