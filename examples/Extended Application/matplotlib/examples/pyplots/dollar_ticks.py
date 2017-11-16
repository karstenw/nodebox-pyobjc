"""
============
Dollar Ticks
============

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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

# Fixing random state for reproducibility
np.random.seed(19680801)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(100*np.random.rand(20))

formatter = ticker.FormatStrFormatter('$%1.2f')
ax.yaxis.set_major_formatter(formatter)

for tick in ax.yaxis.get_major_ticks():
    tick.label1On = False
    tick.label2On = True
    tick.label2.set_color('green')

pltshow(plt)
