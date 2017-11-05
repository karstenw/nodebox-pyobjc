"""
=======================
Simple Axis Direction01
=======================

"""
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist

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

fig = plt.figure(figsize=(4, 2.5))
ax1 = fig.add_subplot(axisartist.Subplot(fig, "111"))
fig.subplots_adjust(right=0.8)

ax1.axis["left"].major_ticklabels.set_axis_direction("top")
ax1.axis["left"].label.set_text("Label")

ax1.axis["right"].label.set_visible(True)
ax1.axis["right"].label.set_text("Label")
ax1.axis["right"].label.set_axis_direction("left")

pltshow(plt)
