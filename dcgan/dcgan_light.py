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

from lib import *

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
n_epoch = 100000
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
        generated = xp.random.uniform(low, hight, size).astype(dtype)
    return generated

def clip_img(x):
    return np.float32(-1 if x < -1 else (1 if x > 1 else x))

def binarize(ndArr, th=50):
    (rowCnt, colCnt) = ndArr.shape
    for i in range(rowCnt):
        for j in range(colCnt):
            ndArr[i][j] = -1 if ndArr[i][j] > th else 1 # 白（背景）を-1に、黒を1にしている
    return ndArr

def train_dcgan_labeled(gen, dis, o_gen, o_dis, epoch0=0):

    # o_gen.setup(gen)
    # o_dis.setup(dis)
    # o_gen.add_hook(chainer.optimizer.WeightDecay(0.00001))
    # o_dis.add_hook(chainer.optimizer.WeightDecay(0.00001))

    zvis = (generate_rand(-1, 1, (100, nz), dtype=np.float32))

    # サンプル52にしたことだし、もう固定で作ってしまう
    # ----------------------------------------------------------------------------------
    x2 = np.zeros((batchsize, 1, 48, 48), dtype=np.float32)
    for j in range(52):
        res = np.asarray(Image.open(StringIO(dataset[j])).convert('L')).astype(np.float32)
        res.flags.writeable = True
        x2[j, :, :, :] = binarize(res, 50)
    x2 = Variable(cuda.to_gpu(x2) if using_gpu else x2)
    # ----------------------------------------------------------------------------------

    for epoch in xrange(epoch0, n_epoch):
        perm = np.random.permutation(n_train)
        sum_l_dis = np.float32(0)
        sum_l_gen = np.float32(0)

        for i in xrange(0, n_train, batchsize):
            # discriminator
            # 0: from dataset
            # 1: from noise

            # print "load image start ", i
            # x2 = np.zeros((batchsize, 1, 48, 48), dtype=np.float32)
            # for j in range(batchsize):
            #     try:
            #         rnd = np.random.randint(len(dataset))
            #         # rnd2 = np.random.randint(2)
            #         # img = np.asarray(Image.open(StringIO(dataset[rnd])).convert('RGB')).astype(np.float32).transpose(2,0,1)
            #         # 左右反転しているっぽい（和田）
            #         # if rnd2 == 0:
            #         #     x2[j, :, :, :] = (img[:, :, ::-1] - 128.0) / 128.0
            #         # else:
            #         #     x2[j, :, :, :] = (img[:, :, :] - 128.0) / 128.0
            #         res = np.asarray(Image.open(StringIO(dataset[rnd])).convert('L')).astype(np.float32)
            #         res.flags.writeable = True
            #         x2[j, :, :, :] = binarize(res, 50)
            #     except:
            #         print 'read image error occured', fs[rnd]

            # train generator
            z = Variable(generate_rand(-1, 1, (batchsize, nz), dtype=np.float32))
            x = gen(z)
            yl = dis(x)
            L_gen = F.softmax_cross_entropy(yl, Variable(xp.zeros(batchsize, dtype=np.int32)))
            L_dis = F.softmax_cross_entropy(yl, Variable(xp.ones(batchsize, dtype=np.int32)))

            # train discriminator

            # x2 = Variable(cuda.to_gpu(x2) if using_gpu else x2)
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
            if epoch % 200 == 0:
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

                serializers.save_hdf5("%s/dcgan_model_dis.h5" % out_model_dir, dis)
                serializers.save_hdf5("%s/dcgan_model_gen.h5" % out_model_dir, gen)
                serializers.save_hdf5("%s/dcgan_state_dis.h5" % out_model_dir, o_dis)
                serializers.save_hdf5("%s/dcgan_state_gen.h5" % out_model_dir, o_gen)

        print 'epoch end', epoch, sum_l_gen / n_train, sum_l_dis / n_train

gen = Generator(nz=nz)
dis = Discriminator()
o_gen = optimizers.Adam(alpha=0.0002, beta1=0.5)
o_dis = optimizers.Adam(alpha=0.0002, beta1=0.5)
o_gen.setup(gen)
o_dis.setup(dis)
o_gen.add_hook(chainer.optimizer.WeightDecay(0.00001))
o_dis.add_hook(chainer.optimizer.WeightDecay(0.00001))

if using_gpu:
    gen.to_gpu()
    dis.to_gpu()

if os.path.exists("%s/dcgan_model_dis.h5" % out_model_dir):
    print "Model files found!"
    serializers.load_hdf5("%s/dcgan_model_dis.h5" % out_model_dir, dis)
    serializers.load_hdf5("%s/dcgan_model_gen.h5" % out_model_dir, gen)
    serializers.load_hdf5("%s/dcgan_state_dis.h5" % out_model_dir, o_dis)
    serializers.load_hdf5("%s/dcgan_state_gen.h5" % out_model_dir, o_gen)
else:
    try:
        os.mkdir(out_image_dir)
        os.mkdir(out_model_dir)
    except:
        pass

train_dcgan_labeled(gen, dis, o_gen, o_dis)
