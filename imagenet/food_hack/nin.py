#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np


class NIN(chainer.Chain):

    """Network-in-Network example model."""

    insize = 227

    def __init__(self):
        w = math.sqrt(2)  # MSRA scaling
        super(NIN, self).__init__(
            mlpconv1=L.MLPConvolution2D(
                3, (96, 96, 96), 11, stride=4, wscale=w),
            mlpconv2=L.MLPConvolution2D(
                96, (256, 256, 256), 5, pad=2, wscale=w),
            mlpconv3=L.MLPConvolution2D(
                256, (384, 384, 384), 3, pad=1, wscale=w),
            mlpconv4=L.MLPConvolution2D(
                384, (1024, 1024, 1000), 3, pad=1, wscale=w),
        )
        self.train = True

    def clear(self):
        self.loss = None
        self.accuracy = None

    def __call__(self, x, t):
        self.clear()
        h = F.max_pooling_2d(F.relu(self.mlpconv1(x)), 3, stride=2)
        h = F.max_pooling_2d(F.relu(self.mlpconv2(h)), 3, stride=2)
        h = F.max_pooling_2d(F.relu(self.mlpconv3(h)), 3, stride=2)
        h = self.mlpconv4(F.dropout(h, train=self.train))
        h = F.reshape(F.average_pooling_2d(h, 6), (x.data.shape[0], 1000))

        self.loss = F.softmax_cross_entropy(h, t)
        self.accuracy = F.accuracy(h, t)
        return self.loss

    def predict(self, x):
        self.clear()
        h = F.max_pooling_2d(F.relu(self.mlpconv1(x)), 3, stride=2)
        h = F.max_pooling_2d(F.relu(self.mlpconv2(h)), 3, stride=2)
        h = F.max_pooling_2d(F.relu(self.mlpconv3(h)), 3, stride=2)
        h = self.mlpconv4(F.dropout(h, train=self.train))
        h = F.reshape(F.average_pooling_2d(h, 6), (x.data.shape[0], 1000))

        sm = F.softmax(h).data
        answers = np.argmax(h.data, axis=1)

        #  chainer.Variable(xp.asarray([0]).astype(np.int32), volatile=volatile)
        t = chainer.Variable(answers.astype(np.int32), volatile='on')

        # probs = []
        # for i in range(len(x)):
        #     probs.append(math.exp(-F.softmax_cross_entropy(chainer.Variable([h.data[i]]), chainer.Variable([t.data[i]])).data))

        sfe = F.softmax_cross_entropy(h, t).data
        prob = math.exp(-sfe)

        # e_s = np.exp(h.data) # 各サンプルの各入力値の指数を取る
        # z_s = e_s.sum(axis=1) # 各サンプルごとに、指数の和を計算
        # probs = e_s[np.arange(len(e_s)), answers] / z_s # 各サ
        return (answers[0], prob)
