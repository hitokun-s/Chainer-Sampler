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



    


