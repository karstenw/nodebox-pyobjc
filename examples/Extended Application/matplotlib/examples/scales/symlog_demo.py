"""
===========
Symlog Demo
===========

Example use of symlog (symmetric log) axis scaling.
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

dt = 0.01
x = np.arange(-50.0, 50.0, dt)
y = np.arange(0, 100.0, dt)

plt.subplot(311)
plt.plot(x, y)
plt.xscale('symlog')
plt.ylabel('symlogx')
plt.grid(True)
plt.gca().xaxis.grid(True, which='minor')  # minor grid on too

plt.subplot(312)
plt.plot(y, x)
plt.yscale('symlog')
plt.ylabel('symlogy')

plt.subplot(313)
plt.plot(x, np.sin(x / 3.0))
plt.xscale('symlog')
plt.yscale('symlog', linthreshy=0.015)
plt.grid(True)
plt.ylabel('symlog both')

plt.tight_layout()
pltshow(plt)
