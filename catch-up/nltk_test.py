#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk, re, string
from nltk.tokenize import word_tokenize

# nltk.download() <= 1回だけ実行してダウンロードしておけばOK

# stop word list
stop_words = nltk.corpus.stopwords.words('english')
print stop_words # 人称代名詞、be動詞、疑問詞、助動詞、前置詞、などなど

regex = re.compile('[%s]' % re.escape(string.punctuation)) #see documentation here: http://docs.python.org/2/library/string.html

def process(sentences):
    result = []
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    for review in tokenized_sentences:
        new_review = []
        for token in review:
            # new_token = regex.sub(u'', token)
            # if not new_token == u'' and not new_token in stop_words:
            #     new_review.append(new_token)
            new_token = regex.sub('', token)
            if not new_token == '' and not new_token in stop_words:
                new_review.append(new_token)
        result.append(new_review)
    return result

print process(["I am a dog, who is running on the ground, with a flying sourcer."])