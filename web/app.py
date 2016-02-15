#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cStringIO
import traceback

from flask import Flask, request, send_from_directory

from char74k.binarize import *
from originalOCR.predict import *

app = Flask(__name__, static_url_path='/static')


# app = Flask(__name__)

@app.route('/<path:path>')
def send_js(path):
    if path is None:
        path = "index.html"
    return send_from_directory('', path)

class_labels = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

@app.route('/query', methods=['POST'])
def query():
    png_recovered = request.form["img"].decode("base64")

    # cStringIOオブジェクト（ファイルのように文字列を読み書きできる）に変換する必要がある
    image_string = cStringIO.StringIO(png_recovered)
    img = Image.open(image_string)

    grayScaled = toGrayScale(numPyToPIL(img))
    standardized = standardize(grayScaled)
    grayed = pilToNumPy(standardized)
    grayed = binarize(grayed)  # 戻り値はndarray
    if should_invert(grayed):
        grayed = invert(grayed)
    print grayed
    try:
        classIdx = predict(np.array([grayed]))[0][0]
        answer = class_labels[classIdx]
    except:
        print traceback.format_exc()

    return answer


if __name__ == '__main__':
    app.run()
