"""
=============
Unit handling
=============

The example below shows support for unit conversions over masked
arrays.

.. only:: builder_html

   This example requires :download:`basic_units.py <basic_units.py>`
"""
import numpy as np
import matplotlib.pyplot as plt
from basic_units import secs, hertz, minutes


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

# create masked array
data = (1, 2, 3, 4, 5, 6, 7, 8)
mask = (1, 0, 1, 0, 0, 0, 1, 0)
xsecs = secs * np.ma.MaskedArray(data, mask, float)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)
ax1.scatter(xsecs, xsecs)
ax1.yaxis.set_units(secs)
ax1.axis([0, 10, 0, 10])

ax2.scatter(xsecs, xsecs, yunits=hertz)
ax2.axis([0, 10, 0, 1])

ax3.scatter(xsecs, xsecs, yunits=hertz)
ax3.yaxis.set_units(minutes)
ax3.axis([0, 10, 0, 1])

fig.tight_layout()
pltshow(plt)
