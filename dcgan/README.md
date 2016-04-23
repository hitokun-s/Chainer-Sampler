original:[https://github.com/mattya/chainer-DCGAN](https://github.com/mattya/chainer-DCGAN)  

##リソース画像のサイズ一括変更

ImageMagickを使ったbatファイルを作成した（multi_resize.bat）  

リサイズしつつフォーマットも変える例：  

    mogrify -resize 96x96 -format png images/*.jpg

##deconvolution netweok

[http://cvlab.postech.ac.kr/research/deconvnet](http://cvlab.postech.ac.kr/research/deconvnet)

##トラブルシューティング

$DISPLAY環境変数未定義エラーが出た場合： 
 
    _tkinter.TclError: no display name and no $DISPLAY environment variable
     
[http://qiita.com/nishio/items/0a8949262d86c181668b](http://qiita.com/nishio/items/0a8949262d86c181668b)  

このエラーが出たら、  

    ln -s /usr/bin/nodejs /usr/bin/node
    
[https://github.com/nodejs/node-v0.x-archive/issues/3911](https://github.com/nodejs/node-v0.x-archive/issues/3911)  
に従って、  

    sudo ln -s /usr/bin/nodejs /usr/bin/node
    
このエラー：  

    OSError: Failed to run `nvcc` command. Check PATH environment variable: [Errno 2] No such file or directory: 'nvcc'
 
が出たら、[http://studylog.hateblo.jp/entry/2016/01/07/161543](http://studylog.hateblo.jp/entry/2016/01/07/161543)  


