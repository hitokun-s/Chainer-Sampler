#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cStringIO
import traceback, sys, os

from flask import Flask, request, send_from_directory
from flask import jsonify
import ssd
from PIL import Image
import json

# add project base dir to module search path ( for importing char74k, originalOCR)
tgt_dir = os.path.dirname(os.getcwd())
sys.path.append(tgt_dir)
print "path added:%s" % tgt_dir

# from char74k.binarize import *
# from originalOCR.predict import *

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def root():
    print "get an access!"
    return send_from_directory('', "index.html")

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('', path)

class_labels = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

@app.route('/query', methods=['POST'])
def query():
    print "get query!"
    png_recovered = request.form["img"].decode("base64")
    if png_recovered is None:
        print "no data..."
    else:
        print "get data!"

    # cStringIOオブジェクト（ファイルのように文字列を読み書きできる）に変換する必要がある
    image_string = cStringIO.StringIO(png_recovered)
    print "here1"

    # save as file
    fh = open("tgt.png", "wb")
    fh.write(png_recovered)
    fh.close()

    img = Image.open(image_string)
    print "let's predict!"
    res = []
    try:
        res = ssd.predict(img, pngFilePath="tgt.png")
    except:
        print "error!"
        print "Unexpected error:", sys.exc_info()[0]
    print res

    res2 = []
    for t in res:
        tmp ={}
        tmp["rect"] = t[0]
        tmp["class"] = int(t[1][0])
        res2.append(tmp)
    return json.dumps(res2)

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5000)
