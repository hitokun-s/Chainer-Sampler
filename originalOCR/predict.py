#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import chainer
import numpy as np
import os
from chainer import cuda

#Chainer Specific
from chainer import Variable, optimizers, serializers
import chainer.functions as F

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

serializers.load_npz(os.path.dirname(__file__) + '/model/mlp.model', model) # modelはCPUモードにして保存したはず
serializers.load_npz(os.path.dirname(__file__) + '/model/mlp.state', optimizer)

if use_gpu:
    model.to_gpu()

def forward(x_data):
    x = chainer.Variable(x_data)
    h = F.max_pooling_2d(F.relu(model.conv1(x)), 2)
    h = F.max_pooling_2d(F.relu(model.conv2(h)), 2)
    h = F.dropout(F.relu(model.l1(h)), train=False)
    y = model.l2(h)
    answers = np.argmax(y.data, axis=1)
    t = chainer.Variable(answers.astype(np.int32))
    # print(F.softmax_cross_entropy(y, t).data)
    e_s = np.exp(y.data) # 各サンプルの各入力値の指数を取る
    z_s = e_s.sum(axis=1) # 各サンプルごとに、指数の和を計算
    probabilities = e_s[np.arange(len(e_s)), answers] / z_s # 各サンプルごとに、e_s / z_s の最大値（＝最大確率）を取得＝Softmax関数
    # confidences = F.accuracy(y, t).data
    return (answers, probabilities)


def prepare(ndArr):
    ndArr = xp.asarray(ndArr.astype(np.float32))
    # 画像を (nsample, channel, height, width) の4次元テンソルに変換
    # MNISTはチャンネル数が1なのでreshapeだけでOK
    return ndArr.reshape((len(ndArr), 1, 50, 50))

def predict(xArr):
    return forward(prepare(xArr))

if __name__ == '__main__':

    data_3 = np.load("../char74k/binarized/3_3.npy")
    answers, confidences = predict(data_3[:3])
    print("answers:%s, confidences:%s" % (str(answers), str(confidences)))

    data_e = np.load("../char74k/binarized/14_E.npy")
    answers, confidences = predict(data_e[0:60])
    print("answers:%s, confidences:%s" % (str(answers), str(confidences)))


