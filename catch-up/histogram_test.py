#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

import codecs
from numpy.random import *

# 3番目の引数には、(2,3,4)などのマトリックスもタプルで指定できる
dist1 = normal(70, 30, 50)  # 戻り値は普通のリストではなくndarray
dist2 = normal(180, 40, 50)

# 普通のリストだと「＋」で結合となるが、
# ndarrayyだと、以下は同じインデックスの要素同士を演算した結果になってしまう！
# dist = dist1 + dist2

# ndarrayを結合
dist = np.r_[dist1, dist2]

# dist = dist[np.where((dist > 0) & (dist < 256))] # 下の書き方で行けるらしい
dist = dist[(dist > 0) | (dist < 256)]
print dist
dist = np.rint(dist)
print dist

##################################
#       PyPlot.histogram()       #
##################################

# binsはヒストグラムの本数。デフォルト10。bin=「区分け棚」の意味があるらしい。
# rangeは対象域
# normedは正規化（グラフ同士の比較で便利
# 下の場合、集計幅を20にしたかったので仕方なくbinsとraingeで対応した
hist, bins, patches = plt.hist(dist, bins=13, range=(0, 260), color='green')

print hist # 各binのカウント数
print bins # 各binの集計域の開始値（この場合は、0, 20, 40, 60, ...）
for patch in patches:
    print patch # Rectangleオブジェクト

# plt.show()

##################################
#     NumPy.histogram()          #
##################################

hist, bins = np.histogram(dist, bins=13, range=(0,260))
print hist # 各binのカウント数
print bins # 各binの集計域の開始値（この場合は、0, 20, 40, 60, ...）

# 判別分析法により、二値化の閾値を算定する
