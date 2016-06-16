#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

num1 = 10
assert num1 / 3 == 3

# 小数のrangeがほしいとき
# print [x * 0.1 for x in range(10,1,-1)]
print np.arange(0.3, 0.01, -0.01).tolist() + np.arange(0.01, 0, -0.001).tolist()
