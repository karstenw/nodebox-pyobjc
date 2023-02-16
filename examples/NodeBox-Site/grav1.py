# -*- XXcXoding: UTF-8 -*-

from math import *

size(900, 800)
speed(60)

def setup():
    global moon1, moon2, earth, path1, path2, d
    moon1 = Planet(x=random(0, WIDTH), y=random(0, HEIGHT), mass=20.0)
    earth = MousePlanet(mass=30.0)
    path1 = []
    d = True

def draw():

    background(0.4,0.2,0)
    global d

    # to do: check if the mouse goes off-stsage etc etc..
    g1 = gravity(earth, moon1, k=20.5)

    earth.update()
    moon1.update(g1)

    nofill()
    strokewidth(2)
    autoclosepath(False)
    stroke(1, 0.75)

    pt1 = Point(moon1.x, moon1.y)
    path1.append(pt1)

    if key == 'p':
        d = False # don't show the path
    if key == 'o':
        d = True # show the path

    if d == True:
        if len(path1) > 0:
            first = True
            for pt in path1:
                if first:
                    beginpath(pt.x, pt.y)
                    first = False
                else:
                    lineto(pt.x, pt.y)
            endpath()

    earth.draw()
    moon1.draw()

class Planet:

	def __init__(self, x, y, mass=1.0):
	   self.x = x
	   self.y = y
	   self.mass = mass
	   self.s = self.mass*1 # size
	   self.r = self.s*0.5 # radius
	   self.alive = True # not used yet
	   self.v_x = 0
	   self.v_y = 0

	def draw(self):
	    fill(1, 0.8)
	    nostroke()
	    oval(self.x-self.r, self.y-self.r, self.s, self.s)

	def update(self, g):
	    a_x = g[0] / self.mass
	    a_y = g[1] / self.mass
	    self.v_x += a_x
	    self.v_y += a_y
	    self.x += self.v_x
	    self.y += self.v_y


class MousePlanet:

	def __init__(self, mass=1.0):
	   self.x = MOUSEX
	   self.y = MOUSEY
	   self.mass = mass
	   self.s = self.mass*2
	   self.r = self.s*0.5
	   self.alive = True

	def draw(self):
	    fill(0.5, 0.9, 1, 0.5)
	    nostroke()
	    oval(self.x-self.r, self.y-self.r, self.s, self.s)

	def update(self):
	    self.x = MOUSEX
	    self.y = MOUSEY


def gravity(obj1, obj2, k=0.5):
    dist = distance(obj1.x, obj1.y, obj2.x, obj2.y)
    limit = max(obj1.s, obj2.s)
    if dist < limit:
        dist = limit
    grav = ( (obj1.mass * obj2.mass) / (dist * dist) ) * k
    grav_x = grav * ( (obj1.x - obj2.x) / dist )
    grav_y = grav * ( (obj1.y - obj2.y) / dist )
    return (grav_x, grav_y)

def distance(x0, y0, x1, y1):
    return sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))

