<?php
 
//ヘッダに「data:image/png;base64,」が付いているので、それは外す
//$canvas = preg_replace("/data:image/png;base64,/i","",$canvas);
 
//残りのデータはbase64エンコードされているので、デコードする
$img = base64_decode($_POST["img"]);

//まだ文字列の状態なので、画像リソース化
$image = imagecreatefromstring($img);
 
//画像として保存（ディレクトリは任意）
imagepng($image ,"image/oekaki.png");

$url = "127.0.0.1";
$port = 8082;
$timeout = 10;
$fp = fsockopen( $url, $port, $errno, $errstr, $timeout );
  if( !$fp || $errno > 0 ) {
    print( "$errno ($errstr) \n" );
    exit();
  }

$send_text =$_POST["img"];
//echo $send_text;

fwrite( $fp, $send_text );
echo fgets($fp, 4096);

fclose( $fp );
?>
