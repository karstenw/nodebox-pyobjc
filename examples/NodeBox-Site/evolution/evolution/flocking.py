# BOIDS - last updated for NodeBox 1rc4 
# Author: Tom De Smedt <tomdesmedt@trapdoor.be>
# Copyright (c) 2004 by Tom De Smedt.
# Usage is free for non-commercial use:
# refer to the "Use" section on http://nodebox.net/code

# For the original pseucode the algorithm is based on:
# http://www.vergenet.net/~conrad/boids/pseudocode.html


from nodebox.util import random

class Boid:
    
    def __init__(self, boids, x, y, z):
        
        self.boids = boids
        
        self.x = 1.0 * x
        self.y = 1.0 * y
        self.z = 1.0 * z
        
        self.vx = 0
        self.vy = 0
        self.vz = 0
        
        self.fill = _ctx.color(0.6)
        self.fill.k += 0.1
        
    def cohesion(self, d=100):
        
        """Boids move towards the flock's centre of mass.
        
        The centre of mass is the average position of all boids,
        not including itself (the "perceived centre").
        
        """
        
        vx = vy = vz = 0
        for b in self.boids:
            if b != self:
                vx, vy, vz = vx+b.x, vy+b.y, vz+b.z
                
        n = len(self.boids)-1
        vx, vy, vz = vx/n, vy/n, vz/n
        
        return (vx-self.x)/d, (vy-self.y)/d, (vz-self.z)/d
                
    def separation(self, r=10):
        
        """Boids keep a small distance from other boids.
        
        Ensures that boids don't collide into each other,
        in a smoothly accelerated motion.
        
        """
        
        vx = vy = vz = 0
        for b in self.boids:
            if b != self:
                if abs(self.x-b.x) < r: vx += (self.x-b.x)
                if abs(self.y-b.y) < r: vy += (self.y-b.y)
                if abs(self.z-b.z) < r: vz += (self.z-b.z)
                
        return vx, vy, vz
        
    def alignment(self, d=5):
        
        """Boids match velocity with other boids.
        """
        
        vx = vy = vz = 0
        for b in self.boids:
           if b != self:
               vx, vy, vz = vx+b.vx, vy+b.vy, vz+b.vz
        
        n = len(self.boids)-1
        vx, vy, vz = vx/n, vy/n, vz/n
        
        return (vx-self.vx)/d, (vy-self.vy)/d, (vz-self.vz)/d
        
    def limit(self, max=30):
        
        """The speed limit for a boid.
        
        Boids can momentarily go very fast,
        something that is impossible for real animals.
        
        """
        
        if abs(self.vx) > max: 
            self.vx = self.vx/abs(self.vx)*max
        if abs(self.vy) > max: 
            self.vy = self.vy/abs(self.vy)*max
        if abs(self.vz) > max: 
            self.vz = self.vz/abs(self.vz)*max
        
    def angle(self):
        
        """Returns the angle towards which the boid is steering.
        """
        
        from math import atan, pi, degrees
        a = degrees(atan(self.vy/self.vx+0.00001)) + 360
        if self.vx < 0: a += 180
        
        return 360-a
        
    def goal(self, x, y, z, d=50.0):
        
        """Tendency towards a particular place.
        """
        
        return (x-self.x)/d, (y-self.y)/d, (z-self.z)/d
        
class Boids:
    
    def __init__(self, n, x, y, w, h, col=None):
        
        self.boids = []
        for i in range(n):
            dx = random(w)
            dy = random(h)
            z = random(200)
            b = Boid(self.boids, x+dx, y+dy, z)
            if col != None: b.fill = col
            self.boids.append(b)
            
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self._scatter = 0.005
        self._scattered = False
        self._timer = 50
        self._i = 0
    
        self._hasgoal = False
        self._flee = False
        self._gx = 0
        self._gy = 0
        self._gz = 0
        
    def copy(self):
        
        boids = Boids(0, self.x, self.y, self.w, self.h)
        boids._scatter = self._scatter
        boids._scattered = self._scattered
        boids._timer = self._timer
        boids._i = self._i
        boids._hasgoal = self._hasgoal
        boids._gx = self._gx
        boids._gy = self._gy
        boids._gz = self._gz
        
        for b in self.boids:
            
            boid = Boid(boids, b.x, b.y, b.z)
            boid.vx = b.vx
            boid.vy = b.vy
            boid.vz = b.vz
            boid.fill = b.fill
            boids.boids.append(boid)
            
        return boids

    def scatter(self, chance=0.005, frames=50):
        
        self._scatter = chance
        self._timer = frames
        
    def goal(self, x, y, z, flee=False):
        
        self._hasgoal = True
        self._flee = flee
        self._gx = x
        self._gy = y
        self._gz = z
        
    def nogoal(self):
        
        self._hasgoal = False
        
    def constrain(self):
        
        """Cages the flock inside the x, y, w, h area.
        
        The actual cage is a bit larger,
        so boids don't seem to bounce of invisible walls
        (they are rather "encouraged" to stay in the area).
        
        """
        
        dx = self.w * 0.1
        dy = self.h * 0.1 
        
        for b in self.boids:
            if b.x < self.x-dx: b.vx += random(dx)
            if b.y < self.y-dy: b.vy += random(dy)
            if b.x > self.x+self.w+dx: b.vx -= random(dx)
            if b.y > self.y+self.h+dy: b.vy -= random(dy)
            if b.z < 0: b.vz += 10
            if b.z > 100: b.vz -= 10
            
    def update(self, 
               shuffled=True, 
               cohesion=100, 
               separation=10, 
               alignment=5, 
               goal=20,
               limit=30):
        
        """Calculates the next motion frame for the flock.
        """
        
        #Shuffling the list of boids ensures fluid movement.
        #If you need the boids to retain their position in the list
        #each update, set the shuffled parameter to False.
        from random import shuffle
        if shuffled: shuffle(self.boids)
        
        m1 = 1.0 #cohesion
        m2 = 1.0 #separation
        m3 = 1.0 #alignment
        m4 = 1.0 #goal
        
        #The flock scatters randomly with a Boids.scatter chance.
        #This means their cohesion (m1) is reversed,
        #and their joint alignment (m3) is dimished,
        #causing boids to oscillate in confusion.
        #Setting Boids.scatter(chance=0) ensures they never scatter.
        if not self._scattered and random() < self._scatter:
            self._scattered = True
        if self._scattered:
            m1 = -m1
            m3 *= 0.25
            self._i += 1
        if self._i >= self._timer:
            self._scattered = False
            self._i = 0

        #A flock can have a goal defined with Boids.goal(x,y,z),
        #a place of interest to flock around.
        if not self._hasgoal:
            m4 = 0
        if self._flee:
            m4 = -m4
        
        for b in self.boids:
            
            vx1, vy1, vz1 = b.cohesion(cohesion)
            vx2, vy2, vz2 = b.separation(separation)
            vx3, vy3, vz3 = b.alignment(alignment)
            vx4, vy4, vz4 = b.goal(self._gx, self._gy, self._gz, goal)
            
            b.vx += m1*vx1 + m2*vx2 + m3*vx3 + m4*vx4
            b.vy += m1*vy1 + m2*vy2 + m3*vy3 + m4*vy4
            b.vz += m1*vz1 + m2*vz2 + m3*vz3 + m4*vz4
            
            b.limit(limit)
        
            b.x += b.vx
            b.y += b.vy
            b.z += b.vz
        
        self.constrain()
        
def flock(n, x, y, w, h, fillcolor=None):
    
    return Boids(n, x, y, w, h, fillcolor)