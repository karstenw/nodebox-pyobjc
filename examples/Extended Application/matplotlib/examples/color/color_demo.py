"""
==========
Color Demo
==========

matplotlib gives you 5 ways to specify colors,

    1) as a single letter string, ala MATLAB

    2) as an html style hex string or html color name

    3) as an R,G,B tuple, where R,G,B, range from 0-1

    4) as a string representing a floating point number
       from 0 to 1, corresponding to shades of gray.

    5) as a special color "Cn", where n is a number 0-9 specifying the
       nth color in the currently active color cycle.

See help(colors) for more info.
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

t = np.arange(0.0, 2.0, 0.01)
s = np.sin(2 * np.pi * t)

fig, ax = plt.subplots(facecolor='darkslategray')
ax.plot(t, s, 'C1')
ax.set_xlabel('time (s)', color='C1')
ax.set_ylabel('voltage (mV)', color='0.5')  # grayscale color
ax.set_title('About as silly as it gets, folks', color='#afeeee')

pltshow(plt)
