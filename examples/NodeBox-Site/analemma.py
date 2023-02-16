from math import cos, sin, pi, sqrt
speed(100)
size(800, 800)
from nodebox.graphics import BezierPath
import numpy as _N
 
class circle(BezierPath):
    def __init__(self, x, y, radius, draw=True, **kwargs):
        BezierPath.__init__(self, _ctx, **kwargs)
        self._nsBezierPath.appendBezierPathWithOvalInRect_( ((x-radius, y-radius), (radius*2.0, radius*2.0)) )
        self.center = _N.array([x, y], _N.float)
        self.radius = float(radius)
        self.diameter = radius*2.0
        self.inheritFromContext(kwargs.keys())    
        if draw: self.draw()
    def pointAtBearing(self,rad):
        ''' returns a point at the angle given in radians 0 radian is the left of the cirle increasing counterclockwise'''
        x = self.center[0] - sin(rad-pi/2) * self.radius
        y = self.center[1] + cos(rad-pi/2) * self.radius
        return _N.array([x, y])
    def externalTangentCircleAtBearing(self, radian, radius, draw=True):
        point = self.pointAtBearing(radian)
        x = point[0] + radius*cos(radian)
        y = point[1] + radius*sin(radian)
        return circle(x, y, radius, draw)
    def tangentCircleWith(self,circ2, radius, draw=True):
        ''' Returns a circle of given radius tangent with both this and circ2 
            Returns None if circle doesnt exist'''
        r1 = self.radius + radius
        r2 = circ2.radius + radius
        d = distance(self.center, circ2.center)
        if  r1+r2 < d:
            # the circles are too far apart to make a connection with the given radius
            return None
        x1, y1 = self.center
        x2, y2 = circ2.center
        
        A = sqrt((d+r1+r2) * (d+r1-r2) * (d-r1+r2) * (-d+r1+r2))/4.0
        x = ((x1+x2)/2.0) - ((x1-x2)*(r1**2-r2**2))/(2.0*d**2) + 2.0*((y1-y2)/d**2)*A
        y = ((y1+y2)/2.0) - ((y1-y2)*(r1**2-r2**2))/(2.0*d**2) - 2.0*((x1-x2)/d**2)*A
        return circle(x, y, radius, draw=draw)        
 
 
########### UTILITY FUNCTIONS
 
def distance(p1, p2):
    '''p1 and p2 are numeric arrays'''
    return sqrt(_N.add.reduce((p1-p2)**2))    
def radians(degrees):
    return degrees *pi/180
def marker(point):
    oval(point[0]-2, point[1]-2, 4, 4, stroke=(.2, .2, .4))
def trailer(point, tran):
    oval(point[0]-2, point[1]-2, 4, 4, stroke=(None), fill=(.2, .2, .4, tran))    
def link(p1, p2, p3):
    marker(p1)
    marker(p2)
    marker(p3)
    line(p1[0], p1[1], p3[0], p3[1])
    line(p2[0], p2[1], p3[0], p3[1])
 
theta = -pi/2
y = 300
r = 50
trails = []
dy = .07
def draw():
    global theta, r, trails, y, dy
    autoclosepath(False)
 
    background(1)
    nofill()
    stroke(.2, .2, .5)
    strokewidth(.25)
    theta += dy
    y += dy
    a1 = circle(200, 221, 80)
    a2 = circle(600, 221, 80)
    
    b = a1.externalTangentCircleAtBearing(theta, 23)
    b2 = a2.externalTangentCircleAtBearing(theta+(pi/2), 23)
 
    c = b.tangentCircleWith(b2, 255)
    link(b2.center, b.center, c.center)
    line(a1.center[0], a1.center[1],  b.center[0], b.center[1])
    line(a2.center[0], a2.center[1],  b2.center[0], b2.center[1])
 
 
    trails.append(c.center)
 
    trails= trails[-92:]
    for i, p in enumerate(trails):
        trailer(p, i/92.)

