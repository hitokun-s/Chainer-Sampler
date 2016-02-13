#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

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
            maxVal = tmp
            maxIdx = i
    return maxIdx * 20

def binarize(ndArr):
    threshold = th(ndArr.flatten())
    # print "threshold:%d" % threshold
    (rowCnt, colCnt) = ndArr.shape
    # print "row:%d, col:%d" % (rowCnt,colCnt)
    for i in range(rowCnt):
        for j in range(colCnt):
            ndArr[i][j] = 1 if ndArr[i][j] > threshold else 0
    return ndArr
