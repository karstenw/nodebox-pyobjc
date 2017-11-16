"""
Sharing axis limits and views
=============================

It's common to make two or more plots which share an axis, e.g., two
subplots with time as a common axis.  When you pan and zoom around on
one, you want the other to move around with you.  To facilitate this,
matplotlib Axes support a ``sharex`` and ``sharey`` attribute.  When
you create a :func:`~matplotlib.pyplot.subplot` or
:func:`~matplotlib.pyplot.axes` instance, you can pass in a keyword
indicating what axes you want to share with
"""

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

t = np.arange(0, 10, 0.01)

ax1 = plt.subplot(211)

ax1.plot(t, np.sin(2*np.pi*t))

ax2 = plt.subplot(212, sharex=ax1)

ax2.plot(t, np.sin(4*np.pi*t))

pltshow(plt)