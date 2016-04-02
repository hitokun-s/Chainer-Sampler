#!/usr/bin/env python
# -*- coding: utf-8 -*-

api_base = "http://www.image-net.org/api"

# 全ての子孫synsetを取得
api_all_sub_synset = api_base + "/text/wordnet.structure.hyponym?full=1&wnid=%(wnid)s"

# 画像IDと画像URLのセットのリストを取得
api_img_urls_with_id = api_base + "/text/imagenet.synset.geturls.getmapping?wnid=%(wnid)s"

# あるwnidに属する各画像のbbox情報（xml）をまとめたtar.gzファイルのダウンロードリンク
api_bbox_download = api_base + "/download/imagenet.bbox.synset?wnid=%(wnid)s"

from urllib2 import urlopen
from urllib import urlretrieve
from bs4 import BeautifulSoup
import sqlite3
import tarfile
from bbox_helper import *

conn = sqlite3.connect("food.sqlite")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS material_image (id VARCHAR PRIMARY KEY  NOT NULL , url VARCHAR, file_path VARCHAR, xml_path VARCHAR, wnid VARCHAR, parent_wnid VARCHAR)")


# "n07707451"}) # 野菜

def get_all_sub_synset(wnid):
    f = urlopen(api_all_sub_synset % {"wnid":wnid})
    soup = BeautifulSoup(f, "html.parser")
    return [line[1:] for line in soup.text.strip().split("\n")[1:]]

def download_bbox_xml(wnid):
    savePath = "tmp/%s.tar.gz" % wnid
    if os.path.exists(savePath):
        print "already exists:%s" % savePath
        return
    urlretrieve("http://image-net.org/downloads/bbox/bbox/%s.tar.gz" % wnid, savePath)
    tf = tarfile.open(savePath, "r:gz")
    # 解凍してxmlをdata/bbox以下に移す
    tf.extractall("data/bbox/")
    tf.close()

def isExists(image_id):
    t = (image_id,)
    res = c.execute("select id from material_image where id = ?", t).fetchone()
    return res is not None

def get_img_url_with_id(wnid):
    f = urlopen(api_img_urls_with_id % {"wnid":wnid}) # 野菜
    soup = BeautifulSoup(f, "html.parser")
    lines = soup.text.strip().split("\n")
    print "wnid:" + wnid +   ",count:%d" % len(lines)
    targets = [] # タプルのリストにする
    ext_cnt = 0
    for line in lines:
        id,url = line.split()
        if not isExists(id):
            targets.append((id, url, wnid))
        else:
            ext_cnt += 1
    print "ext cnt:%d" % ext_cnt
    if len(targets) > 0:
        c.executemany("insert into material_image(id, url, wnid) values (?, ?, ?)", targets)
        conn.commit()

# for wnid in get_all_sub_synset("n07707451"):# vegetable
#     print "let's go to:%s" % wnid
#     get_img_url_with_id(wnid)

def del_image(image_id):
    print "deleting image from db:%s" % image_id
    c.execute("delete from material_image where id = ?", (image_id, ))
    imgPath = "data/image/%s.jpg" % image_id
    os.remove(imgPath)

def saveAsBoudingBoxImg(image_id):
    wnid = image_id[:image_id.index("_")]
    print wnid
    xmlFilePath = "data/bbox/Annotation/%s/%s.xml" % (wnid, image_id)
    imgFilePath = "data/image/%s.jpg" % image_id
    try:
        bbhelper = BBoxHelper(xmlFilePath)
    except:
        # もしxmlがなかったらデータを消す
        del_image(image_id)
        print "xml not exists"
        return
    print bbhelper.findImagePath()
    # Search image path according to bounding box xml, and crop it
    print bbhelper.get_BoudingBoxs()
    bbhelper.saveBoundBoxImage(imgPath=imgFilePath, outputFolder="data/bbox_image")

def del_invalid_image(imgPath):
    # 画像ファイルではない場合、もしくは、3kb以下の場合（flickerでの無効画像）に削除する。データも。
    imgName = imgPath.split("/")[-1]
    image_id = imgName[:imgName.index(".")]
    try:
        im = Image.open(imgPath)
        im.verify()
        if os.path.getsize(file) < 4:
            print "delete too small file:%s" % imgPath
            del_image(image_id)
    except:
        print "dele invalid file:%s" % imgPath
        del_image(image_id)

def del_all_invalid_image(dirPath):
    for fileName in os.listdir(dirPath):
        del_invalid_image(dirPath + fileName)

def isValidImageUrl(url):
    try:
        return urlopen(url).code == 200
    except:
        return False

def dowmload_image(wnid):
    c.execute("select id, url from material_image where wnid = ?", (wnid,))
    for row in c:
        imgPath = "data/image/%s.jpg" % row[0]
        if os.path.exists(imgPath):
            print "image exists:%s" % imgPath
            continue
        url = row[1]
        if isValidImageUrl(url):
            urlretrieve(row[1], imgPath)
        # del_invalid_image(imgPath)

# bbox xml is PASCAL VOC format
# https://github.com/tzutalin/ImageNet_Utils というのがある

# del_all_invalid_image("data/image/")

def createBboxImage(wnid):
    c = conn.cursor()
    c.execute("select id from material_image where wnid = ?", (wnid,))
    cnt = 0
    for row in c:
        saveAsBoudingBoxImg(row[0])
        cnt += 1
    print "cnt:%d" % cnt

target_wnid = "n07707451"
get_img_url_with_id(target_wnid)
download_bbox_xml(target_wnid)
dowmload_image(target_wnid)
createBboxImage(target_wnid)

conn.close()



