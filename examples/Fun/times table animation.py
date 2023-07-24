# inspired by:
# mathologer
# Times Tables, Mandelbrot and the Heart of Mathematics
# https://www.youtube.com/watch?v=qhbuKbxJsk8

# referenced by:
# http://blog.schockwellenreiter.de/2019/02/2019021402.html
# Daniel Schiffman
# https://youtu.be/bl3nc_a1nvs

# Times Tables Cardioid Visualization


def mt( p ):
    x, y = p
    moveto(x+0.5, y+0.5)

def lt( p ):
    x, y = p
    lineto(x+0.5, y+0.5)


def drawit(n, factor, points):

    background( bg )
    fontsize(10)
    fill(1,1,0)
    #text("%.3f   %i / %i" % (factor, factoridx, len(factors)), 12,20)
    text("%.3f" % (factor,), 12,20)
    # lines
    stroke(1,1,0)
    strokewidth( 0.33 )
    # strokewidth( 1 )
    lines = []
    autoclosepath(False)
    beginpath()
    for i,p in enumerate( points ):
        mt( points[i] )
        target = int(round(i * factor))
        target = target % n
        lt( points[target] )
    endpath()

def setup():
    pass

speed( 100 )


# radius of main circle
radius = 192
size(2*radius, 2*radius)

cx, cy = int( WIDTH / 2), int( HEIGHT / 2 )

# number of points on main circle
n = 116
step = 360.0 / n

# radius of circle marker on circle
r = 0

# background gray
bg = 0.067


slowness = int(n * 1.5)
circlepoints = 12000

factors = [ (i+1) / slowness for i in range(circlepoints) ]
factoridx = 0

# calculate points on circle
points = []
deg = 0
for i in range(n):
    deg = i * step + 180
    x1, y1 = coordinates(cx,cy, radius, deg)
    points.append( (x1, y1) )
for i in range(n, 0, -1):
    deg = i * step + 180
    x1, y1 = coordinates(cx,cy, radius, deg)
    points.append( (x1, y1) )

def draw():
    global factoridx
    if factoridx > len( factors )-1:
        factoridx = 0
    drawit( n, factors[factoridx], points )
    factoridx = factoridx + 1

