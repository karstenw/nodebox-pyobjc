import math
import pdb





# this function handles ALL var changes
def params(val, name):
    """a handler with two parameters receives value and name."""
    global x1, y1, x2, y2, d, a
    # global scope needs updating.
    val = round(val,1)
    if name == "x1":
        x1 = val
    elif name == "x2":
        x2 = val
    elif name == "y1":
        y1 = val
    elif name == "y2":
        y2 = val
    elif name == "d":
        d = val
    elif name == "a":
        a = val
    #refresh display    
    drawit(x1,y1,x2,y2,d,a)



def drawit(x1,y1,x2,y2,d,a):
    # draw a line with origin (circle) and reflection (cross)  markers
    stroke(0.2)
    nofill()
    strokewidth(2)

    line(x1, y1,x2,y2)

    x3,y3 = reflect(x1,y1,x2,y2,d=d,a=a)
    if 0:
        print "(x1,y1,x2,y2,d,a)", (x1,y1,x2,y2,d,a)
        print "x3,y3", x3,y3
        print

    # reflection marker
    stroke(1,0,0)
    strokewidth(1)
    line(x3-5, y3-5, x3+5, y3+5)
    line(x3-5, y3+5, x3+5, y3-5)

    # origin marker
    oval( x1-5, y1-5, 10,10)

    
    lx,ly = 50, 30
    fill(0)
    fontsize(14)
    text("reflect(x0=%.1f, y0=%.1f, x1=%.1f, y1=%.1f, d=%.1f, a=%.1f) = (%.1f, %.1f)" % (x1,y1,x2,y2,d,a,x3,y3), lx, ly)


var("x1", NUMBER, default=300, min=0, max=600, handler=params)
var("y1", NUMBER, default=200, min=0, max=600, handler=params)
var("x2", NUMBER, default=400, min=0, max=600, handler=params)
var("y2", NUMBER, default=200, min=0, max=600, handler=params)
var("d", NUMBER, default=1.0, min=0.0, max=4.0, handler=params)
var("a", NUMBER, default=180, min=0, max=360, handler=params)


drawit(x1,y1,x2,y2,d,a)
