"""
Easily creating subplots
========================

In early versions of matplotlib, if you wanted to use the pythonic API
and create a figure instance and from that create a grid of subplots,
possibly with shared axes, it involved a fair amount of boilerplate
code.  e.g.
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

x = np.random.randn(50)

# old style
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222, sharex=ax1, sharey=ax1)
ax3 = fig.add_subplot(223, sharex=ax1, sharey=ax1)
ax3 = fig.add_subplot(224, sharex=ax1, sharey=ax1)

###############################################################################
# Fernando Perez has provided a nice top level method to create in
# :func:`~matplotlib.pyplots.subplots` (note the "s" at the end)
# everything at once, and turn on x and y sharing for the whole bunch.
# You can either unpack the axes individually::

# new style method 1; unpack the axes
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey=True)
ax1.plot(x)

###############################################################################
# or get them back as a numrows x numcolumns object array which supports
# numpy indexing

# new style method 2; use an axes array
fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
axs[0, 0].plot(x)

pltshow(plt)