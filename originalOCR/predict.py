#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse

import numpy as np
import six

import chainer
from chainer import computational_graph
from chainer import cuda
import chainer.links as L
from chainer import optimizers
from chainer import serializers

import numpy as np

#Chainer Specific
from chainer import FunctionSet, Variable, optimizers, serializers
import chainer.functions as F
import chainer.links as L

parser = argparse.ArgumentParser()
parser.add_argument('--gpu', '-g', default=-1, type=int)

args = parser.parse_args()
use_gpu = args.gpu >= 0
if use_gpu:
    cuda.check_cuda_available()
    xp = cuda.cupy
    cuda.get_device(args.gpu).use()
else:
    xp = np

def mnist_forward(data, model):

    out1 = model.l1(data)
    out2 = F.relu(out1)
    out3 = model.l2(out2)
    out4 = F.relu(out3)
    final = model.l3(out4)
    return final

def mnist_predict(x, model):
    x = Variable(x)
    # output = mnist_forward(x, model)
    return np.argmax(model.predictor(x).data,1)

    # return F.softmax(output).data.argmax(1)

model = chainer.FunctionSet(conv1=F.Convolution2D(1, 20, 5, stride=2),   # 入力1枚、出力20枚、フィルタサイズ5ピクセル
                            conv2=F.Convolution2D(20, 50, 5),  # 入力20枚、出力50枚、フィルタサイズ5ピクセル
                            l1=F.Linear(800, 500),
                            l2=F.Linear(500, 62))

optimizer = optimizers.Adam()
optimizer.setup(model)

serializers.load_npz('model/mlp.model', model) # modelはCPUモードにして保存したはず
serializers.load_npz('model/mlp.state', optimizer)

if use_gpu:
    model.to_gpu()

def forward(x_data):
    x = chainer.Variable(x_data)
    h = F.max_pooling_2d(F.relu(model.conv1(x)), 2)
    h = F.max_pooling_2d(F.relu(model.conv2(h)), 2)
    h = F.dropout(F.relu(model.l1(h)), train=False)
    y = model.l2(h)
    answers = np.argmax(y.data, axis=1)
    confidences = F.accuracy(y, chainer.Variable(answers.astype(np.int32))).data
    return (answers, confidences)


def prepare(ndArr):
    ndArr = xp.asarray(ndArr.astype(np.float32))
    # 画像を (nsample, channel, height, width) の4次元テンソルに変換
    # MNISTはチャンネル数が1なのでreshapeだけでOK
    return ndArr.reshape((len(ndArr), 1, 50, 50))

data_3 = np.load("../char74k/binarized/3_3.npy")
answers, confidences = forward(prepare(data_3[:3]))
print(answers)

data_e = np.load("../char74k/binarized/14_E.npy")
answers, confidences = forward(prepare(data_e[6:10]))
print(answers)


