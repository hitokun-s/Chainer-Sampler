# -*- coding: utf-8 -*-
import skimage.data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import numpy as np
from PIL import Image
from skimage import io
import os

def main():

    # loading lena image
    img = skimage.data.chelsea() # => numpy.ndarray
    print img[0][0]

    # 書きの方法はダメ！ネガポジ画像になってしまう。
    # img = Image.open("images/fruit.jpg")
    # img.load()
    # img = np.asarray( img, dtype="int32" )

    # 参考：http://www.scipy-lectures.org/packages/scikit-image/
    img = io.imread('images/fruit.jpg')

    print img[0][0]

    # perform selective search
    img_lbl, regions = selectivesearch.selective_search(
            img, scale=500, sigma=0.9, min_size=10)

    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        if r['size'] < 2000:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 1.2 or h / w > 1.2:
            continue
        candidates.add(r['rect'])

    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    for x, y, w, h in candidates:
        print x, y, w, h
        rect = mpatches.Rectangle(
                (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    plt.show()

if __name__ == "__main__":
    main()