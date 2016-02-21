#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import six
import collections, pickle, os

index2word = {} # 順引辞書
word2index = {} # 逆引辞書

# 出現回数辞書（キーは単語ID）
counts = collections.Counter()

# 文書全体を単語IDリストに変換したもの
dataset = []

def process_line(line):
    for word in line.split(): # スペースで分割
        # 新出単語だったら、順引辞書、逆引辞書に登録
        if word not in word2index:
            ind = len(word2index)
            word2index[word] = ind # 新出単語にIDを付与
            index2word[ind] = word # ID辞書に登録
        counts[word2index[word]] += 1 # 出現回数をカウント
        dataset.append(word2index[word]) # 単語IDを全体データに追加

isData = False
cnt = 0

fileNames = os.listdir("data/raw")
for fileName in fileNames:
    print "let's go to : " + fileName
    with open("data/raw/" + fileName) as f:
        for line in f:
            if line.startswith("<doc"):
                isData = True
                continue
            if line.count("</doc>") > 0:
                isData = False
                data = ""
                cnt = cnt + 1
                continue
            process_line(line)

print len(dataset)
print len(index2word)

# with open('data/ptb.train.txt') as f:
#     for line in f:
#         process_line(line)\

# ファイルに保存
data = {
    "index2word":index2word,
    "word2index":word2index,
    "dataset":dataset,
    "counts":counts
}
f = open("data/pickle.dump", "w")
pickle.dump(data, f)
f.close()