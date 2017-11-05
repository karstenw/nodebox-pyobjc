"""
==================
Simple Axisartist1
==================

"""
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA

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

fig = plt.figure(1)
fig.subplots_adjust(right=0.85)
ax = AA.Subplot(fig, 1, 1, 1)
fig.add_subplot(ax)

# make some axis invisible
ax.axis["bottom", "top", "right"].set_visible(False)

# make an new axis along the first axis axis (x-axis) which pass
# through y=0.
ax.axis["y=0"] = ax.new_floating_axis(nth_coord=0, value=0,
                                      axis_direction="bottom")
ax.axis["y=0"].toggle(all=True)
ax.axis["y=0"].label.set_text("y = 0")

ax.set_ylim(-2, 4)

pltshow(plt)
