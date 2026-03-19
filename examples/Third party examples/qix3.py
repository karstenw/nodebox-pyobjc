
# article: https://blog.adafruit.com/2021/07/16/the-math-formulas-for-the-arcade-game-qix-gaming-gameduino/
# original code:
# https://github.com/jamesbowman/py-bteve/blob/master/examples/qix.py

s = 391
size( s, s )

import sys
import time
import math
import random as rnd



def tri(tn):
    # sawtooth comes from the fractional part.
    # ints return 1.0
    return 2 * abs(math.fmod(tn, 1.0) - 0.5)
    # return 2 * abs(math.fmod(tn, 1.0) - 0.5)
    #return math.cos( tn % 360 )

def at(t, px, py, typ=0):
    x = WIDTH * tri(px * t)
    y = HEIGHT * tri(py * t)
    if typ == 0:
        moveto( x, y )
    elif typ == 1:
        lineto( x, y )
    else:
        circle( x,y,3 )

rnd.seed( 1 )

p1x = rnd.random() 
p1y = rnd.random() 
p2x = rnd.random() 
p2y = rnd.random() 

red = rnd.random() 
green = rnd.random() 
blue = rnd.random() 


def setup():
    pass

speed( 30 )
t = 100
nlines = 42

def fizzle( v ):
    if rnd.random() > 0.5:
        return v
    n = rnd.random() / 50
    if rnd.random() > 0.5:
        n = -n
    v = v + n
    if v > 1.0:
        v = v - 1.0
    if v < 0.0:
        v = v + 1.0
    return v



#
# some ideas
#
def anchor( whichPoint ):
    """Anchor p1 or p2 for an amount of frames"""
    # trigger anchor when distance < limit (1/8 of canvas size?)
    pass


def tempwall( whichWall ):
    """One or more of the 4 walls gets narrower."""
    pass


typ = 0

def draw():
    global p1x, p1y, p2x, p2y
    background( 1 )
    global t
    t = t + 1
    strokewidth( 0.5 )
    nofill()
    
    # direction changes work only if there is a true memory of past locations
    # otherwise the whole path changes direction
    if 0: #rnd.random() > 0.5:
        p1x = fizzle( p1x )
        p1y = fizzle( p1y )
        p2x = fizzle( p2x )
        p2y = fizzle( p2y )
    
    for dt in range( 1, nlines, 3 ):
        tn = (t - dt) / (4*nlines)
        # print("tn:", t, tn)
        # print( "tri:", tri(tn))
        col = color( tri( red * tn), tri( green * tn), tri( blue * tn), 0.5 )
        stroke( col )
        if typ < 2:
            beginpath()
        
        at( tn, p1x, p1y, typ )
        #x1 = WIDTH * tri( p1x * tn)
        #y1 = HEIGHT * tri( p1y * tn)
        # beginpath(x1,y1)
        #circle(x1,y1,5)


        #x2 = WIDTH * tri( p2x * tn)
        #y2 = HEIGHT * tri( p2y * tn)
        #circle(x2,y2,5)
        at( tn, p2x, p2y, typ+1 )

        #lineto( x2, y2 )
        if typ < 2:
            endpath()
        # drawline( x1, y1, x2, y1 )
# draw()

