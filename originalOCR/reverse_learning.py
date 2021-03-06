#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse

import numpy as np
import six

import chainer, os, time
from chainer import computational_graph
from chainer import cuda
import chainer.links as L
import chainer.functions as F
from chainer import optimizers
from chainer import serializers

parser = argparse.ArgumentParser(description='Chainer example: MNIST')
parser.add_argument('--initmodel', '-m', default='',
                    help='Initialize the model from given file')
parser.add_argument('--resume', '-r', default='',
                    help='Resume the optimization from snapshot')
parser.add_argument('--net', '-n', choices=('simple', 'parallel'),
                    default='simple', help='Network type')

parser.add_argument('--gpu', '-g', default=-1, type=int)
parser.add_argument('--epoch', '-e', default=20, type=int)

args = parser.parse_args()

batchsize = 100
n_epoch = args.epoch

inputCnt = 50 * 50
classCnt = 62
data = []
target = []

class_labels = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

# Prepare dataset
fileNames = os.listdir("../char74k/binarized")
for fileName in fileNames:
    class_idx = int(fileName[:fileName.index("_")]) # 文字列先頭から'_'までの数字を取得
    class_data = np.load("../char74k/binarized/" + fileName)
    print("parsed file:%s, class:%s, data count:%d" % (fileName, class_labels[class_idx], class_data.shape[0]))
    for class_datum in class_data:
        assert class_datum.size == inputCnt
        data.append(class_datum)
        target.append(class_idx)

data = np.array(data, dtype=np.float32)
target = np.array(target, dtype=np.int32)

print("data count:%d" % len(data))
print("target count:%d" % len(target))

# randomize order
randomized_idx = np.random.permutation(target.size)
data = data[randomized_idx]
target = target[randomized_idx]

# 訓練データとテストデータに分割
N = int(target.size * 0.98) # sample count
x_train, x_test = np.split(data,   [N])
y_train, y_test = np.split(target, [N])
# from sklearn.cross_validation import train_test_split
# x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.1)

N_test = y_test.size

print("test sample size:%d" % y_test.size)

use_gpu = args.gpu >= 0
if use_gpu:
    cuda.check_cuda_available()
    xp = cuda.cupy
    cuda.get_device(args.gpu).use()
else:
    xp = np

print("using GPU:%s" % use_gpu)

# 画像を (nsample, channel, height, width) の4次元テンソルに変換
# MNISTはチャンネル数が1なのでreshapeだけでOK
x_train = x_train.reshape((len(x_train), 1, 50, 50))
x_test = x_test.reshape((len(x_test), 1, 50, 50))

# F.Convolution2D(入力チャネル数, 特徴マップチャネル数, フィルタサイズ（一辺）)
# F.Linear(全結合層の入力ユニット数、出力ユニット数)
model = chainer.FunctionSet(conv1=F.Convolution2D(1, 20, 5, stride=2),   # 入力1枚、出力20枚、フィルタサイズ5ピクセル
                            conv2=F.Convolution2D(20, 50, 5),  # 入力20枚、出力50枚、フィルタサイズ5ピクセル => 出力画像は、１チャネルで8 * 8 （= 64ユニット）
                            l1=F.Linear(800, 500),
                            l2=F.Linear(500, classCnt))

if use_gpu:
    model.to_gpu()

def forward(x_data, y_data, train=True):
    x, t = chainer.Variable(x_data), chainer.Variable(y_data)
    h = F.max_pooling_2d(F.relu(model.conv1(x)), 2)
    h = F.max_pooling_2d(F.relu(model.conv2(h)), 2)
    h = F.dropout(F.relu(model.l1(h)), train=train)
    y = model.l2(h)
    if train:
        return F.softmax_cross_entropy(y, t)
    else:
        return F.accuracy(y, t)

# Setup optimizer
optimizer = optimizers.Adam()
optimizer.setup(model)

# Init/Resume
if args.initmodel:
    print('Load model from', args.initmodel)
    serializers.load_npz(args.initmodel, model)
if args.resume:
    print('Load optimizer state from', args.resume)
    serializers.load_npz(args.resume, optimizer)

# 訓練ループ
start_time = time.clock()
for epoch in range(1, n_epoch + 1):
    print("epoch: %d" % epoch)

    perm = np.random.permutation(N)
    sum_loss = 0
    for i in range(0, N, batchsize):
        x_batch = xp.asarray(x_train[perm[i:i + batchsize]])
        y_batch = xp.asarray(y_train[perm[i:i + batchsize]])

        optimizer.zero_grads()
        loss = forward(x_batch, y_batch)
        loss.backward()
        optimizer.update()
        sum_loss += float(loss.data) * len(y_batch)

    print("train mean loss: %f" % (sum_loss / N))

    sum_accuracy = 0
    for i in range(0, N_test, batchsize):
        x_batch = xp.asarray(x_test[i:i + batchsize])
        y_batch = xp.asarray(y_test[i:i + batchsize])

        acc = forward(x_batch, y_batch, train=False)
        sum_accuracy += float(acc.data) * len(y_batch)

    print("test accuracy: %f" % (sum_accuracy / N_test))


end_time = time.clock()
print(end_time - start_time)

# CPU環境でも学習済みモデルを読み込めるようにCPUに移してからダンプ
model.to_cpu()

# Save the model and the optimizer
print('save the model')
serializers.save_npz('model/mlp.model', model)
print('save the optimizer')
serializers.save_npz('model/mlp.state', optimizer)
