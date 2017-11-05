"""
===============
Demo Gridspec04
===============

"""
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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

def make_ticklabels_invisible(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)


# gridspec inside gridspec

f = plt.figure()

gs0 = gridspec.GridSpec(1, 2)

gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs0[0])

ax1 = plt.Subplot(f, gs00[:-1, :])
f.add_subplot(ax1)
ax2 = plt.Subplot(f, gs00[-1, :-1])
f.add_subplot(ax2)
ax3 = plt.Subplot(f, gs00[-1, -1])
f.add_subplot(ax3)


gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs0[1])

ax4 = plt.Subplot(f, gs01[:, :-1])
f.add_subplot(ax4)
ax5 = plt.Subplot(f, gs01[:-1, -1])
f.add_subplot(ax5)
ax6 = plt.Subplot(f, gs01[-1, -1])
f.add_subplot(ax6)

plt.suptitle("GridSpec Inside GridSpec")
make_ticklabels_invisible(f)

pltshow(plt)
