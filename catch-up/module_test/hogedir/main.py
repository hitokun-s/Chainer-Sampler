#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

# 下記のようにすると、本スクリプトを実行するディレクトリ（os.getcwd()）がどこであっても、module_a をImportできる

print os.path.dirname(__file__)
tgt_dir = os.path.dirname(os.path.dirname(__file__))

sys.path.append(tgt_dir)

import module_a

module_a.hoge()