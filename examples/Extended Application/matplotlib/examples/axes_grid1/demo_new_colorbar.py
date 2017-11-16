"""
=================
Demo New Colorbar
=================

"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.colorbar import colorbar

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

plt.rcParams["text.usetex"] = False

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3))

im1 = ax1.imshow([[1, 2], [3, 4]])
cb1 = fig.colorbar(im1, ax=ax1)
cb1.ax.set_yticks([1, 3])
ax1.set_title("Original MPL's colorbar w/\nset_yticks([1,3])", size=10)

im2 = ax2.imshow([[1, 2], [3, 4]])
cb2 = colorbar(im2, ax=ax2)
cb2.ax.set_yticks([1, 3])
ax2.set_title("AxesGrid's colorbar w/\nset_yticks([1,3])", size=10)

pltshow(plt)
