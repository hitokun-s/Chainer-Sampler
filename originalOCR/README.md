##参考資料  

Chainerでmnistで畳込みネットワーク：  
[http://aidiary.hatenablog.com/entry/20151007/1444223445](http://aidiary.hatenablog.com/entry/20151007/1444223445)  

ChainerでCIFAR-10:  
[http://aidiary.hatenablog.com/entry/20151108/1446952402](http://aidiary.hatenablog.com/entry/20151108/1446952402)  

畳み込み層の入出力で、サイズWがどう変わるかの公式：  

    W = (W - 2 * [H / 2]) / stride 
    
    ※H:ウィンドウ（＝フィルタ）サイズ
    ※⌊⋅⌋は小数点以下切り下げて整数化する演算