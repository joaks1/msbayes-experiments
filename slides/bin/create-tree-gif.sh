#!/bin/bash

# Run tree plotting script
python plot-sec-tree.py

# frame_dir="../images/mascot-tree-animation-frames"
# if [ ! -d "$frame_dir" ]
# then
#     mkdir -p "$frame_dir"
# fi


# Get the dimensions of the tree png
dimensions="$(identify sec-tree-bare.png | egrep -o ' [0-9]+x[0-9]+ ')"
dimensions=${dimensions/ /}
width=${dimensions/x*/}
height=${dimensions/*x/}

slice=$(expr $width / 100)

# Create series of masked tree pngs
# cnt=0
for i in $(seq -w 0 $slice $width)
do
    current_width=$(expr $width - $i)
    echo "$i of $width"
    convert sec-tree-bare.png -alpha set -region "${current_width}x${height}+${i}+0" -alpha transparent mt-${i}.png
    # cp "mt-${i}.png" "${frame_dir}/mascot-tree-frame-${cnt}.png"
    # cnt=$(expr $cnt + 1)
done

# cp sec-tree-bare.png "${frame_dir}/mascot-tree-frame-${cnt}.png"
# cnt=$(expr $cnt + 1)
# cp sec-tree.png "${frame_dir}/mascot-tree-frame-${cnt}.png"

# Create gif from png files
convert -layers OptimizePlus -delay 5 mt-*.png sec-tree-bare.png -delay 250 sec-tree.png -loop 0 ../images/mascot-tree.gif

# convert -background white -alpha remove -layers OptimizePlus -delay 5 mt-*.png sec-tree-bare.png -delay 250 sec-tree.png -loop 0 ../images/mascot-tree2.gif

mv sec-tree.png ../images/mascot-tree.png
mv sec-tree-bare.png ../images/mascot-tree-bare.png

# Remove intermediate files
rm mt-*.png
