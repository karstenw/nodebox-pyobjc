# Source - https://stackoverflow.com/q/40689189

# Posted by user7173404, modified by community. See post 'Timeline' for change history

# Retrieved 2026-09-08, License - CC BY-SA 3.0



size(600, 600)
colormode(RGB, 255)
speed = (100)

from random import seed
import random
import math
from nodebox import geo



global LEMONCHIFFON, LIGHTBLUE, STEELBLUE, ROYALBLUE

LEMONCHIFFON = (200,205,108)
LIGHTBLUE = (52,86, 163)
STEELBLUE = (70, 130,180)
ROYALBLUE = (65,105,225)

class Stroke:

    def linecap_rounded(pt1, pt2, path):
        a = geo.angle(pt1.x, pt1.y, pt2.x, pt2.y)
        d= geo.distance(pt1.x, pt1.y, pt2.x, pt2.y) * 1
        dx1, dy1 = geo.coordinates(pt1.x, pt1.y, d, a+80)
        dx2, dy2 = geo.coordinates(pt2.x, pt2.y, d, a+70)
        path.curveto(dx1, dy1, dx2, dy2, pt2.x, pt2.y)    

    def transform_uniform(time, distance, angle):
        return distance, angle

    def transform_expand(time, distance, angle):
        return distance * (0.2 + 0.7*time), angle

    def transform_contract(time, distance, angle):
        return distance * (0.8 + 0.3*(1-time)), angle

    ROUNDED = linecap_rounded
    UNIFORM  = transform_uniform
    EXPAND   = transform_expand
    CONTRACT = transform_contract

    def outline_stroke(path, linecap=ROUNDED, transform=UNIFORM, precision=30):
        L = [ ] # The stroke edge to "the left" of the path.
        R = [ ] # The stroke edge to "the right" of the path.
        # The stroke width / 2 is the distance from the path to the left and right.
        # This distance can be tweaked by the given transform function.
        r = _ctx.strokewidth() * 0.6
        # Take a number of sample points on the path.
        # The longer the path, the more precision is needed.
        points = list(path.points(precision))
        for i, pt in enumerate(points):
            if i < precision-1:
                next = points[i+1]
                a = geo.angle(pt.x, pt.y, next.x, next.y)
            else:
                previous = points[i-1]
                a = geo.angle(pt.x, pt.y, previous.x, previous.y) - 180
            d = r
            d, a = transform(float(i)/precision, d, a)
            # With some basic trigonometry, we can calculate the coordinates
            # of a new point at a distance from the point on the path.
            # The direction + 90 degrees is a point on the left stroke edge,
            # the direction - 90 degrees is a point on the right stroke edge.
            dx1, dy1 = geo.coordinates(pt.x, pt.y, d, a+90)
            dx2, dy2 = geo.coordinates(pt.x, pt.y, d, a-90)
            L.append((dx1, dy1))
            R.append((dx2, dy2))
        # Reset the strokewidth (we may have changed it in debug mode).  
        # From the points on the stroke edges,
        # calculate new Bezier paths.
        _ctx.strokewidth(r*2) 
        L = _ctx.findpath(L)
        R = _ctx.findpath(list(reversed(R)))
        path = _ctx.BezierPath()
        for pt in L: 
            path.append(pt)
        linecap(pt, R[0], path) # Close end.
        for pt in list(R)[1:]:  # Ignore first MOVETO. 
            path.append(pt)
        linecap(pt, L[0], path) # Close beginning.
        return path

    def __init__(self, center, angle, color):
        (x, y) = center
        self.cx = x
        self.cy = y
        self.angle = angle
        self.length = random.randint(50, 60)
        self.color = color 

    def rotate(self):
        (cx, cy) = self.cx, self.cy
        newAngle = self.angle - self.delta
        x1 = cx + self.length/2*math.sin(newAngle)
        x2 = cx - self.length/2*math.sin(newAngle)
        y1 = cy - arc.radius

    def draw(self):
        h = self.length/2 * math.sin(self.angle)
        w = self.length/2 * math.cos(self.angle)
        x0 = self.cx - w
        y0 = self.cy + h
        x1 = self.cx + w
        y1 = self.cy - h
        path = BezierPath()
        path.moveto(x0, y0)
        h1x, h1y = (x0*1.7, y0*0.9)
        h2x, h2y= (x0*1.8, y1*0.9)
        path.curveto(x0, y0, x1, y1, x1, y1)
        strokewidth(4)
        path = outline_stroke(path, linecap=ROUNDED, transform=CONTRACT)
        strokewidth(0)
        fill(self.color)
        drawpath(path)

    def move(self):
        LEMONCHIFFON = (200,205,108)
        LIGHTBLUE = (52,86, 163)
        STEELBLUE = (70, 130,180)
        ROYALBLUE = (65,105,225)
        self.angle += math.pi/20
        if self.color == STEELBLUE:
            self.cx-=5
            self.cy-=5
        else:
            self.cx+=5
            self.cy+=5

def setup():
    global frame
    global LEMONCHIFFON, LIGHTBLUE, STEELBLUE, ROYALBLUE
    global listofStrokes
    frame = 1
    listofStrokes = []
    total = 800
    (w, h) = (800,600)
    for i in range(total):
        cx = random.randint(1, 750)
        cy = random.randint(300, 600)
        thiscolor = random.choice([LIGHTBLUE, STEELBLUE, ROYALBLUE,LEMONCHIFFON])
        angle = random.choice([math.pi/15, math.pi/20])
        newstroke = Stroke((cx, cy), angle, thiscolor)
        listofStrokes.append(newstroke)

def draw():
    global frame
    global listofStrokes 
    frame += 1
    for s in listofStrokes:
        s.move()
        s.draw()
