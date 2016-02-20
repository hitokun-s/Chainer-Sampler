#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

# pm2 startで実行すると、print文は標準ログに出力されるはず。
# 実行中プロセスのログファイルパスは、pm2 desc [process id]でわかる

parser = argparse.ArgumentParser()
parser.add_argument('--hoge', '-o', default='',help='')
args = parser.parse_args()
print args
