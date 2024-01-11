size(780,780)
background(None)
import math
import pprint

nofill()
stroke(0)
speed(36)


def drawArcedCircle(x,y,r,n,s,sw,t,o):
    """x,y - center
       r - radius
       n - no of segments
       s - gray intensity
       sw - strokewidth
       t - alpha
       o - orientation (angle)
    """
    n = int(n)
    sw = float(sw)
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
        if 0: #fractional:
            arcsize = stepsize * float(n-1) / n
        else:
            arcsize = stepsize * 3 / 4.0

    for i in range(n):
        start = i * stepsize + o
        end = start + arcsize
        arc(x, y, r, start, end)

x, y = WIDTH / 2.0, HEIGHT / 2.0

a = 0.5
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

rings = [
    # (radius, speed, color)
    [ (i+1)*segtotal, 2**(int(ringnumber)-i-1), 0.90-(i*lightgap)] for i in range(int(ringnumber))]





def handleAlpha(i):
    global a
    a = i

def handleFractional(b):
    global fractional
    fractional = b

def handleRingcount(n):
    global ringnumber, rings, phiincrement, lightgap
    ringnumber = int(n)
    phiincrement = 1 / (2**(ringnumber-1) * 0.1)
    lightgap = 0.8 / (ringnumber-1)
    rings = [
        # (radius, speed, color)
        [ (i+1)*segtotal, 2**(int(ringnumber)-i-1), 0.90-(i*lightgap)] for i in range(int(ringnumber))]

def handleSegcount(n):
    global segments
    segments = int(n)

def handleSegwidth(w):
    global segwidth, segtotal, rings
    segwidth = w
    segtotal = segwidth + seggap
    rings = [
        # (radius, speed, color)
        [ (i+1)*segtotal, 2**(int(ringnumber)-i-1), 0.90-(i*lightgap)] for i in range(int(ringnumber))]


def handleSeggap(w):
    global seggap, segtotal, rings
    seggap = int(w)
    segtotal = segwidth + seggap
    rings = [
        # (radius, speed, color)
        [ (i+1)*segtotal, 2**(int(ringnumber)-i-1), 0.90-(i*lightgap)] for i in range(int(ringnumber))]

ringMenu = range(1,20)
ringMenu = [str(i) for i in ringMenu]

segMenu = range(1,16)
segMenu = [str(i) for i in segMenu]


var("alpha", NUMBER, 0.5, 0.01, 1.0, handler=handleAlpha)
# var("fractional", BOOLEAN, default=False, handler=handleFractional)
var("ringnumber", MENU, default='7', handler=handleRingcount, menuitems=ringMenu)
var("segments", MENU, default='8', handler=handleSegcount, menuitems=segMenu)
var("segwidth", NUMBER, default=80, min=1, max=120, handler=handleSegwidth)
var("seggap", NUMBER, default=-32, min=-100, max=200, handler= handleSeggap)


def draw():
    global phi

    background(None)
    phi = phi % 360.0
    for i,ring in enumerate(rings):
        r, spd, c = ring
        o = phi * spd
        if i % 2 == 0:
            o = -o
        drawArcedCircle(x,y,r,segments, c, segwidth, a, o)
    phi += phiincrement

