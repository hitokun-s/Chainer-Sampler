# Word Embedding

This is an example of word embedding.
We impelmented Mikolov's Skip-gram model and Continuous-BoW model with Hierarhcical softmax and Negative sampling.

First use `../ptb/download.py` to download `ptb.train.txt`.
And then, run `train_word2vec.py` to train and get `model.pickle` which includes embedding data.
You can find top-5 nearest embedding vectors using `search.py`.

This example is based on the following word embedding implementation in C++.
https://code.google.com/p/word2vec/

参考：  
[http://chainernlpman.hatenablog.com/entry/2015/12/02/022151](http://chainernlpman.hatenablog.com/entry/2015/12/02/022151)  

# 英語コーパス

[http://www.cs.upc.edu/~nlp/wikicorpus/](http://www.cs.upc.edu/~nlp/wikicorpus/)  

アイデア：  
rawでそのままword2vecを実行すると、語彙数が1億超になってしまいメモリエラーで実行できない。  
taggedデータの2つ目（lemmatizedのやつ）を用いて、かつ英語辞書に登録のないもの（変な数字とか）は除く。  

