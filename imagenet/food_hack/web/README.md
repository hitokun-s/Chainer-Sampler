##Canvasでのクリック位置取得

[http://www.sist.ac.jp/~kanakubo/programming/canvas/canvas5.html](http://www.sist.ac.jp/~kanakubo/programming/canvas/canvas5.html)
[http://d.hatena.ne.jp/sandai/20091105/p1](http://d.hatena.ne.jp/sandai/20091105/p1)  

##注意点

event.clientX/Yだと、ブラウザ描画部分の左上を基点にとる。  
=> canvas内の位置取得で画面全体がスクロールされる場合には使えない！

