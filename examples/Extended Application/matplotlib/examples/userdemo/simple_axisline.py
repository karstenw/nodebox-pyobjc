"""
===============
Simple Axisline
===============

"""
import matplotlib.pyplot as plt

from mpl_toolkits.axisartist.axislines import SubplotZero


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

if 1:

    fig = plt.figure(1)
    fig.subplots_adjust(right=0.85)
    ax = SubplotZero(fig, 1, 1, 1)
    fig.add_subplot(ax)

    # make right and top axis invisible
    ax.axis["right"].set_visible(False)
    ax.axis["top"].set_visible(False)

    # make xzero axis (horizontal axis line through y=0) visible.
    ax.axis["xzero"].set_visible(True)
    ax.axis["xzero"].label.set_text("Axis Zero")

    ax.set_ylim(-2, 4)
    ax.set_xlabel("Label X")
    ax.set_ylabel("Label Y")
    # or
    #ax.axis["bottom"].label.set_text("Label X")
    #ax.axis["left"].label.set_text("Label Y")

    # make new (right-side) yaxis, but wth some offset
    offset = (20, 0)
    new_axisline = ax.get_grid_helper().new_fixed_axis

    ax.axis["right2"] = new_axisline(loc="right",
                                     offset=offset,
                                     axes=ax)
    ax.axis["right2"].label.set_text("Label Y2")

    ax.plot([-2, 3, 2])
    pltshow(plt)
