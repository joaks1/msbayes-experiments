#! /usr/bin/env python

import os
import sys

from PIL import Image
import ete2

from Gram import TreeGram
var.punctuation = var.phylip_punctuation

_wide_images = ['mascot-missouri-tiger.png',
                'mascot-florida-gator.png',
                'mascot-arkansas-razorback.png',
                ]
_extinct_images = [
        "mascot-sewanee-tiger.jpg",
        "mascot-tulane-green-wave.png",
        "mascot-georgia-tech-yellow-jacket.png",
        ]
_extinct_lengths = {
        "mascot-sewanee-tiger": 0.14,
        "mascot-tulane-green-wave": 0.29,
        "mascot-georgia-tech-yellow-jacket": 0.43,
        }
_extinct_lengths_shared = {
        "mascot-sewanee-tiger": 0.15,
        "mascot-tulane-green-wave": 0.26,
        "mascot-georgia-tech-yellow-jacket": 0.43,
        }
_sec_tree_ladder = """
(((((((((((mascot-auburn-tiger.png:0.03,mascot-lsu-tiger.jpg:0.03):0.04,mascot-missouri-tiger.png:0.07):0.12,mascot-sewanee-tiger.jpg:{mascot-sewanee-tiger}):0.13,mascot-kentucky-wild-cat.jpg:0.32):0.08,
((((mascot-georgia-bulldog.jpg:0.01,mascot-mississippi-state-bulldog.png:0.01):0.03,mascot-texas-am-reveille.png:0.04):0.08,mascot-tennessee-smokey.png:0.12):0.22,mascot-ole-miss-rebel-black-bear.jpg:0.34):0.06):0.005,
mascot-arkansas-razorback.png:0.405):0.045,
mascot-vanderbilt-commodore-cartoon.png:0.45):0.025,
mascot-alabama-big-al.png:0.475):0.015,
(mascot-sc-gamecock.png:0.33,mascot-florida-gator.png:0.33):0.16):0.08,
mascot-georgia-tech-yellow-jacket.png:{mascot-georgia-tech-yellow-jacket}):0.02,
mascot-tulane-green-wave.png:{mascot-tulane-green-wave}):0.01;
""".format(**_extinct_lengths)
_sec_tree = """
(mascot-tulane-green-wave.png:{mascot-tulane-green-wave},(mascot-georgia-tech-yellow-jacket.png:{mascot-georgia-tech-yellow-jacket},(((((((((mascot-auburn-tiger.png:0.03,mascot-lsu-tiger.jpg:0.03):0.04,mascot-missouri-tiger.png:0.07):0.12,mascot-sewanee-tiger.jpg:{mascot-sewanee-tiger}):0.13,mascot-kentucky-wild-cat.jpg:0.32):0.08,
((((mascot-georgia-bulldog.jpg:0.01,mascot-mississippi-state-bulldog.png:0.01):0.03,mascot-texas-am-reveille.png:0.04):0.08,mascot-tennessee-smokey.png:0.12):0.22,mascot-ole-miss-rebel-black-bear.jpg:0.34):0.06):0.005,
mascot-arkansas-razorback.png:0.405):0.045,
mascot-vanderbilt-commodore-cartoon.png:0.45):0.025,
mascot-alabama-big-al.png:0.475):0.015,
(mascot-sc-gamecock.png:0.33,mascot-florida-gator.png:0.33):0.16):0.08
):0.02
):0.01;
""".format(**_extinct_lengths)
_sec_tree_shared = """
(mascot-tulane-green-wave.png:{mascot-tulane-green-wave},(mascot-georgia-tech-yellow-jacket.png:{mascot-georgia-tech-yellow-jacket},(((((((((mascot-auburn-tiger.png:0.04,mascot-lsu-tiger.jpg:0.04):0.03,mascot-missouri-tiger.png:0.07):0.12,mascot-sewanee-tiger.jpg:{mascot-sewanee-tiger}):0.14,mascot-kentucky-wild-cat.jpg:0.33):0.07,
((((mascot-georgia-bulldog.jpg:0.01,mascot-mississippi-state-bulldog.png:0.01):0.03,mascot-texas-am-reveille.png:0.04):0.08,mascot-tennessee-smokey.png:0.12):0.21,mascot-ole-miss-rebel-black-bear.jpg:0.33):0.07):0.005,
mascot-arkansas-razorback.png:0.405):0.045,
mascot-vanderbilt-commodore-cartoon.png:0.45):0.025,
mascot-alabama-big-al.png:0.475):0.015,
(mascot-sc-gamecock.png:0.33,mascot-florida-gator.png:0.33):0.16):0.08
):0.02
):0.01;
""".format(**_extinct_lengths_shared)

