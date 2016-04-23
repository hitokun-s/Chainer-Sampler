#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from urllib2 import urlopen
from urllib import urlretrieve
from bs4 import BeautifulSoup
import sqlite3
import tarfile
import glob

def initDir(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.mkdir(dirname)

initDir("images")
initDir("tmp")

url = "http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/EnglishFnt.tgz"
urlretrieve(url, "tmp/EnglishFnt.tgz")
tf = tarfile.open("tmp/EnglishFnt.tgz", "r:gz")
tf.extractall("tmp")
tf.close()

for file in glob.glob('tmp/English/Fnt/**/*.png'):
    print file
    shutil.copy(file, "images")

