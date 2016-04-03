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
    filePath = train_image_dir + fileName
    try:
        numpy.asarray(Image.open(filePath)).transpose(2, 0, 1)
    except:
        print "broken file"
        os.remove(filePath)
        continue
    wnid = fileName[:fileName.index("_")]
    print "wnid:%s" % wnid
    if wnid in targets:
        print "find target!:%s" % fileName
        classIdx = targets.index(wnid)
        f.write((train_image_dir + "%s %d") % (fileName, classIdx) + "\n")
f.close()
# ---------------------------------------------------