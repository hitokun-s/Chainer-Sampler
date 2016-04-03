#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cStringIO
import traceback, sys, os

from flask import Flask, request, send_from_directory
from flask import jsonify
import ssd
from PIL import Image

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

    png_recovered = request.form["img"].decode("base64")

    # cStringIOオブジェクト（ファイルのように文字列を読み書きできる）に変換する必要がある
    image_string = cStringIO.StringIO(png_recovered)
    img = Image.open(image_string)
    res = ssd.predict(img)
    return jsonify(res)
    #
    # grayScaled = toGrayScale(numPyToPIL(img))
    # standardized = standardize(grayScaled)
    # grayed = pilToNumPy(standardized)
    # grayed = binarize(grayed)  # 戻り値はndarray
    # if should_invert(grayed):
    #     grayed = invert(grayed)
    # try:
    #     prediction = predict(np.array([grayed]))
    #     classIdx = prediction[0][0]
    #     confidence = prediction[1][0]
    #     answer = class_labels[classIdx]
    #     print answer
    # except:
    #     print traceback.format_exc() # stacktrace
    #
    # return jsonify(dict(answer=answer, confidence=int(confidence * 100)))


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5000)
