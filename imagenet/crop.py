#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def pilToNumPy(pilImg):
    imgArray = np.asarray(pilImg)
    imgArray.flags.writeable = True
    return imgArray

def numPyToPIL(imgArr):
    return Image.fromarray(np.uint8(imgArr))

parser = argparse.ArgumentParser()
parser.add_argument("source_dir")
parser.add_argument("target_dir")
args = parser.parse_args()

target_shape = (256, 256)

for source_imgpath in os.listdir(args.source_dir):
    print source_imgpath
    # src = cv2.imread(args.source_dir+"/"+source_imgpath)
    src = plt.imread(args.source_dir+"/"+source_imgpath) # 戻り値はRGB配列の二次元配列（ndarray, cv2と同じ）
    # mirror image
    while src.shape[0] < target_shape[0] or src.shape[1] < target_shape[1]:
        print src.shape
        src = np.concatenate((np.fliplr(src), src), axis=1)
        src = np.concatenate((np.flipud(src), src), axis=0)
    src = src[:target_shape[0], :target_shape[1]]
    print src.shape
    # cv2.imwrite(args.target_dir+"/"+source_imgpath, src)
    numPyToPIL(src).save(args.target_dir+"/"+source_imgpath)