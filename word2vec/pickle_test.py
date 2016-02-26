#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, pickle

curr_dir = os.getcwd()

data = {"arr":[10, 20, 30]}

# ファイルに保存
f = open(curr_dir + "/data/pickle.dump", "w")
pickle.dump(data, f)
f.close()

# ファイルから復元
f2 = open("data/pickle.dump", "r")
data2 = pickle.load(f2)
f2.close()
assert data2 == data
