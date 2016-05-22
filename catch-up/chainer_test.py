#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chainer
from chainer import computational_graph
from chainer import cuda
from chainer import optimizers
from chainer import serializers
from chainer import Variable
from chainer.utils import type_check
from chainer import function

import chainer.functions as F
import chainer.links as L

import math,sys,os
import numpy as np

def generate_rand(low, hight, size, dtype=np.float32):
    return np.random.uniform(low, hight, size, ).astype(dtype)

nz = 100

class Generator(chainer.Chain):
    def __init__(self):
        super(Generator, self).__init__(
                l0z=L.Linear(nz, 6 * 6 * 512, wscale=0.02 * math.sqrt(nz)),
                dc1=L.Deconvolution2D(512, 256, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 512)),
                dc2=L.Deconvolution2D(256, 128, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 256)),
                dc3=L.Deconvolution2D(128, 64, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 128)),
                dc4=L.Deconvolution2D(64, 3, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 64)),
                bn0l=L.BatchNormalization(6 * 6 * 512),
                bn0=L.BatchNormalization(512),
                bn1=L.BatchNormalization(256),
                bn2=L.BatchNormalization(128),
                bn3=L.BatchNormalization(64)
        )

    def __call__(self, z, test=False):
        lf = self.l0z(z).creator
        # print lf.outputs

        h = F.reshape(F.relu(self.bn0l(self.l0z(z), test=test)), (z.data.shape[0], 512, 6, 6))
        h = F.relu(self.bn1(self.dc1(h), test=test))
        h = F.relu(self.bn2(self.dc2(h), test=test))
        h = F.relu(self.bn3(self.dc3(h), test=test))
        x = (self.dc4(h)) # shape:(サンプル数（＝ z.data.shape[0]）, 3,96,96) になっている
        return F.reshape(x, (z.data.shape[0], 3 * 96 * 96))

gen = Generator()

o_gen = optimizers.Adam(alpha=0.0002, beta1=0.5)
o_gen.setup(gen)
o_gen.add_hook(chainer.optimizer.WeightDecay(0.00001))

o_gen.zero_grads()

batchsize = 5

seed = generate_rand(-1, 1, (batchsize, nz), dtype=np.float32)
z = Variable(seed)

z2 = chainer.links.Parameter(seed)

x = gen(z)
print x.data.shape # (100,3,96,96)

# t = Variable(np.random.uniform(0, 1, batchsize).astype(np.int32))
t = Variable(np.random.uniform(0, 1, (batchsize, 27648)).astype(np.float32))
print t.data.shape

fl = None # first layer
for l in gen.namedlinks():
    if l[1].__class__.__name__ == "Linear":
        print "found"
        # print l[1].W.data
        # print l[1].W.grad
        # print l[1].b.data
        # print l[1].b.grad
        fl = l[1]

# fl = gen.children()[0] # なんかだめ。
print fl.W.grad.shape # (18432, 100)
print fl.W.grad

# L_gen = F.softmax_cross_entropy(x, Variable(np.zeros(batchsize, dtype=np.int32)))
# L_gen = F.softmax_cross_entropy(x, t)
L_gen = F.mean_squared_error(x, t)

print L_gen.data

o = gen.l0z(z)
# fl = o.creator

# L_gen.backward()
# o_gen.update()

# print gen.l0z
# print fl.W.grad

print z.data.shape # => (100, 100)
# print fl.inputs[0].data.shape # => (100, 100)
# print fl.inputs[1].data.shape # W => (18432, 100) ここで、18432 = 6 * 6 * 512
# print fl.inputs[2].data.shape # b => (18432, )

# w = fl.inputs[1]
w = fl.W

def getLearnedInput(inputs, o):
    for sample_idx in range(len(inputs)):
        input = inputs[sample_idx]
        for in_idx in range(len(input)):
            sum = 0
            for i in range(18432):
                sum += w.data[i, in_idx] * w.grad[i, in_idx] / o.data[sample_idx][i]
            input[in_idx] -= 0.05 * sum
    return inputs

for it in range(10):
    o = gen.l0z(z)
    L_gen.backward()
    z = Variable(getLearnedInput(z.data, o))
    x = gen(z)
    L_gen = F.mean_squared_error(x, t)
    print L_gen.data