#! /usr/bin/env python

import os
import sys

from PIL import Image
import ete2

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
((((mascot-georgia-bulldog.jpg:0.01,mascot-mississippi-state-bulldog.gif:0.01):0.03,mascot-texas-am-reveille.gif:0.04):0.08,mascot-tennessee-smokey.png:0.12):0.22,mascot-ole-miss-rebel-black-bear.jpg:0.34):0.06):0.005,
mascot-arkansas-razorback.png:0.405):0.045,
mascot-vanderbilt-commodore-cartoon.gif:0.45):0.025,
mascot-alabama-big-al.gif:0.475):0.015,
(mascot-sc-gamecock.png:0.33,mascot-florida-gator.png:0.33):0.16):0.08,
mascot-georgia-tech-yellow-jacket.png:{mascot-georgia-tech-yellow-jacket}):0.02,
mascot-tulane-green-wave.png:{mascot-tulane-green-wave}):0.01;
""".format(**_extinct_lengths)
_sec_tree = """
(mascot-tulane-green-wave.png:{mascot-tulane-green-wave},(mascot-georgia-tech-yellow-jacket.png:{mascot-georgia-tech-yellow-jacket},(((((((((mascot-auburn-tiger.png:0.03,mascot-lsu-tiger.jpg:0.03):0.04,mascot-missouri-tiger.png:0.07):0.12,mascot-sewanee-tiger.jpg:{mascot-sewanee-tiger}):0.13,mascot-kentucky-wild-cat.jpg:0.32):0.08,
((((mascot-georgia-bulldog.jpg:0.01,mascot-mississippi-state-bulldog.gif:0.01):0.03,mascot-texas-am-reveille.gif:0.04):0.08,mascot-tennessee-smokey.png:0.12):0.22,mascot-ole-miss-rebel-black-bear.jpg:0.34):0.06):0.005,
mascot-arkansas-razorback.png:0.405):0.045,
mascot-vanderbilt-commodore-cartoon.gif:0.45):0.025,
mascot-alabama-big-al.gif:0.475):0.015,
(mascot-sc-gamecock.png:0.33,mascot-florida-gator.png:0.33):0.16):0.08
):0.02
):0.01;
""".format(**_extinct_lengths)
_sec_tree_shared = """
(mascot-tulane-green-wave.png:{mascot-tulane-green-wave},(mascot-georgia-tech-yellow-jacket.png:{mascot-georgia-tech-yellow-jacket},(((((((((mascot-auburn-tiger.png:0.04,mascot-lsu-tiger.jpg:0.04):0.03,mascot-missouri-tiger.png:0.07):0.12,mascot-sewanee-tiger.jpg:{mascot-sewanee-tiger}):0.14,mascot-kentucky-wild-cat.jpg:0.33):0.07,
((((mascot-georgia-bulldog.jpg:0.01,mascot-mississippi-state-bulldog.gif:0.01):0.03,mascot-texas-am-reveille.gif:0.04):0.08,mascot-tennessee-smokey.png:0.12):0.21,mascot-ole-miss-rebel-black-bear.jpg:0.33):0.07):0.005,
mascot-arkansas-razorback.png:0.405):0.045,
mascot-vanderbilt-commodore-cartoon.gif:0.45):0.025,
mascot-alabama-big-al.gif:0.475):0.015,
(mascot-sc-gamecock.png:0.33,mascot-florida-gator.png:0.33):0.16):0.08
):0.02
):0.01;
""".format(**_extinct_lengths_shared)

def get_image_path(leaf_name):
    return os.path.join(os.path.pardir, 'images', leaf_name)

def ultrametric(node):
    node.img_style["size"] = 0
    node.img_style["vt_line_width"] = 0

def branch_style(node, weight=10, color="#000000"):
    node.img_style["vt_line_width"] = weight
    node.img_style["hz_line_width"] = weight
    node.img_style["size"] = -weight
    node.img_style["vt_line_color"] = color
    node.img_style["hz_line_color"] = color
    node.img_style["shape"] = "circle"

def mascots_hidden(node):
    mascots(node, opacity = 0.0)

def mascots(node, opacity = 1.0):
    # ultrametric(node)
    branch_style(node, color="#000000")
    if node.is_leaf():
        try:
            img = Image.open(get_image_path(node.name))
        except IOError as e:
            print node.name
            raise e
        w, h = img.size
        width, height = None, 150 
        if w > h:
            width, height = 150, None
        vmargin = 0
        lmargin = 25
        if height is None:
            # vmargin += (width - (width * (float(h)/w)))
            pass
        else:
            lmargin += ((height - (height * (float(w)/h))) * 0.5)
        f = ete2.faces.ImgFace(get_image_path(node.name),
                height = height,
                width = width)
        f.margin_left = lmargin
        f.margin_top = vmargin
        f.margin_bottom = vmargin
        f.opacity = opacity
        ete2.faces.add_face_to_node(f, node,
                column = 0,
                position = "branch-right")
    if os.path.splitext(node.name)[0] in _extinct_lengths.keys():
        node.img_style["shape"] = "circle"
        node.img_style["size"] = 40
        node.img_style["fgcolor"] = "#FF0000"


def main_cli():
    t = ete2.Tree(_sec_tree)
    ts = ete2.TreeStyle()
    ts.show_leaf_name = True
    ts.show_branch_length = False
    # ts.scale = 3600
    ts.tree_width = 3600
    ts.show_leaf_name = False
    ts.show_scale = False
    ts.min_leaf_separation = 150
    t.render("sec-tree.png", layout=mascots, dpi=200, tree_style = ts)
    t = ete2.Tree(_sec_tree)
    ts = ete2.TreeStyle()
    ts.show_leaf_name = True
    ts.show_branch_length = False
    # ts.scale = 3600
    ts.tree_width = 3600
    ts.show_leaf_name = False
    ts.show_scale = False
    ts.min_leaf_separation = 150
    t.render("sec-tree.png", layout=mascots, dpi=300, tree_style = ts)
    t.render("sec-tree-bare.png", layout=mascots_hidden, dpi=300, tree_style = ts)

if __name__ ==  '__main__':
    main_cli()

