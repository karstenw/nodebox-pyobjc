"""
============
Artist tests
============

Test unit support with each of the Matplotlib primitive artist types.

The axis handles unit conversions and the artists keep a pointer to their axis
parent. You must initialize the artists with the axis instance if you want to
use them with unit data, or else they will not know how to convert the units
to scalars.

.. only:: builder_html

   This example requires :download:`basic_units.py <basic_units.py>`
"""
import random
import matplotlib.lines as lines
import matplotlib.patches as patches
import matplotlib.text as text
import matplotlib.collections as collections

from basic_units import cm, inch
import numpy as np
import matplotlib.pyplot as plt


# nodebox section
if __name__ == '__builtin__':
    # were in nodebox
    import os
    import tempfile
    W = 800
    inset = 20
    size(W, 600)
    plt.cla()
    plt.clf()
    plt.close('all')
    def tempimage():
        fob = tempfile.NamedTemporaryFile(mode='w+b', suffix='.png', delete=False)
        fname = fob.name
        fob.close()
        return fname
    imgx = 20
    imgy = 0
    def pltshow(plt, dpi=300):
        global imgx, imgy
        temppath = tempimage()
        plt.savefig(temppath, dpi=dpi)
        dx,dy = imagesize(temppath)
        w = min(W,dx)
        image(temppath,imgx,imgy,width=w)
        imgy = imgy + dy + 20
        os.remove(temppath)
        size(W, HEIGHT+dy+40)
else:
    def pltshow(mplpyplot):
        mplpyplot.show()
# nodebox section end

fig, ax = plt.subplots()
ax.xaxis.set_units(cm)
ax.yaxis.set_units(cm)

# Fixing random state for reproducibility
np.random.seed(19680801)

if 0:
    # test a line collection
    # Not supported at present.
    verts = []
    for i in range(10):
        # a random line segment in inches
        verts.append(zip(*inch*10*np.random.rand(2, random.randint(2, 15))))
    lc = collections.LineCollection(verts, axes=ax)
    ax.add_collection(lc)

# test a plain-ol-line
line = lines.Line2D([0*cm, 1.5*cm], [0*cm, 2.5*cm],
                    lw=2, color='black', axes=ax)
ax.add_line(line)

if 0:
    # test a patch
    # Not supported at present.
    rect = patches.Rectangle((1*cm, 1*cm), width=5*cm, height=2*cm,
                             alpha=0.2, axes=ax)
    ax.add_patch(rect)


t = text.Text(3*cm, 2.5*cm, 'text label', ha='left', va='bottom', axes=ax)
ax.add_artist(t)

ax.set_xlim(-1*cm, 10*cm)
ax.set_ylim(-1*cm, 10*cm)
# ax.xaxis.set_units(inch)
ax.grid(True)
ax.set_title("Artists with units")
pltshow(plt)
