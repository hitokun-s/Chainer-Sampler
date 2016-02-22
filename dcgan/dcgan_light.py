#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import numpy as np
from PIL import Image
import os
from StringIO import StringIO
import math
import pylab

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

import numpy

using_gpu = False
xp = np
try:
    cuda.check_cuda_available()
    xp = cuda.cupy
    cuda.get_device(0).use()
    using_gpu = True
except:
    print  "I'm sorry. Using CPU."

image_dir = './images48'
out_image_dir = './out_images'
out_model_dir = './out_models'

nz = 30  # # of dim for Z
batchsize = 52
n_epoch = 10000
n_train = 52
image_save_interval = 51

fs = os.listdir(image_dir)
print len(fs)
dataset = []
for fn in fs:
    f = open('%s/%s' % (image_dir, fn), 'rb')
    img_bin = f.read()
    dataset.append(img_bin)
    f.close()
print len(dataset)


# sizeは、1次元なら数字、多次元ならタプル
def generate_rand(low, hight, size, dtype=np.float32):
    global using_gpu
    if using_gpu:
        # この書き方だと、xp = cuda.cupy なら良いが、xp = np の場合にエラーになる
        generated = xp.random.uniform(low, hight, size, dtype=dtype)
    else:
        generated = xp.random.uniform(low, hight, size, ).astype(dtype)
    return generated


class ELU(function.Function):
    """Exponential Linear Unit."""

    # https://github.com/muupan/chainer-elu

    def __init__(self, alpha=1.0):
        self.alpha = numpy.float32(alpha)

    def check_type_forward(self, in_types):
        type_check.expect(in_types.size() == 1)
        x_type, = in_types

        type_check.expect(
                x_type.dtype == numpy.float32,
        )

    def forward_cpu(self, x):
        y = x[0].copy()
        neg_indices = x[0] < 0
        y[neg_indices] = self.alpha * (numpy.exp(y[neg_indices]) - 1)
        return y,

    def forward_gpu(self, x):
        y = cuda.elementwise(
                'T x, T alpha', 'T y',
                'y = x >= 0 ? x : alpha * (exp(x) - 1)', 'elu_fwd')(
                x[0], self.alpha)
        return y,

    def backward_cpu(self, x, gy):
        gx = gy[0].copy()
        neg_indices = x[0] < 0
        gx[neg_indices] *= self.alpha * numpy.exp(x[0][neg_indices])
        return gx,

    def backward_gpu(self, x, gy):
        gx = cuda.elementwise(
                'T x, T gy, T alpha', 'T gx',
                'gx = x >= 0 ? gy : gy * alpha * exp(x)', 'elu_bwd')(
                x[0], gy[0], self.alpha)
        return gx,


def elu(x, alpha=1.0):
    """Exponential Linear Unit function."""
    # https://github.com/muupan/chainer-elu
    return ELU(alpha=alpha)(x)


class Generator(chainer.Chain):
    def __init__(self):
        super(Generator, self).__init__(
                l0z=L.Linear(nz, 6 * 6 * 128, wscale=0.02 * math.sqrt(nz)),
                dc1=L.Deconvolution2D(128, 64, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 128)),
                dc2=L.Deconvolution2D(64, 32, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 64)),
                dc3=L.Deconvolution2D(32, 1, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 32)),
                bn0l=L.BatchNormalization(6 * 6 * 128),
                bn0=L.BatchNormalization(128),
                bn1=L.BatchNormalization(64),
                bn2=L.BatchNormalization(32)
        )

    def __call__(self, z, test=False):
        h = F.reshape(F.relu(self.bn0l(self.l0z(z), test=test)), (z.data.shape[0], 128, 6, 6))
        h = F.relu(self.bn1(self.dc1(h), test=test))
        h = F.relu(self.bn2(self.dc2(h), test=test))
        x = (self.dc3(h))
        return x


class Discriminator(chainer.Chain):
    def __init__(self):
        super(Discriminator, self).__init__(
                c0=L.Convolution2D(1, 32, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 3)),
                c1=L.Convolution2D(32, 64, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 32)),
                c2=L.Convolution2D(64, 128, 4, stride=2, pad=1, wscale=0.02 * math.sqrt(4 * 4 * 64)),
                l4l=L.Linear(6 * 6 * 128, 2, wscale=0.02 * math.sqrt(6 * 6 * 128)),
                bn0=L.BatchNormalization(32),
                bn1=L.BatchNormalization(64),
                bn2=L.BatchNormalization(128)
        )

    def __call__(self, x, test=False):
        h = elu(self.c0(x))  # no bn because images from generator will katayotteru?
        h = elu(self.bn1(self.c1(h), test=test))
        h = elu(self.bn2(self.c2(h), test=test))
        l = self.l4l(h)
        return l


def clip_img(x):
    return np.float32(-1 if x < -1 else (1 if x > 1 else x))

