#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import six
import collections, pickle, os

import nltk, re, string
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from functools import wraps

# nltk.download() <= 1回だけ実行してダウンロードしておけばOK

# stop word list
stop_words = nltk.corpus.stopwords.words('english')
print stop_words # 人称代名詞、be動詞、疑問詞、助動詞、前置詞、などなど

regex = re.compile('[%s]' % re.escape(string.punctuation)) #see documentation here: http://docs.python.org/2/library/string.html

lemmatizer =nltk.WordNetLemmatizer()

def process(sentences):
    result = []
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    for review in tokenized_sentences:
        new_review = []
        for token in review:
            new_token = regex.sub(u'', token)
            if not new_token == u'' and not new_token in stop_words:
                if len(wordnet.lemmas(new_token)) > 0:
                    new_review.append(lemmatizer.lemmatize(new_token))
            # new_token = regex.sub('', token)
            # if not new_token == '' and not new_token in stop_words:
            #     new_review.append(new_token)
        result.append(new_review)
    return result

curr_dir = os.path.dirname(__file__)

def doExec():
    index2word = {} # 順引辞書
    word2index = {} # 逆引辞書

    # 出現回数辞書（キーは単語ID）
    counts = collections.Counter()

    # 文書全体を単語IDリストに変換したもの
    dataset = []

    def process_line(contents):
        res = process(contents.split(".")) # resは、配列の配列になる
        words = []
        for r in res:
            words.extend(r)
        for word in words:
            # 新出単語だったら、順引辞書、逆引辞書に登録
            if word not in word2index:
                ind = len(word2index)
                word2index[word] = ind # 新出単語にIDを付与
                index2word[ind] = word # ID辞書に登録
            counts[word2index[word]] += 1 # 出現回数をカウント
            dataset.append(word2index[word]) # 単語IDを全体データに追加

    isData = False
    cnt = 0

    fileNames = os.listdir(curr_dir + "/data/raw")
    for fileName in fileNames:
        print "let's go to : " + fileName
        with open(curr_dir + "/data/raw/" + fileName) as f:
            for line in f:
                if line.startswith("<doc"):
                    isData = True
                    continue
                if line.count("</doc>") > 0:
                    isData = False
                    data = ""
                    cnt = cnt + 1
                    continue
                try:
                    process_line(line.encode('utf-8', 'ignore'))
                except:
                    pass
                    # print "utf-8 encode error!"
                    # print line


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
    return data

if __name__ == '__main__':
    f = open(curr_dir + "/data/pickle.dump", "w")
    data = doExec()
    print "go!"
    print len(data["word2index"])
    # 何も工夫をしないと、englishText_0_10000ファイルだけで17万語彙になってしまったが、その多くは、数字とか固有名詞というゴミデータだった
    # そこで、lemmatizeを行うとともに、wordnetに見出し語が存在しない語を捨てたら、語彙数は48000になった。
    pickle.dump(data, f)
    f.close()

    for w in data["word2index"]:
        print w