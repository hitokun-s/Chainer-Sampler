#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

arr = np.array([1, 2, 3, 4])
assert np.sum(arr) == 10
assert arr.sum() == 10
assert np.array_equal(arr + 1, np.array([2, 3, 4, 5]))
assert arr.max() == 4

arr2 = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
assert arr2.size == 8
assert len(arr2) == 2
assert arr2.shape[0] == len(arr2)
assert np.array_equal(np.sum(arr2, axis=1), np.array([10,26]))
assert np.array_equal(np.amax(arr2, axis=1), np.array([4,8]))
assert np.array_equal(np.argmax(arr2, axis=1), np.array([3,3]))

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

# 部分配列
assert np.array_equal(arr4[:2], np.array([
    [1, 1, 1, 0],
    [0, 1, 1, 1]
]))

# ランダムに並び変える、ランダムサンプリング
arr5 = np.array([1,2,3,4,5])
perm = np.random.permutation(5)
print perm # ランダムに並べたインデックス
print arr5[perm] # ランダムに並べた値

arr6 = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])
assert np.array_equal(arr6.sum(axis=1), np.array([6,15,24]))
assert np.array_equal(arr6[:,[0]], np.array([[1],[4],[7]]))
assert np.array_equal(arr6[[0,1,2],[1,1,1]], np.array([2,5,8]))

arr7 = np.arange(5)
assert np.array_equal(arr7, np.array([0,1,2,3,4]))

arr8 = np.array([2,4,6]).astype(float)
arr9 = np.array([4,4,4])
assert np.array_equal(arr8 / arr9, np.array([0.5,1.0,1.5]))
