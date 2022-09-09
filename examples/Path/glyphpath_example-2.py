
from __future__ import print_function

size(0, 0)

#
# RUN FULLSCREEN
#


import random as rnd
# Parts taken from beziereditor pathimport example

fonts = fontnames()

def setup():
    background(0,0.2,0.3)


speed( 0.125 )

def draw():
    background(0,0.2,0.3)
    chars = (u"abcdefghijklmnopqrstuvwxyzäöüß"
             u"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ"
             u"!§$%&/()=¡¶¢{}ÁÛØ∏ÅÍÏÌÓﬂŒÆ‡ÙÇ÷—")
    for drawing in range(50):
        chr = choice( chars )
        f = choice( fonts )
        x = 100 + (random(WIDTH) - 200)
        y = HEIGHT - random(400)
        fontsize(800)
        p = textpath(chr, x, y, font=f)
        a = random(-90, 90)
        col = [1,1,random()]
        rnd.shuffle(col)
        rnd.shuffle(col)
        rnd.shuffle(col)
        print( chr,f )
        col.append( 0.05 )
        points = []
        for pt in p:
            points.append(pt)

        reset()
        # rotate(a)
        for i in range(8):
            beginpath()
            # fill(1, 1, 1, 0.05)
            fill( *col )
            stroke(1, 1, 1, 0.1)
            strokewidth(0.5)
            scale(0.93)
            rotate(-i*0.2)
            translate(i,0)
            drawpath(points)

