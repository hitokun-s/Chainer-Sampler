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
print "permutation:%s" % perm # ランダムに並べたインデックス
print arr5[perm] # ランダムに並びかえたもの
print arr5[perm[:2]] # ランダムに３つ取り出したもの

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

# 一様分布に従うデータ（＝一様乱数）を5個生成
rands = np.random.uniform(0.0, 1.0, 5)
print rands
rands = np.random.uniform(0.0, 1.0, (5,5))
print rands
print np.round(rands)

arr10 = np.array([
    [[1,2,3],[2,3,4],[3,4,5]],
    [[1,3,5],[2,4,6],[3,5,7]],
    [[1,2,3],[2,3,5],[3,5,8]]
])
# :はワイルドカードと思えばいい
print arr10[1,:,1] # => [3,4,5]
print arr10[:,:,::-1] # 最小単位内で逆順になる
arr10[0,0,:] = [9,9,9]
print arr10


randomized = (np.random.uniform(-1, 1, (4,2)).astype(np.float32))
print randomized
# 行インデックス≧２のデータ（つまり３，４行目）を置換する
randomized[2:, :] = (np.random.uniform(-1, 1, (2,2)).astype(np.float32))
print randomized

nz = 30
z = (np.random.uniform(-1, 1, (100,nz)).astype(np.float32))
z[50:, :] = (np.random.uniform(-1, 1, (50, nz)).astype(np.float32))

print z.shape
print "The end!"

# 所定範囲内からランダムに選んだ数を返す
print np.random.randint(10)
print np.random.randint(10)
print np.random.randint(10)

x2 = np.zeros((10, 1, 2, 2), dtype=np.float32)
for i in range(10):
    x2[i,0,:,:] = np.array([[i,i],[i,i]])

perm = np.random.permutation(10)
selected = x2[perm[:5]]
print selected

# reshape(構造変形)
arr11 = np.arange(6)
print arr11 # [0 1 2 3 4 5]
arr11 = arr11.reshape((3, 2))
print arr11 # [[0 1][2 3][4 5]]
print arr11.reshape(6) # 直列化

# 対象に最も近いものを探索
tgt = np.array([
    [5,5],[5,5]
])
samples = np.array([
    [
        [1,2],[2,2]
    ],
    [
        [8,9],[10,11]
    ],
    [
        [4,5],[6,5]
    ],
    [
        [-1,0],[1,2]
    ],
])
print [((sample - tgt) * (sample - tgt)).sum() for sample in samples]
print np.argmin([((sample - tgt) * (sample - tgt)).sum() for sample in samples])

print samples + tgt