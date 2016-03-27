#!/usr/bin/env bash
echo start!
# mogrify -resize 256x256 images/*.jpg
# これだとargument list too long になってしまう

i=1
for imgfile in $( ls images ); do
    echo $i
    echo images/$imggile
#    これだと長軸編が256になるだけで、リサイズになって、正方形になってくれない
#    mogrify -resize 256x256 images/${imgfile}
# refs: http://blog.knazsky.com/post/102867716507/create-square-thumbnails-with-imagemagic
    mogrify -resize 256x256 -gravity center -crop 256x256+0+0 +repage -format jpg -quality 75 images/${imgfile}

    # iを$i+1で上書きする
    i=$((i+1))
done

pause