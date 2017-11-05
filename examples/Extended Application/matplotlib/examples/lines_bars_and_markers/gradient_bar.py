"""
============
Gradient Bar
============

"""
import matplotlib.pyplot as plt
from numpy import arange
from numpy.random import rand

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

def gbar(ax, x, y, width=0.5, bottom=0):
    X = [[.6, .6], [.7, .7]]
    for left, top in zip(x, y):
        right = left + width
        ax.imshow(X, interpolation='bicubic', cmap=plt.cm.Blues,
                  extent=(left, right, bottom, top), alpha=1)


fig = plt.figure()

xmin, xmax = xlim = 0, 10
ymin, ymax = ylim = 0, 1
ax = fig.add_subplot(111, xlim=xlim, ylim=ylim,
                     autoscale_on=False)
X = [[.6, .6], [.7, .7]]

ax.imshow(X, interpolation='bicubic', cmap=plt.cm.copper,
          extent=(xmin, xmax, ymin, ymax), alpha=1)

N = 10
x = arange(N) + 0.25
y = rand(N)
gbar(ax, x, y, width=0.7)
ax.set_aspect('auto')
pltshow(plt)
