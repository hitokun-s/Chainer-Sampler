#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from shutil import copyfile

def createDirIfNotExist(dirname):
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)

image_dir = "images"
createDirIfNotExist(image_dir)
createDirIfNotExist("out_images")
createDirIfNotExist("out_models")


data_dir = "../char74k/data/English/Fnt/"

dirNames = os.listdir(data_dir)
print dirNames

for dirName in dirNames:
    fileNames = os.listdir(data_dir + dirName)
    targets = [file for file in fileNames if file.endswith("-00005.png")]
    copyfile(data_dir + dirName + "/" + targets[0], "images/" + targets[0])

print "You should exec multi_resize.bat/sh, please!"