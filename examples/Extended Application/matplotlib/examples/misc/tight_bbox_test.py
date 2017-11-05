"""
===============
Tight Bbox Test
===============

"""
from __future__ import print_function
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

ax = plt.axes([0.1, 0.3, 0.5, 0.5])

ax.pcolormesh(np.array([[1, 2], [3, 4]]))
plt.yticks([0.5, 1.5], ["long long tick label",
                        "tick label"])
plt.ylabel("My y-label")
plt.title("Check saved figures for their bboxes")
for ext in ["png", "pdf", "svg", "svgz", "eps"]:
    print("saving tight_bbox_test.%s" % (ext,))
    plt.savefig("tight_bbox_test.%s" % (ext,), bbox_inches="tight")
pltshow(plt)
