#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

import codecs


def ccc(name):
    if name.lower() == 'windows-31j':
        return codecs.lookup('utf-8')


codecs.register(ccc)


def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], scipy.io.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict


def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, scipy.io.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


res = loadmat("Lists/English/Img/lists.mat")["list"]
for k in res:
    print k
print res["ALLlabels"]
print len(res["ALLlabels"])  # => 12503
print len(res["ALLnames"])  # => 12503
print len(res["classlabels"])  # => 62
print res["classlabels"]  # => [ 1  2  3  4  ... 61  62 ] （例えば、11 : 'A' という対応。）
print len(res["classnames"])  # => 62
print res["classnames"]  # => 例えば'A'の名前は、'GoodImg/Bmp/Sample011'

# check content
import os

labels = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
assert len(labels) == 62
assert len(res["classnames"]) == 62

data = {}

for i, dirName in enumerate(res["classnames"]):
    dir = 'data/English/Img/' + dirName
    fileNames = os.listdir(dir)
    fileCount = len([name for name in fileNames if os.path.isfile(os.path.join(dir, name))])

    print "i:%d,dir:%s,file count:%d" % (i, dir, fileCount)

    images = [plt.imread('data/English/Img/' + dirName + '/' + name, 'bmp') for name in fileNames]
    np.save('parsed/%d_%s.npy' % (i, labels[i]), np.array(images))

    print "label:%s, fileCount:%d" % (labels[i], fileCount)