def get_image_path(leaf_name):
    return os.path.join(os.path.pardir, 'images', leaf_name)

def plot_tree(tree, base_name = 'tree', dir_name = 'gram', show_events = False):
    read(tree)
    print var.trees
    t = var.trees[-1]
    for n in t.iterNodes():
        if n.isLeaf:
            try:
                img = Image.open(get_image_path(n.name))
            except IOError as e:
                print n.name
                raise e
            w, h = img.size
            width, height = None, 6.5
            if w > h and (n.name in _wide_images):
                width, height = 8, None
            vmargin = 0
            lmargin = 9
            dimension_name = 'height'
            dimension = height
            if height is None:
                dimension_name = 'width'
                dimension = width
            node_name = n.name
            if node_name in _extinct_images:
                lmargin += 2
            n.name = r"\hspace{{{0}mm}}\includegraphics[{1}={2}mm,resolution=150]{{{3}}}".format(
                    lmargin,
                    dimension_name,
                    dimension,
                    get_image_path(node_name))

    tg = TreeGram(t, yScale=0.65, widthToHeight=1.3)
    tg.tgDefaultLineThickness = 'very thick'
    tg.baseName = base_name
    tg.dirName = dir_name
    l1 = tg.gramLine(6.34,-0.5,6.34,11)
    # l1.lineStyle = 'loosely dashed'
    # l1.lineThickness = 'ultra thick'
    l1.lineThickness = 10.0
    l2 = tg.gramLine(13.4,-0.5,13.4,11)
    # l2.lineStyle = 'loosely dashed'
    # l2.lineThickness = 'ultra thick'
    l2.lineThickness = 10.0
    l1.colour = 'black!40'
    l2.colour = 'black!40'
    if not show_events:
        # print dir(l1)
        l1.colour = 'black!00'
        l2.colour = 'black!00'
    s = tg.code(r"""\draw [draw=none] (10.97, 9.75) node[circle, minimum width=10pt, draw=none, inner sep=0pt, path picture={\draw[red] (path picture bounding box.south east) -- (path picture bounding box.north west) (path picture bounding box.south west) -- (path picture bounding box.north east);}] {};""")
    if tree == _sec_tree:
        s = tg.code(r"""\draw [draw=none] (7.08, 10.4) node[circle, minimum width=10pt, draw=none, inner sep=0pt, path picture={\draw[red] (path picture bounding box.south east) -- (path picture bounding box.north west) (path picture bounding box.south west) -- (path picture bounding box.north east);}] {};""")
        s = tg.code(r"""\draw [draw=none] (13.17, 7.15) node[circle, minimum width=10pt, draw=none, inner sep=0pt, path picture={\draw[red] (path picture bounding box.south east) -- (path picture bounding box.north west) (path picture bounding box.south west) -- (path picture bounding box.north east);}] {};""")
    else:
        s = tg.code(r"""\draw [draw=none] (6.34, 10.4) node[circle, minimum width=10pt, draw=none, inner sep=0pt, path picture={\draw[red] (path picture bounding box.south east) -- (path picture bounding box.north west) (path picture bounding box.south west) -- (path picture bounding box.north east);}] {};""")
        s = tg.code(r"""\draw [draw=none] (13.4, 7.15) node[circle, minimum width=10pt, draw=none, inner sep=0pt, path picture={\draw[red] (path picture bounding box.south east) -- (path picture bounding box.north west) (path picture bounding box.south west) -- (path picture bounding box.north east);}] {};""")
    tg.epdf()


def main_cli():
    out_dir = os.path.join(os.path.pardir, 'mascot-tree')
    plot_tree(_sec_tree,
            base_name = 'mascot-tree',
            dir_name = out_dir,
            show_events = False)
    plot_tree(_sec_tree_shared,
            base_name = 'mascot-tree-shared',
            dir_name = out_dir,
            show_events = False)
    plot_tree(_sec_tree_shared,
            base_name = 'mascot-tree-shared-events',
            dir_name = out_dir,
            show_events = True)

if __name__ ==  '__main__':
    main_cli()

