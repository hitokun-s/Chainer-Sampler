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

import data
import net

import numpy as np

#Chainer Specific
from chainer import FunctionSet, Variable, optimizers, serializers
import chainer.functions as F
import chainer.links as L

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

mnist = data.load_mnist_data()
mnist['data'] = mnist['data'].astype(np.float32)
mnist['data'] /= 255

print(mnist['data'])
print(len(mnist['data'][0])) # 784 = 28 * 28

mnist['target'] = mnist['target'].astype(np.int32)
print(mnist['target'])

n_units = 100
model = L.Classifier(net.MnistMLP(784, n_units, 10))

optimizer = optimizers.Adam()
optimizer.setup(model)

serializers.load_npz('data/mlp.model', model)
serializers.load_npz('data/mlp.state', optimizer)

# print(model)
# model = L.Classifier(net.MnistMLP(784, n_units, 10))
# model = serializers.load_npz('mlp.model', model)
print(model)
print(mnist["data"].shape)
print(mnist["target"].shape)
print(mnist_predict(mnist["data"], model))

