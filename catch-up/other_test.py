#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, traceback

# スクリプトとして実行された場合は、__nam__には"__main__"が入る
# これによってモジュール呼び出しと区別できる
assert __name__ == "__main__"

print __file__  # 本ファイルのパス
print os.path.dirname(__file__) # 本ファイルのディレクトリ

# さらに親ディレクトリの取得方法
# print "parent dir:%s" % os.path.dirname(os.path.dirname(__file__)) # => これはLinux環境だと取得できない！！！
print "parent dir:%s" % os.path.dirname(os.getcwd())  #（windowsだとフォルダ区切り文字が円マークになる）

# OS依存のパス、カレントディレクトリ（windowsだとフォルダ区切り文字が円マークになる）
print os.path.realpath(__file__)
print os.getcwd()

try:
    var1 = 1/ 0
except:
    # 現在処理中の例外を示すタプル、(type, value, traceback) を返す
    assert sys.exc_info()[0] == ZeroDivisionError

# stacktraceを表示
try:
    var1 = 1/ 0
except:
    print traceback.format_exc()

# 0 から始まる差分10の等差数列を、200まで作る（200は含まない）
arr = xrange(0, 200, 10) # [0,10,20,30,...,.190]
