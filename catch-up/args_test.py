#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

# 起動オプションの指定方法は2通り
# python args_test.py --hoge=2
# python args_test.py -o 2

parser = argparse.ArgumentParser()

parser.add_argument('--hoge', '-o', default=1, type=int)
parser.add_argument('--fuga', '-f', default='abc')

args = parser.parse_args()

assert args.hoge == 1
assert args.fuga == 'abc'
