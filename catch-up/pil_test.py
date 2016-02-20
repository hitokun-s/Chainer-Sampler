#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image

def binarize(ndArr, th=50):
    # threshold = th(ndArr.flatten())
    # print "threshold:%d" % threshold
    (rowCnt, colCnt) = ndArr.shape
    # print "row:%d, col:%d" % (rowCnt,colCnt)
    for i in range(rowCnt):
        for j in range(colCnt):
            ndArr[i][j] = 1 if ndArr[i][j] > th else 0
    return ndArr

res = np.asarray(Image.open("images/48x48.png").convert('L'))
res.flags.writeable = True

print res.shape
print res
binalized = binarize(res, 50)
print binalized

f = np.vectorize(lambda x : 1 - x) # 全要素に作用する関数を作成（xは各要素の値）
reversed = f(binalized)

print reversed
