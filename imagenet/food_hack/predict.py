#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import datetime
import json
import multiprocessing
import os
import random
import sys
import threading
import time

import numpy as np
from PIL import Image
import six
import six.moves.cPickle as pickle
from six.moves import queue
import chainer
from chainer import computational_graph
from chainer import cuda
from chainer import optimizers
from chainer import serializers

#Chainer Specific
from chainer import Variable, optimizers, serializers
import chainer.functions as F

parser = argparse.ArgumentParser()
parser.add_argument('--gpu', '-g', default=0, type=int)

args = parser.parse_args()
use_gpu = args.gpu >= 0
if use_gpu:
    cuda.check_cuda_available()
    xp = cuda.cupy
    cuda.get_device(args.gpu).use()
else:
    xp = np

def mnist_predict(x, model):
    x = Variable(x)
    # output = mnist_forward(x, model)
    return np.argmax(model.predictor(x).data,1)

import nin
model = nin.NIN()

if args.gpu >= 0:
    cuda.get_device(args.gpu).use()
    model.to_gpu()

# Setup optimizer
optimizer = optimizers.MomentumSGD(lr=0.01, momentum=0.9)
optimizer.setup(model)

serializers.load_npz(os.path.join(os.path.dirname(__file__), 'model'), model)
serializers.load_npz(os.path.join(os.path.dirname(__file__), 'state'), optimizer)


mean_image = pickle.load(open("mean.npy", 'rb'))
cropwidth = 256 - model.insize


def read_image_data(ndArrData, center=False, flip=False):
    image = ndArrData.transpose(2, 0, 1)
    if center:
        top = left = cropwidth / 2
    else:
        top = random.randint(0, cropwidth - 1)
        left = random.randint(0, cropwidth - 1)
    bottom = model.insize + top
    right = model.insize + left

    image = image[:, top:bottom, left:right].astype(np.float32)
    image -= mean_image[:, top:bottom, left:right]
    image /= 255
    if flip and random.randint(0, 1) == 0:
        return image[:, :, ::-1]
    else:
        return image

def read_image(path, center=False, flip=False):
    read_image_data(np.asarray(Image.open(path)), center, flip)

def predict_core(img):
    x_batch = np.ndarray((1, 3, model.insize, model.insize), dtype=np.float32)
    x_batch[0] = img
    volatile = 'on'
    x = chainer.Variable(xp.asarray(x_batch), volatile=volatile)
    t1 = chainer.Variable(xp.asarray([0]).astype(np.int32), volatile=volatile)
    t2 = chainer.Variable(xp.asarray([1]).astype(np.int32), volatile=volatile)
    t3 = chainer.Variable(xp.asarray([2]).astype(np.int32), volatile=volatile)

    # print(model.predictor(x).data)
    print(model(x,t1).data)
    print(model(x,t2).data)
    print(model(x,t3).data)

def predict_by_data(ndArrData):
    return predict_core(read_image_data(ndArrData, False, True))

def predict(file_path):
    return predict_core(read_image(file_path, False, True))

if __name__ == '__main__':

    predict("data/bbox_image/n07735510_322_box1.JPEG") # 0
    print("----------")
    predict("data/bbox_image/n07747607_693_box3.JPEG") # 2
    print("----------")
    predict("data/bbox_image/n07734017_391_box2.JPEG") # 1
    print("----------")
    predict("data/bbox_image/n07747607_631_box2.JPEG") # 2
    print("----------")

