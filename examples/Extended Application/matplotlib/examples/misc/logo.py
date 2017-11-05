"""
====
Logo
====

This file generates an old version of the Matplotlib logo.
"""

from __future__ import print_function
# Above import not necessary for Python 3 onwards. Recommend taking this
# out in examples in the future, since we should all move to Python 3.
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook

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

# convert data to mV
datafile = cbook.get_sample_data('membrane.dat', asfileobj=False)
print('loading', datafile)

x = 1000 * 0.1 * np.fromstring(open(datafile, 'rb').read(), np.float32)
# 0.0005 is the sample interval
t = 0.0005 * np.arange(len(x))
plt.figure(1, figsize=(7, 1), dpi=100)
ax = plt.subplot(111, facecolor='y')
plt.plot(t, x)
plt.text(0.5, 0.5, 'matplotlib', color='r',
         fontsize=40, fontname=['Courier', 'DejaVu Sans Mono'],
         horizontalalignment='center',
         verticalalignment='center',
         transform=ax.transAxes,
         )
plt.axis([1, 1.72, -60, 10])
plt.gca().set_xticklabels([])
plt.gca().set_yticklabels([])

pltshow(plt)
