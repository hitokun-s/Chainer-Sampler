参考：[http://hi-king.hatenablog.com/entry/2015/06/11/021144](http://hi-king.hatenablog.com/entry/2015/06/11/021144)  
の通りにやってみる。  
ただしcrop.pyについては、cv2のinstallが面倒そうだったので、PIL,pltで代用するように修正した。  

##train_imagenet.pyについて

デフォルト仕様：  

- 終了すると、モデルデータが、model, stateというファイルとして保存される

複数スレッドで作業分担してQueueで管理している：  

    # This example consists of three threads: data feeder, logger and trainer.
    # These communicate with each other via Queue.
    
##なんかいろんな学習モデルがあるっぽい

[https://github.com/BVLC/caffe/wiki/Model-Zoo](https://github.com/BVLC/caffe/wiki/Model-Zoo)  

##ninモデル

デフォルトだと、  

    if args.arch == 'nin':
        import nin
        model = nin.NIN()
        
に従う。

鍵はここらへん。  

    x = chainer.Variable(xp.asarray(inp[0]), volatile=volatile)
    t = chainer.Variable(xp.asarray(inp[1]), volatile=volatile)
    
            if model.train:
                optimizer.update(model, x, t)
                if not graph_generated:
                    with open('graph.dot', 'w') as o:
                        o.write(computational_graph.build_computational_graph(
                            (model.loss,)).dump())
                    print('generated graph', file=sys.stderr)
                    graph_generated = True
            else:
                model(x, t)

ここでxを作っているinp\[0\]が何かというと、  

    inp = data_q.get()

で、あとは、

    path, label = train_list[idx]
    batch_pool[i] = pool.apply_async(read_image, (path, False, True))
    y_batch[i] = label
    i += 1
                
    for j, x in enumerate(batch_pool):
       x_batch[j] = x.get()
    data_q.put((x_batch.copy(), y_batch.copy()))
    
ということなので、要は、read_image(path, False, True)の結果が、配列となって、x_batchができている。  

x_batchの型をみておく。  

    x_batch = np.ndarray((args.batchsize, 3, model.insize, model.insize), dtype=np.float32)
    
ここで、insizeとは、ninモデルなら227になっている。  
まあそのへんは気にしなくても、read_image()を通せば、(3,227,227)になってくれるんだろうきっと。



## 画像検索API
    
imagenet:  
[http://image-net.org/download-imageurls](http://image-net.org/download-imageurls)  
wordnetと連携しているプロジェクト。  

例：lemon  
[http://image-net.org/synset?wnid=n07749582](http://image-net.org/synset?wnid=n07749582)  
すごい！  
画像URLダウンロードリンク：  
http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07749582  

wordnet分類で、今回対象とすべきもの：  

- 果物=> reproductive_structure(421) => fruit(320) （例：lemon）   
- 野菜=> misc(20400) （例：cucumber）  

vegetableという項目がない！？いや、imagenetトップにはvegetableという項目があるよ？  
わかった。。。cucumberは、misc直下にもあるし、misc > vegetable(n07718472) > cucumber にもある！    
そうか、これが「1項目が複数の上位項目にひもづく」ということか。  
vegetable(id:n07718472)には175種類がある。
fruit(id:n07749582)には320種類がある。
どうでもいいがスイカはどっちだろう？  
wordnetのsynset階層検索方法が知りたい。wnidをたどるために。  
  
これだ！  
[http://image-net.org/download-API](http://image-net.org/download-API)  

参考記事：  
http://aial.shiroyagi.co.jp/2014/12/%E3%83%87%E3%82%A3%E3%83%BC%E3%83%97%E3%83%A9%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%81%AE%E5%88%87%E3%82%8A%E6%8A%9C%E3%81%8D/
このpyDataの発表会おもしろそうだな。  
imageNet2013での学習モデルは、200種類の物体を認識できる。  
この中に野菜、果物があればそのまま使えるのだけど。。。  
その200カテゴリの内容がこちら。  
http://www.image-net.org/challenges/LSVRC/2013/browse-det-synsets  

=> lemon, apple, orange, banana, cucumberなどはある。carrot,melon,onion,grape,peachはない。うーん。。。  

Image|Net2015ではどうなっているのか？  
http://image-net.org/challenges/LSVRC/2015/  
1000カテゴリというのがある。  
http://image-net.org/challenges/LSVRC/2015/browse-synsets  
でもやっぱり、上記のなかったやつはない。  








