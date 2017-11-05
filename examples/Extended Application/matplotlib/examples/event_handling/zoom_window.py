"""
===========
Zoom Window
===========

This example shows how to connect events in one window, for example, a mouse
press, to another figure window.

If you click on a point in the first window, the z and y limits of the
second will be adjusted so that the center of the zoom in the second
window will be the x,y coordinates of the clicked point.

Note the diameter of the circles in the scatter are defined in
points**2, so their size is independent of the zoom
"""
import matplotlib.pyplot as plt #import figure, show
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


figsrc = plt.figure()
figzoom = plt.figure()

axsrc = figsrc.add_subplot(111, xlim=(0, 1), ylim=(0, 1), autoscale_on=False)
axzoom = figzoom.add_subplot(111, xlim=(0.45, 0.55), ylim=(0.4, .6),
                             autoscale_on=False)
axsrc.set_title('Click to zoom')
axzoom.set_title('zoom window')
x, y, s, c = np.random.rand(4, 200)
s *= 200


axsrc.scatter(x, y, s, c)
axzoom.scatter(x, y, s, c)


def onpress(event):
    if event.button != 1:
        return
    x, y = event.xdata, event.ydata
    axzoom.set_xlim(x - 0.1, x + 0.1)
    axzoom.set_ylim(y - 0.1, y + 0.1)
    figzoom.canvas.draw()

figsrc.canvas.mpl_connect('button_press_event', onpress)
pltshow(plt)
