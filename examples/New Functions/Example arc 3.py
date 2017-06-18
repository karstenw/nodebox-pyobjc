size(800,800)
import math

background(0.9)
nofill()
stroke(0)

var("arcs", NUMBER, 4, 1, 80)
var("radius", NUMBER, 200, 0, 400)
var("strokesize", NUMBER, 8.0, 0.5, 60.0)

arcs = int(arcs)

def mark(x,y,size=10, col=color(255,0,0)):
    push()
    d = size / 2.0
    stroke(col)
    line(x-d-0.5,y-d-0.5,x+d+0.5,y+d+0.5)
    line(x-d-0.5,y+d+0.5,x+d+0.5,y-d-0.5)
    pop()

def label(s,x,y):
    push()
    # save fill value
    f = fill()
    fill(1)
    text(s, x, y+20)
    fill(0)
    text(s, x+1, y+21)
    # restore fill value
    fill(f)
    pop()


strokewidth(strokesize)
stroke(0,0,0)

x, y = WIDTH / 2.0, HEIGHT / 2.0

if arcs == 0:
    stepsize = 360
else:
    stepsize = 360.0 / arcs

arcsize = stepsize / 2.0
#print "stepsize:", stepsize

n = int(360.0 / stepsize)
#print "n:", n
#print "arcs:", arcs
#print "radius:", radius
for i in range(n):
    #print "i:", i
    start = i * stepsize
    #print "start:", start
    end = start + arcsize
    #print "end:", end
    arc(x, y, radius, start, end)
