#!/usr/bin/env python
# -*- coding: utf-8 -*-

# test.txt, train.txt のファイルからエラーファイルのデータを消す

import argparse
import os
import sys

import numpy
from PIL import Image
import six.moves.cPickle as pickle

def filter(file_name):
    new_file = open('tmp.txt', 'w') # 書き込みモードで開く

    for i, line in enumerate(open(file_name)):
        # line == "images/hoge.jpg" という想定
        filepath = line.strip().split()[0]
        if not filepath.endswith(".jpg"):
            print "not jpg file. skip..."
            os.remove(filepath)
            continue
        try:
            numpy.asarray(Image.open(filepath)).transpose(2, 0, 1)
            new_file.write(line) # 引数の文字列をファイルに書き込む
        except:
            print "idx:%d" % i
            print "file:%s" % filepath
            os.remove(filepath)
    new_file.close() # ファイルを閉じる
    os.remove(file_name) # 元のファイルを消して
    os.rename('tmp.txt', file_name) # 変名

filter("train.txt")
filter("test.txt")