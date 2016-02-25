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

from nltk.corpus import wordnet

from functools import wraps

def unicode_ignore_invalid_char(text):
    if isinstance(text, str):
        return text.decode('utf-8', 'ignore')
    return text

def str_ignore_invalid_char(text):
    if isinstance(text, unicode):
        return text.encode('utf-8', 'ignore')
    return text

def consistent_texttype(function):
    @wraps(function)
    def _consistent_texttype(*args, **kwargs):
        assert(1 <= len(args))
        input_text = args[0]
        is_unicode = False
        if isinstance(input_text, unicode):
            is_unicode = True
        elif not isinstance(input_text, str):
            is_unicode = isinstance(input_text[0], unicode)  # for collections
        output_text = function(*args, **kwargs)
        if isinstance(output_text, unicode) or isinstance(output_text, str):
            if is_unicode:
                return unicode_ignore_invalid_char(output_text)
            return str_ignore_invalid_char(output_text)
        if is_unicode:
            return map(unicode_ignore_invalid_char, output_text)
        return map(str_ignore_invalid_char, output_text)
    return _consistent_texttype

@consistent_texttype
def lemmatize_term(term, pos=None):
    if pos is None:
        synsets = wordnet.synsets(term)
        if not synsets:
            return term
        pos = synsets[0].pos
        if pos == wordnet.ADJ_SAT:
            pos = wordnet.ADJ
    assert(pos in (wordnet.NOUN, wordnet.VERB, wordnet.ADJ, wordnet.ADV))
    return nltk.WordNetLemmatizer().lemmatize(term, pos=pos)

lemmatizer =nltk.WordNetLemmatizer()


print process(["I am a dog, who is running on the ground, with a flying sourcer."])

print lemmatizer.lemmatize('men')
print wordnet.lemmas('men')

print lemmatizer.lemmatize('1234')
assert len(wordnet.lemmas('1234')) == 0
assert len(wordnet.synsets('1234')) == 0