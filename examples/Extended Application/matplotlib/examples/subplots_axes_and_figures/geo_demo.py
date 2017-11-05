"""
======================
Geographic Projections
======================

This shows 4 possible projections using subplot.  Matplotlib also
supports `Basemaps Toolkit <https://matplotlib.org/basemap>`_ and
`Cartopy <http://scitools.org.uk/cartopy>`_ for geographic projections.

"""

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

###############################################################################

plt.figure()
plt.subplot(111, projection="aitoff")
plt.title("Aitoff")
plt.grid(True)

###############################################################################

plt.figure()
plt.subplot(111, projection="hammer")
plt.title("Hammer")
plt.grid(True)

###############################################################################

plt.figure()
plt.subplot(111, projection="lambert")
plt.title("Lambert")
plt.grid(True)

###############################################################################

plt.figure()
plt.subplot(111, projection="mollweide")
plt.title("Mollweide")
plt.grid(True)

pltshow(plt)
