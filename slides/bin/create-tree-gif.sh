#!/bin/bash

python plot-sec-tree.py

dimensions="$(identify sec-tree-bare.png | egrep -o ' [0-9]+x[0-9]+ ')"
dimensions=${dimensions/ /}
width=${dimensions/x*/}
height=${dimensions/*x/}

slice=$(expr $width / 100)

for i in $(seq -w 0 $slice $width)
do
    current_width=$(expr $width - $i)
    echo "$i of $width"
    convert sec-tree-bare.png -alpha set -region "${current_width}x${height}+${i}+0" -alpha transparent mt-${i}.png
done

convert -layers OptimizePlus -delay 5 mt-*.png sec-tree-bare.png -delay 250 sec-tree.png -loop 0 ../images/mascot-tree.gif

convert -background white -alpha remove -layers OptimizePlus -delay 5 mt-*.png sec-tree-bare.png -delay 250 sec-tree.png -loop 0 ../images/mascot-tree2.gif

mv sec-tree.png ../images/mascot-tree.png

rm sec-tree-bare.png mt-*.png
