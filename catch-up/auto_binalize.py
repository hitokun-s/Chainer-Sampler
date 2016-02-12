#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 自動二値化

import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

from numpy.random import *

# 二値化の閾値を取得する。判別判定法による。
# 引数は、256諧調のグレースケール値（0-255）の一次配列（ndarray）を想定
def th(arr):
    hist, bins = np.histogram(arr, bins=13, range=(0, 260))
    # hist : 各binのカウント数の配列
    # bins : 各binの集計域の開始値の配列（この場合は、0, 20, 40, 60, ...）=> 閾値を調べるのには必要ない！
    sum = 0
    for i, cnt in enumerate(hist):
        sum += i * cnt
    maxVal = maxIdx = 0
    c1, c2, s1, s2 = (0, np.sum(hist), 0, sum)
    for i, cnt in enumerate(hist):
        c1 += cnt
        c2 -= cnt
        if c1 == 0 or c2 == 0:
            continue
        delta = i * cnt
        s1 += delta
        s2 -= delta
        tmp = c1 * c2 * pow(s1/c1 - s2/c2, 2)
        if tmp > maxVal:
            maxIdx = i
    return maxIdx * 20

dist1 = normal(70, 30, 50)  # 戻り値は普通のリストではなくndarray
dist2 = normal(180, 40, 50)
dist = np.r_[dist1, dist2]
dist = dist[(dist > 0) | (dist < 256)]

print th(dist) # 大体200か220になる
