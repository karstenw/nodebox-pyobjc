import math


def params(val, name):
    global x0, y0, d, a
    # global scope needs updating.
    val = round(val,1)
    if name == "x0":
        x0 = val
    elif name == "y0":
        y0 = val
    elif name == "d":
        d = val
    elif name == "a":
        a = val
    drawit(x0,y0,d,a)


def drawit(x0,y0,d,a):
    stroke(0.2)
    nofill()
    strokewidth(2)


    x1, y1 = coordinates(x0,y0,d,a)
    line(x0,y0, x1,y1)

    # reflection marker
    stroke(1,0,0)
    strokewidth(1)
    line(x1-5, y1-5, x1+5, y1+5)
    line(x1-5, y1+5, x1+5, y1-5)

    # origin marker
    oval( x0-5, y0-5, 10,10)

    
    lx,ly = 50, 30
    fill(0)
    fontsize(14)
    s = "coordinates(x0=%.1f, y0=%.1f, d=%.1f, a=%.1f) = (%.1f, %.1f)" % (x0,y0,d,a,x1,y1)
    text(s, lx, ly)
    print s


var("x0", NUMBER, default=200, min=10, max=400, handler=params)
var("y0", NUMBER, default=200, min=10, max=400, handler=params)
var("d", NUMBER, default=50, min=0, max=400, handler=params)
var("a", NUMBER, default=180, min=0, max=360, handler=params)


drawit(x0,y0,d,a)
