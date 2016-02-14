#!/usr/bin/env python
# -*- coding: utf-8 -*-

str1 = "abcde"
assert str1.index("c") == 2
assert str1[2] == "c"
assert str1[0:2] == "ab"
assert str1[:2] == "ab"

# 変数展開
assert "bool value:%s" % True == "bool value:True"