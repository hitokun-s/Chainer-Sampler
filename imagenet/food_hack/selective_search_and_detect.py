# -*- coding: utf-8 -*-
import skimage.data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import numpy as np
from PIL import Image
from skimage import io
import os
import predict

# arg: cropped PIL.Image object
def resize_and_predict(img):
    size = min(img.size) # img.size は、(width, height)というタプルを返す。PILのバージョンによっては、img.width, img.heightも使えるが。
    start_x = img.size[0] / 2 - size / 2
    start_y = img.size[1] / 2 - size / 2
    box = (start_x, start_y, start_x + size, start_y + size) #  box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
    img = img.crop(box).resize((256, 256), Image.ANTIALIAS)
    predict.read_image_data(np.asarray(img))

def main():

    # loading lena image
    # img = skimage.data.chelsea() # => numpy.ndarray
    # print img[0][0]

    # 書きの方法はダメ！ネガポジ画像になってしまう。
    # img = Image.open("images/fruit.jpg")
    # img.load()
    # img = np.asarray( img, dtype="int32" )

    # predictでは、data/bbox_image/n07747607_631_box2.JPEGは正解できた。
    # ということは、n07747607_631.jpg でselective search すると正解できるかも？
    tgt_img_path = "data/image/n07747607_631.jpg"
    img = io.imread(tgt_img_path)

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

    img = Image.open(tgt_img_path)
    for rect in candidates:
        resize_and_predict(img.crop(rect))

    # fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    # ax.imshow(img)
    # for x, y, w, h in candidates:
    #     print x, y, w, h
    #     rect = mpatches.Rectangle(
    #             (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
    #     ax.add_patch(rect)
    # plt.show()

if __name__ == "__main__":
    main()