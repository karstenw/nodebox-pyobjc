"""
==========
Agg Buffer
==========

Use backend agg to access the figure canvas as an RGB string and then
convert it to an array and pass it to Pillow for rendering.
"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

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
    def pltshow(plt, dpi=150):
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

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow must be installed to run this example")

plt.plot([1, 2, 3])

canvas = plt.get_current_fig_manager().canvas

agg = canvas.switch_backends(FigureCanvasAgg)
agg.draw()
s = agg.tostring_rgb()

# get the width and the height to resize the matrix
l, b, w, h = agg.figure.bbox.bounds
w, h = int(w), int(h)

X = np.fromstring(s, np.uint8).reshape((h, w, 3))

try:
    im = Image.fromstring("RGB", (w, h), s)
except Exception:
    im = Image.frombytes("RGB", (w, h), s)

# Uncomment this line to display the image using ImageMagick's
# `display` tool.
# im.show()
pltshow(plt)