def binarize(ndArr, th=50):
    (rowCnt, colCnt) = ndArr.shape
    for i in range(rowCnt):
        for j in range(colCnt):
            ndArr[i][j] = -1 if ndArr[i][j] > th else 1 # 白（背景）を-1に、黒を1にしている
    return ndArr

def train_dcgan_labeled(gen, dis, epoch0=0):
    o_gen = optimizers.Adam(alpha=0.0002, beta1=0.5)
    o_dis = optimizers.Adam(alpha=0.0002, beta1=0.5)
    o_gen.setup(gen)
    o_dis.setup(dis)
    o_gen.add_hook(chainer.optimizer.WeightDecay(0.00001))
    o_dis.add_hook(chainer.optimizer.WeightDecay(0.00001))

    zvis = (generate_rand(-1, 1, (100, nz), dtype=np.float32))

    for epoch in xrange(epoch0, n_epoch):
        perm = np.random.permutation(n_train)
        sum_l_dis = np.float32(0)
        sum_l_gen = np.float32(0)

        for i in xrange(0, n_train, batchsize):
            # discriminator
            # 0: from dataset
            # 1: from noise

            # print "load image start ", i
            x2 = np.zeros((batchsize, 1, 48, 48), dtype=np.float32)
            for j in range(batchsize):
                try:
                    rnd = np.random.randint(len(dataset))
                    # rnd2 = np.random.randint(2)
                    # img = np.asarray(Image.open(StringIO(dataset[rnd])).convert('RGB')).astype(np.float32).transpose(2,0,1)
                    # 左右反転しているっぽい（和田）
                    # if rnd2 == 0:
                    #     x2[j, :, :, :] = (img[:, :, ::-1] - 128.0) / 128.0
                    # else:
                    #     x2[j, :, :, :] = (img[:, :, :] - 128.0) / 128.0
                    res = np.asarray(Image.open(StringIO(dataset[rnd])).convert('L')).astype(np.float32)
                    res.flags.writeable = True
                    x2[j, :, :, :] = binarize(res, 50)
                except:
                    print 'read image error occured', fs[rnd]
            # print "load image done"

            # train generator
            z = Variable(generate_rand(-1, 1, (batchsize, nz), dtype=np.float32))
            x = gen(z)
            yl = dis(x)
            L_gen = F.softmax_cross_entropy(yl, Variable(xp.zeros(batchsize, dtype=np.int32)))
            L_dis = F.softmax_cross_entropy(yl, Variable(xp.ones(batchsize, dtype=np.int32)))

            # train discriminator

            x2 = Variable(cuda.to_gpu(x2) if using_gpu else x2)
            yl2 = dis(x2)
            L_dis += F.softmax_cross_entropy(yl2, Variable(xp.zeros(batchsize, dtype=np.int32)))

            # print "forward done"

            o_gen.zero_grads()
            L_gen.backward()
            o_gen.update()

            o_dis.zero_grads()
            L_dis.backward()
            o_dis.update()

            sum_l_gen += L_gen.data.get()
            sum_l_dis += L_dis.data.get()

            # print "backward done"

            # if i % image_save_interval == 0:
            if epoch % 20 == 0:
                pylab.rcParams['figure.figsize'] = (16.0, 16.0)
                pylab.clf()
                vissize = 100
                z = zvis
                z[50:, :] = (xp.random.uniform(-1, 1, (50, nz), dtype=np.float32))
                z = Variable(z)
                x = gen(z, test=True)
                x = x.data.get()
                for i_ in range(100):
                    # tmp = ((np.vectorize(clip_img)(x[i_, :, :, :]) + 1) / 2).transpose(1, 2, 0)
                    tmp = np.vectorize(clip_img)(x[i_, 0, :, :])
                    pylab.subplot(10, 10, i_ + 1)
                    pylab.gray()
                    pylab.imshow(tmp)
                    pylab.axis('off')
                pylab.savefig('%s/vis_%d_%d.png' % (out_image_dir, epoch, i))

        serializers.save_hdf5("%s/dcgan_model_dis_%d.h5" % (out_model_dir, epoch), dis)
        serializers.save_hdf5("%s/dcgan_model_gen_%d.h5" % (out_model_dir, epoch), gen)
        serializers.save_hdf5("%s/dcgan_state_dis_%d.h5" % (out_model_dir, epoch), o_dis)
        serializers.save_hdf5("%s/dcgan_state_gen_%d.h5" % (out_model_dir, epoch), o_gen)
        print 'epoch end', epoch, sum_l_gen / n_train, sum_l_dis / n_train


gen = Generator()
dis = Discriminator()

if using_gpu:
    gen.to_gpu()
    dis.to_gpu()

try:
    os.mkdir(out_image_dir)
    os.mkdir(out_model_dir)
except:
    pass

train_dcgan_labeled(gen, dis)
