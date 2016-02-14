#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

arr = np.array([1, 2, 3, 4])
assert np.sum(arr) == 10
assert np.array_equal(arr + 1, np.array([2, 3, 4, 5]))

arr2 = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
assert arr2.size == 8
assert len(arr2) == 2
assert arr2.shape[0] == len(arr2)

# bit inversion
arr3 = np.array([1, 0, 1, 1, 0])
f = np.vectorize(lambda x: 1 - x)
assert np.array_equal(f(arr3), np.array([0, 1, 0, 0, 1]))

# 外縁の要素を切り取る
arr4 = np.array([
    [1, 1, 1, 0],
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1]
])
arr4.shape == (4, 4)
res = []
for i, v in np.ndenumerate(arr4):
    if i[0] in [0, 3] or i[1] in [0, 3]:
        res.append(v)
res = np.array(res)
assert res.size == 12
assert np.count_nonzero(res) == 9

# ランダムに並び変える、ランダムサンプリング
arr5 = np.array([1,2,3,4,5])
perm = np.random.permutation(5)
print perm # ランダムに並べたインデックス
print arr5[perm] # ランダムに並べた値
