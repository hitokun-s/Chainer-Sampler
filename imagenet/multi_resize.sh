#!/usr/bin/env bash
echo start!
# mogrify -resize 256x256 images/*.jpg
# これだとargument list too long になってしまう

i=1
for imgfile in $( ls images ); do
    echo $i
    echo "images/$imggile"
    mogrify -resize 256x256 "images/$imggile"

    # iを$i+1で上書きする
    i=$((i+1))
done

pause