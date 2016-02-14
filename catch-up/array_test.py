#!/usr/bin/env python
# -*- coding: utf-8 -*-

arr1 = [1,2,3]
arr2 = [4,5,6]
assert arr1 + arr2 == [1,2,3,4,5,6]

arr1 += arr2
assert arr1 == [1,2,3,4,5,6]