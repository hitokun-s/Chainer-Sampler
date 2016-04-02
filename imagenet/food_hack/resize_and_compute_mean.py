#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import numpy
from PIL import Image
import six.moves.cPickle as pickle

train_image_dir = "data/bbox_image/"

# ---------------------------------------------------
# create train.txt
import targets
targets = targets.getTargets()
if os.path.exists("train.txt"):
    os.remove("train.txt")
f = open("train.txt","w")
for fileName in os.listdir(train_image_dir):
    wnid = fileName[:fileName.index("_")]
    print "wnid:%s" % wnid
    if wnid in targets:
        print "find target!:%s" % fileName
        classIdx = targets.index(wnid)
        f.write((train_image_dir + "%s %d") % (fileName, classIdx) + "\n")
f.close()
# ---------------------------------------------------

# ---------------------------------------------------
# resize
print "====================================="
print "start resize!"
print "====================================="
for i, imgpath in enumerate(os.listdir(train_image_dir)):
    if not imgpath.endswith(".jpg") and not imgpath.endswith(".JPEG"):
        print "not image file!:%s" % imgpath
        continue
    print i
    img = Image.open(train_image_dir + imgpath)
    size = min(img.size) # img.size は、(width, height)というタプルを返す。PILのバージョンによっては、img.width, img.heightも使えるが。
    start_x = img.size[0] / 2 - size / 2
    start_y = img.size[1] / 2 - size / 2
    box = (start_x, start_y, start_x + size, start_y + size) #  box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
    img2 = img.crop(box).resize((256, 256), Image.ANTIALIAS)
    img2.save(train_image_dir + imgpath, 'JPEG')

# -----------------------------------------------------

print "====================================="
print "start compute mean!"
print "====================================="

parser = argparse.ArgumentParser(description='Compute images mean array')
parser.add_argument('--dataset', '-d', help='Path to training image-label list file',  default='train.txt')
parser.add_argument('--root', '-r', default='.',
                    help='Root directory path of image files')
parser.add_argument('--output', '-o', default='mean.npy',
                    help='path to output mean array')
args = parser.parse_args()

sum_image = None
count = 0
for i, line in enumerate(open(args.dataset)):
    filepath = os.path.join(args.root, line.strip().split()[0])
    if not imgpath.endswith(".jpg") and not imgpath.endswith(".JPEG"):
        print "not jpg file. skip..."
        continue
    try:
        image = numpy.asarray(Image.open(filepath)).transpose(2, 0, 1)
    except:
        print "idx:%d" % i
        print "file:%s" % filepath
        print sys.exc_info()[0]
        continue

    if sum_image is None:
        sum_image = numpy.ndarray(image.shape, dtype=numpy.float32)
        sum_image[:] = image
    else:
        # ここで、operands could not be broadcast together with shapes エラーになった
        # broadcast ... サイズ/形状の異なる配列同士の演算のこと
        sum_image += image
    count += 1
    # sys.stderr.write('\r{}'.format(count))
    # sys.stderr.flush()

sys.stderr.write('\n')

mean = sum_image / count
pickle.dump(mean, open(args.output, 'wb'), -1)
