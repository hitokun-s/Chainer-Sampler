#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PCA = 主成分分析
# 出典：http://breakbee.hatenablog.jp/entry/2014/07/13/191803

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sklearn import datasets, decomposition

# データセットの読み込み
iris = datasets.load_iris()
X = iris.data
Y = iris.target
print Y # クラスインデックス（＝ラベル数字）の配列

# 主成分分析前のサイズ
print X.shape

# 主成分分析による次元削減
pca = decomposition.PCA(n_components = 2)
pca.fit(X)
X_pca= pca.transform(X)

# 主成分分析後のサイズ
print X_pca.shape # (150, 2)

# 可視化
s  = np.array([x for i, x in enumerate(X_pca) if Y[i] == 0])
ve = np.array([x for i, x in enumerate(X_pca) if Y[i] == 1])
vi = np.array([x for i, x in enumerate(X_pca) if Y[i] == 2])

colors = ['b.', 'r.', 'k.']
fig, ax = plt.subplots()
ax.plot(s[:,0],  s[:,1],  'b.', label='Setosa')
ax.plot(ve[:,0], ve[:,1], 'r.', label='Versicolour')
ax.plot(vi[:,0], vi[:,1], 'k.', label='Virginica')

ax.set_title("PCA for iris")
ax.legend(numpoints=1)

plt.show()
