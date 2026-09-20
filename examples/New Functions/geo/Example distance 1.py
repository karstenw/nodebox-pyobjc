import math




def params(val, name):
    global x, y
    # global scope needs updating.
    val = int(round(val,0))
    if name == "x":
        x = int(val)
    else:
        y = int(val)
    triangle(x, y)


def triangle(x, y):

    x0, y0 = 80, 180
    x1, y1 = x0 + x, y0
    x2, y2 = x0, y0 + y
    # draw a triangle
    stroke(0.2)
    nofill()
    strokewidth(2)
    autoclosepath(True)
    beginpath(x0, y0)
    lineto(x1, y1)
    lineto(x2, y2)
    endpath()

    # labels
    fill(0)

    lx,ly = x0 + (x/2.0), y0 - 10
    text("x", lx, ly)

    lx,ly = x0 - 15, y0 + (y / 2.0)
    text("y", lx, ly)
    
    lx,ly = x0, y0 -150
    text("x = %i" % x, lx, ly)

    lx,ly = x0, y0 -120
    text("y = %i" % y, lx, ly)


    d = round(distance(x1, y1, x2, y2), 3)
    lx,ly = x0, y0 -90
    text("hypotenuse ≈ %.3f" % d, lx, ly)

    lx,ly = x0, y0 -45
    text("distance( x0=%i, y0=%i, x1=%i, y1=%i )" % (x1, y1, x2, y2), lx, ly)


var("x", NUMBER, default=50, min=10, max=300, handler=params)
var("y", NUMBER, default=50, min=10, max=300, handler=params)


triangle(x,y)
