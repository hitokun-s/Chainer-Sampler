#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, traceback

# スクリプトとして実行された場合は、__nam__には"__main__"が入る
# これによってモジュール呼び出しと区別できる
assert __name__ == "__main__"

print __file__  # 本ファイルのパス
print os.path.dirname(__file__) # 本ファイルのディレクトリ

# さらに親ディレクトリの取得方法2通り
print "parent dir:%s" % os.path.dirname(os.path.dirname(__file__))
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
