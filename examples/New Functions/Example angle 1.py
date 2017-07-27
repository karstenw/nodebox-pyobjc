import math
import pdb




# this function handles ALL var changes
def params(val, name):
    """a handler with two parameters receives value and name."""
    global x0, y0, x1, y1

    # global scope needs updating.
    val = round(val,1)
    if name == "x0":
        x0 = val
    elif name == "x1":
        x1 = val
    elif name == "y0":
        y0 = val
    elif name == "y1":
        y1 = val
    #refresh display    
    drawit(x0,y0,x1,y1)



def drawit(x0,y0,x1,y1):
    # draw a line with start (circle) and end (cross) markers
    stroke(0.2)
    nofill()
    strokewidth(2)

    line(x0, y0,x1,y1)

    a = angle(x0,y0,x1,y1)

    # line end marker
    stroke(1,0,0)
    strokewidth(1)
    line(x1-5, y1-5, x1+5, y1+5)
    line(x1-5, y1+5, x1+5, y1-5)

    # origin marker
    oval( x0-5, y0-5, 10,10)

    
    # display the command, parameters and result
    lx,ly = 50, 30
    fill(0)
    fontsize(14)
    text("angle(x0=%.1f, y0=%.1f, x1=%.1f, y1=%.1f) = %.1f" % (x0,y0,x1,y1,a,), lx, ly)


var("x0", NUMBER, default=160, min=0, max=600, handler=params)
var("y0", NUMBER, default=250, min=0, max=600, handler=params)
var("x1", NUMBER, default=400, min=0, max=600, handler=params)
var("y1", NUMBER, default=250, min=0, max=600, handler=params)


drawit(x0,y0,x1,y1)
