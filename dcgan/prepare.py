#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from shutil import copyfile

image_dir = "images"
if not os.path.exists(image_dir):
    os.mkdir(image_dir)

data_dir = "../char74k/data/English/Fnt/"

dirNames = os.listdir(data_dir)
print dirNames

for dirName in dirNames:
    fileNames = os.listdir(data_dir + dirName)
    targets = [file for file in fileNames if file.endswith("-00005.png")]
    copyfile(data_dir + dirName + "/" + targets[0], "images/" + targets[0])

