# inspired by:
# https://www.youtube.com/watch?v=qhbuKbxJsk8

import math


# radius of main circle
radius = 340

# number of points on main circle
n = 400

# radius of circle marker on circle
r = 2

# background gray
bg = 0.067

#
factor = 2.0

def params(val, name):
    global radius, n, r, bg, factor
    # global scope needs updating.
    if name == "radius":
        val = int(round(val))
        radius = val
    elif name == "n":
        val = int(round(val))
        n = val
    elif name == "r":
        val = round(val,1)
        r = val
    elif name == "bg":
        val = round(val, 2)
        bg = val
    elif name == "factor":
        val = round(val, 5)
        factor = val
    print name, val
    drawit(radius, n)


def circle( center, radius ):
    x,y = center
    x = x-radius
    y = y-radius
    r = radius * 2
    oval(x,y,r,r)
    
def mt( p ):
    x, y = p
    moveto(x, y)

def lt( p ):
    x, y = p
    lineto(x, y)



def drawit(radius, n):
    width = radius * 2
    oversize = r * 2
    w = width+oversize
    h = w
    x = w / 2.0
    y = x
    size( w, h )
    if bg == 0.0:
        background( None )
    else:
        background( bg )
    
    step = 360.0 / n
    
    # calculate points on circle
    points = []
    deg = 0
    for i in range(n):
        deg = i * step + 180
        x1, y1 = coordinates(x,y, radius, deg)
        points.append( (x1, y1) )

    # points on circle
    stroke(1,0,0)
    strokewidth(1)
    if r > 1:
        for p in points:
            circle( p, r )

    # lines
    stroke(1,1,0)
    strokewidth( 0.33 )
    lines = []
    autoclosepath(False)
    beginpath()
    for i,p in enumerate( points ):
        mt( points[i] )
        target = int(round(i * factor))
        target = target % n
        lt( points[target] )
    endpath()


var("radius", NUMBER, default=340, min=50, max=850, handler=params)
var("n", NUMBER, default=400, min=3, max=800, handler=params)
var("r", NUMBER, default=1, min=1, max=5, handler=params)
var("bg", NUMBER, default=0.067, min=0.0, max=1.0, handler=params)
var("factor", NUMBER, default=2.0, min=0.00001, max=5.0, handler=params)

drawit( radius, n )
