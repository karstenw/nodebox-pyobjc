"""
Transparent, fancy legends
==========================

Sometimes you know what your data looks like before you plot it, and
may know for instance that there won't be much data in the upper right
hand corner.  Then you can safely create a legend that doesn't overlay
your data:

  ax.legend(loc='upper right')

Other times you don't know where your data is, and loc='best' will try
and place the legend::

  ax.legend(loc='best')

but still, your legend may overlap your data, and in these cases it's
nice to make the legend frame transparent.
"""

import matplotlib.pyplot as plt
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

np.random.seed(1234)
fig, ax = plt.subplots(1)
ax.plot(np.random.randn(300), 'o-', label='normal distribution')
ax.plot(np.random.rand(300), 's-', label='uniform distribution')
ax.set_ylim(-3, 3)

ax.legend(loc='best', fancybox=True, framealpha=0.5)
ax.set_title('fancy, transparent legends')
pltshow(plt)