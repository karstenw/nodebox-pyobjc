"""
===========================
Configuring the font family
===========================

You can explicitly set which font family is picked up for a given font
style (e.g., 'serif', 'sans-serif', or 'monospace').

In the example below, we only allow one font family (Tahoma) for the
san-serif font style.  You the default family with the font.family rc
param, e.g.,::

  rcParams['font.family'] = 'sans-serif'

and for the font.family you set a list of font styles to try to find
in order::

  rcParams['font.sans-serif'] = ['Tahoma', 'DejaVu Sans',
                                 'Lucida Grande', 'Verdana']

"""


from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
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

fig, ax = plt.subplots()
ax.plot([1, 2, 3], label='test')

ax.legend()
pltshow(plt)
