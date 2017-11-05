"""
================
Simple Axisline2
================

"""
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
import numpy as np

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

fig = plt.figure(1, (8, 6))

# a subplot with two additional axis, "xzero" and "yzero". "xzero" is
# y=0 line, and "yzero" is x=0 line.
ax = SubplotZero(fig, 1, 1, 1)
fig.add_subplot(ax)

# make xzero axis (horizontal axis line through y=0) visible.
ax.axis["xzero"].set_visible(True)
ax.axis["xzero"].label.set_text("Axis Zero")

# make other axis (bottom, top, right) invisible.
for n in ["bottom", "top", "right"]:
    ax.axis[n].set_visible(False)

xx = np.arange(0, 2*np.pi, 0.01)
ax.plot(xx, np.sin(xx))

pltshow(plt)
