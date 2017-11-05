"""
====
Pong
====

A small game demo using Matplotlib.

.. only:: builder_html

   This example requires :download:`pipong.py <pipong.py>`

"""
from __future__ import print_function, division
import time


import matplotlib.pyplot as plt
import pipong


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
canvas = ax.figure.canvas
animation = pipong.Game(ax)

# disable the default key bindings
if fig.canvas.manager.key_press_handler_id is not None:
    canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)


# reset the blitting background on redraw
def handle_redraw(event):
    animation.background = None


# bootstrap after the first draw
def start_anim(event):
    canvas.mpl_disconnect(start_anim.cid)

    def local_draw():
        if animation.ax._cachedRenderer:
            animation.draw(None)
    start_anim.timer.add_callback(local_draw)
    start_anim.timer.start()
    canvas.mpl_connect('draw_event', handle_redraw)


start_anim.cid = canvas.mpl_connect('draw_event', start_anim)
start_anim.timer = animation.canvas.new_timer()
start_anim.timer.interval = 1

tstart = time.time()

pltshow(plt)
print('FPS: %f' % (animation.cnt/(time.time() - tstart)))
