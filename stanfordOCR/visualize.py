#coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

size = 50 # sample size

file = open('data/letter.data', 'r').read()
lines = file.split('\n')[0:size]

print len(lines)

colcnt = 10
tmp = size / colcnt
rowcnt = tmp if 50 % colcnt == 0 else tmp + 1

f, tpl = plt.subplots(rowcnt, colcnt)

for i, line in enumerate(lines):
    itemList = line[:-1].split('\t')
    print itemList[1] # letter
    data = itemList[6:134]
    assert len(data) == 128 # <= 16 * 8
    rowIdx = i / colcnt
    colIdx = i % colcnt
    arr = np.array(data).reshape([16,8]).astype(np.int32)
    subplot = tpl[rowIdx][colIdx]
    subplot.imshow(arr, interpolation='none', cmap = cm.Greys_r)
    subplot.axes.get_xaxis().set_visible(False) # == subplot.axes.get_xaxis().set_ticks([])
    subplot.axes.get_yaxis().set_visible(False) # == subplot.axes.get_yaxis().set_ticks([])

plt.savefig("image.png")