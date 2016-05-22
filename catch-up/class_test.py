#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Test():

    """An example of multi-layer perceptron for MNIST dataset.

    This is a very simple implementation of an MLP. You can modify this code to
    build your own neural net.

    """
    def __init__(self):
        print "Test created!"

    def __call__(self, x):
        return "%s is tested!" % x

    def __call__(self, x, y):
        return "%s and %s is tested!" % (x, y)

test = Test()
test("hoge")