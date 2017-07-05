size(780,780)
background(None)
import math
import pprint

nofill()
stroke(0)
speed(36)


def drawArcedCircle(x,y,r,n,s,sw,t,o):
    strokewidth(sw)
    stroke(s)
    if t < 1:
        stroke(s, t)
    nofill()
    if n == 0:
        arcsize = 360
        stepsize = 360
    else:
        stepsize = 360.0 / n
        if fractional:
            arcsize = stepsize * float(n-1) / n
        else:
            arcsize = stepsize * 3 / 4.0

    for i in range(n):
        start = i * stepsize + o
        end = start + arcsize
        arc(x, y, r, start, end)

x, y = WIDTH / 2.0, HEIGHT / 2.0


# fractional arc length
fractional = False

# how many rings
ringnumber = 7

# a ring is divided into this many segments
segments = 8

# width of a segment
segwidth = 80

# gap between rings
seggap = -32

segtotal = segwidth + seggap
phi = 0
phiincrement = 1 / (2**(ringnumber-1) * 0.1)

# use 0.9..0.1 for color
lightgap = 0.8 / (ringnumber-1)

var("alpha", NUMBER, 0.5, 0.01, 1.0)


rings = [
    # (radius, speed, color)
    [ (i+1)*segtotal, 2**(ringnumber-i-1), 0.90-(i*lightgap)] for i in range(ringnumber)]


def draw():
    global phi

    background(None)
    phi = phi % 360.0
    for i,ring in enumerate(rings):
        r, spd, c = ring
        o = phi * spd
        if i % 2 == 0:
            o = -o
        drawArcedCircle(x,y,r,segments, c, segwidth, alpha, o)
    phi += phiincrement

