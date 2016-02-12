official:  
[http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/](http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/)  

ref:  
[http://www.wjxfpf.com/2015/10/290442.html](http://www.wjxfpf.com/2015/10/290442.html)  

重みを可視化している例  
[http://aidiary.hatenablog.com/entry/20151007/1444223445](http://aidiary.hatenablog.com/entry/20151007/1444223445)  

matlabplotで画像を読み込む  
[http://daemon.ice.uec.ac.jp/~shouno/2012.Programming/ImageHandling.html](http://daemon.ice.uec.ac.jp/~shouno/2012.Programming/ImageHandling.html)  
=> pngしかダメ、とあるが、下記ドキュメントではbmp等でも対応してくれるらしい。  
bmpを読む例    
[http://www.mathworks.com/matlabcentral/newsreader/view_thread/9665](http://www.mathworks.com/matlabcentral/newsreader/view_thread/9665)  

でも実行すると、確かにエラーになる。  

> ValueError: Only know how to handle extensions: [u'png']; with Pillow installed matplotlib can handle more images

[http://stackoverflow.com/questions/8827016/matplotlib-savefig-in-jpeg-format](http://stackoverflow.com/questions/8827016/matplotlib-savefig-in-jpeg-format)  
に従って、  

    pip install pillow
    
を実行するとbmpファイルでもできた！  
imread()は、RGB配列の配列を返す。dtypeは「uint8」  

手動でグレースケール化  
[https://samarthbhargav.wordpress.com/2014/05/05/image-processing-with-python-rgb-to-grayscale-conversion/](https://samarthbhargav.wordpress.com/2014/05/05/image-processing-with-python-rgb-to-grayscale-conversion/) 

numpyとPILを共用する  
[http://d.hatena.ne.jp/white_wheels/20100322/p1](http://d.hatena.ne.jp/white_wheels/20100322/p1)  
pip install pilがエラーになると思ったら、pillowっていうのはpilのforkらしい  
[http://stackoverflow.com/questions/20060096/installing-pil-with-pip](http://stackoverflow.com/questions/20060096/installing-pil-with-pip)  

ので、すでにpillowを入れているのなら、PILは使えるってこと！






  

