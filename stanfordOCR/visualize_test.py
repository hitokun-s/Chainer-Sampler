#coding: utf-8
# import cPickle
# import matplotlib.pyplot as plt
# model = cPickle.load(open("model.pkl", "rb"))
#
# # 1つめのConvolution層の重みを可視化
# print model.conv1.W.shape
#
# n1, n2, h, w = model.conv1.W.shape
# fig = plt.figure()
# fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)
# for i in range(n1):
#     ax = fig.add_subplot(2, 10, i + 1, xticks=[], yticks=[])
#     ax.imshow(model.conv1.W[i, 0], cmap=plt.cm.gray_r, interpolation='nearest')
# plt.show()

import matplotlib.pyplot as plt
import numpy as np
e = np.eye( 3 )  # 単位行列の生成

# plt.subplot( 131 ) # 表示区画を１行３列に設定し，その１番目に描画
# plt.imshow( e , interpolation='none' )
# plt.gray()
#
# plt.subplot( 132 )
# plt.imshow( e , interpolation='none' )
# plt.gray()
#
# plt.subplot( 133 )
# plt.imshow( e , interpolation='none' )
# plt.gray()

f, ((ax1, ax2, ax3)) = plt.subplots(1,3)
ax1.imshow( e , interpolation='none' )
ax2.imshow( e , interpolation='none' )
ax3.imshow( e , interpolation='none' )

plt.savefig("image.png")

plt.clf()

f, tpl = plt.subplots(1,3)
tpl[0].imshow( e , interpolation='none' )
tpl[1].imshow( e , interpolation='none' )
tpl[2].imshow( e , interpolation='none' )

plt.savefig("image.png")