from math import sqrt
from random import choice, shuffle

from nodebox.graphics import CENTER
from nodebox.util import files, random
# from DrawingPrimitives import files, random, CENTER

from creatures import Creature

_boids = None
def boids():
    global _boids
    if _boids == None:
        _boids = _ctx.ximport("flocking")
        reload(_boids)
    return _boids

# Different states for dragons
FLOCKING = "flocking"
FIGHTING = "fighting"
ROAMING = "roaming"
FLEEING = "fleeing"
HUNTING = "hunting"
PREYING = "preying"
INTERCEPTING = "intercepting"

class Dragon(Creature):
    
    def __init__(self, x=None, y=None, z=None, name=None):
        
        # Load statistics and images
        Creature.__init__(self)
        self.name = ""
        self.fitness = random()
        self.velocity = random()
        self.ferocity = random()
        self.cunning = random()
        if name: self.spawn(name)
        self.health = self.fitness
        
        # By default, start somewhere offscreen
        if x == None: x = choice((-50,_ctx.WIDTH+250)) - random(200)
        if y == None: y = choice((-50,_ctx.HEIGHT+250)) - random(200)
        if z == None: z = random(100)
        
        self.x = x
        self.y = y
        self.z = z
        self. r = 0
        self.trail = []
        self.state = ROAMING
        
        boids = _ctx.ximport("flocking")
        self.roaming = True
        self.physics = boids.Boids(2, 0, 0, _ctx.WIDTH, _ctx.HEIGHT)
        self.head = self.physics.boids[0]
        self.copy(self, self.head)
        
        self.flocking = False    
        self.flock = None
        self.boid = None
        
        self.prey = None
        
        #self.polarise()

    def polarise(self, d=0.1):
        
        # Makes low creature statistics lower,
        # and high creature statistics higher.
        # This makes the confrontation more black/white.
        
        def f(p):
            if p < 0.4: p = max(0, p-d)
            if p > 0.6: p = min(1.0, p+d)
            return p
            
        self.fitness = f(self.fitness)
        self.health = f(self.health)
        self.velocity = f(self.velocity)
        self.ferocity = f(self.ferocity)
        self.cunning = f(self.cunning)

    def copy(self, v1, v2):
        
        # Copies the coordinates of vector 1 into vector 2.
        v2.x = v1.x
        v2.y = v1.y
        v2.z = v1.z
        
        try: v2.r = v1.angle()
        except: pass  
    
    def update(self, trail=7):
        
        # Updates the creature's trail.
        # The trail is a history of positions.
        if len(self.trail) > trail: del self.trail[0]
        self.trail.append((self.x, self.y, self.z))

        # If the creature is part of a flock,
        # let the flock handle the motion physics.        
        if self.flocking and self.roaming:
            self.state = FLOCKING
            self.roaming = False
            self.copy(self, self.boid)
        if self.flocking:
            self.copy(self.boid, self)

        # Otherwise, use a head/brain of two boids
        # to calculate individual steering, goals, etc.        
        if not self.flocking and not self.roaming:
            self.state = ROAMING
            self.roaming = True
            self.copy(self.boid, self.head)         
        if self.roaming:
            self.physics.update(goal=10, 
                                limit=40*self.velocity)
            self.copy(self.head, self)
            
    def chase(self, flock):
        
        # The idea is to target a random creature in the flock,
        # predator's don't perceive the individuals in a group.
        # Once the flock breaks apart, target a lone straggler.
        # Pick a straggler with the lowest life.
        self.prey = choice(flock.creatures)
        if random() < self.cunning: 
            self.prey = flock.creatures[0]
        self.state = HUNTING
        if random() < self.cunning:
            for creature in flock.creatures:
                if not creature.flocking:
                    if self.prey.flocking \
                    or self.prey.health > creature.health:
                        self.prey = creature
                        self.state = PREYING

        # Chase the prey.
        # Sometimes the predator loses interest,
        # this allows him to steer a random direction
        # (instead of eternally tailing the prey)
        # and possibly intercepting its prey.
        self.physics.goal(self.prey.x, self.prey.y, self.prey.z)
        if random() > 0.8 and random() < self.cunning: 
            self.physics.nogoal()
            self.state = INTERCEPTING
        
        # If our prey is putting up a defense, engage.
        if self.prey.state == FIGHTING:
            self.state = FIGHTING
        
        # Engage when close enough.
        if self.distance(self.prey) < 100:
            self.fight(self.prey)
            self.state = FIGHTING
            
        if random() > self.cunning and random() > self.ferocity:
            self.prey = None
            self.state = ROAMING
    
    def evade(self, creature):
        
        # The prey either runs away from the predator,
        # attempts to fight it,
        # attempts to hide in the flock,
        # or continues its path as usual.
        # A constant switching between these three 
        # gives a feel of eratic, life/death confusion.
        self.flocking = False
        self.update()
        if random() < self.cunning:
            self.physics.goal(creature.x, creature.y, creature.z, flee=True)
            self.state = FLEEING
        if random() < self.ferocity:
            self.physics.goal(creature.x, creature.y, creature.z)
            self.state = FIGHTING
        if random() < self.cunning and self.ferocity < creature.ferocity*2:
            self.flocking = True
            self.state = FLOCKING            
            
    def fight(self, creature):
        
        # The higher a creature's ferocity,
        # the higher its chance of inflicting damage
        # on its victim.
        if random() < self.ferocity: creature.health *= 0.8
    
    def distance(self, creature):
        
        dx = self.x - creature.x
        dy = self.y - creature.y
        dz = self.z - creature.z
        return sqrt(dx*dx + dy*dy + dz*dz)
        
    def offscreen(self):
        
        if 0 < self.x < _ctx.WIDTH or 0 < self.y < _ctx.HEIGHT:
            return False
        for x, y, z in self.trail:
            if 0 < x < _ctx.WIDTH or 0 < y < _ctx.HEIGHT:
                return False
        return True
        
    def draw(self, alpha=1.0):

        _ctx.nofill()
        for i in range(len(self.trail)):
            
            x, y, z = self.trail[i]
            
            a = 1.0 * i / len(self.trail) * (self.health/self.fitness)
            _ctx.stroke(0, 0, 0, 0.5*a*alpha)
            
            #if i < len(self.trail)-3 \
            #and self.name == None:
            r = min(15, abs(z/5))
            _ctx.oval(x-r/2, y-r/2, r, r)
            if i > 0:
                dx = self.trail[i-1][0]
                dy = self.trail[i-1][1]                
                _ctx.line(x, y, dx, dy)
                
            if i >= len(self.trail)-3 \
            and self.name != "":
                _ctx.push()
                w, h = _ctx.imagesize(self.image_small)
                z = min(100, max(z, 0)) * 0.01
                _ctx.translate(x-w/2, y-h/2)
                _ctx.scale(0.3 + z*0.8 * i/len(self.trail))
                _ctx.rotate(self.r-90)
                _ctx.image(self.shadow_small, 5+z*50, 5+z*50, alpha=(a*0.3*(1-z))*alpha)
                _ctx.image(self.image_small, 0, 0, alpha=(0.25+a)*alpha)
                _ctx.pop()
                
    ### RULES
    
    def threatened(self, predator):
        # Is the predator too close?
        if self.distance(predator) < 200: return True
        else: return False
        
    def hunted(self, predator):
        # Is the predator planning to eat me?
        if predator.prey == self: return True
        else: return False
        
    def attacked(self, predator):
        # Is the predator busy eating me?
        if predator.prey == self and predator.state == FIGHTING: return True
        else: return False
        
    def ambushed(self, predator):
        # Is the predator planning a strategic move to catch me?
        if predator.prey == self and predator.state == INTERCEPTING: return True
        else: return False
        
    def fighting(self, predator):
        if self.hunted(predator) and self.state == FIGHTING: return True
        else: return False
        
    def dying(self):
        if self.health < 0.1*self.fitness: return True
        else: return False
        
class Flock:
    
    def __init__(self):
        
        self.creatures = []
        boids = _ctx.ximport("flocking")
        self.physics = boids.Boids(0, 0, 0, _ctx.WIDTH, _ctx.HEIGHT)
        self.separation = 0
        self.velocity = 0
    
    def add(self, creature):
        
        # Adds the creature to the flock.
        # Sets the creature's status to flocking,
        # so its motion is regulated by this flock.
        boids = _ctx.ximport("flocking")
        boid = boids.Boid(self.physics.boids, creature.x, creature.y, creature.z)
        creature.flocking = True
        creature.flock = self
        creature.boid = boid
        self.creatures.append(creature)
        self.physics.boids.append(boid)
        
        # Update the average separation and velocity.
        self.velocity = 0
        self.separation = 0
        for creature in self.creatures:
            self.velocity += creature.velocity
            self.separation += creature.fitness
        self.velocity /= len(self.creatures)
        self.separation /= len(self.creatures)
        
    def update(self):

        # Updates the flock if there are enough flocking creatures.
        if len(self.physics.boids) > 1:
            self.physics.update(cohesion=100, 
                                separation=10+10*self.separation,
                                limit=30*self.velocity)
            
        # Updates each creature.
        # Flocking creatures will use the coordinates calculated by this flock,
        # others follow their own path.
        for creature in self.creatures: creature.update()

class Animation:
    
    def __init__(self):
        
        self.prey = None
        self.flock = None
        self.predator = None
        
        self.frames = 600
        self.i = 0
        self.done = True
        
    def load(self, prey, predator, flock=3):
    
        self.prey = Dragon(name=prey)
        self.flock = Flock()
        for i in range(flock): 
            creature = Dragon(name=prey)
            self.flock.add(creature)

        x = random(_ctx.WIDTH)
        y = random(2000,3000)
        z = random(100)
        self.predator = Dragon(x, y, z, name=predator)
    
    def polarise(self):
        
        self.predator.polarise()
        for creature in self.flock.creatures:
            creature.polarise()
    
    def dashboard_clock(self, x, y, alpha=1.0):
        
        # An emptying oval
        # indicating the time remaining.
        r = 40.0
        remaining = r * (self.frames-self.i)/self.frames
        _ctx.fill(1,1,1,0.6*alpha)
        _ctx.oval(x-remaining/2, y-remaining/2, remaining, remaining) 
        _ctx.fill(0,0,0,0.25*alpha)
        _ctx.stroke(1,1,1,0.6*alpha)
        _ctx.strokewidth(1)
        _ctx.oval(x-r/2, y-r/2, r, r)        
        
    def dashboard_meter(self, creature, x, y, alpha=1.0):

        # An indicator bar 
        # of the creature's health.
        h = 60 * creature.fitness
        _ctx.fill(0,0,0,0.25*alpha)
        _ctx.stroke(1,1,1,0.6*alpha)
        _ctx.rect(x, y-h, 10, h)
        _ctx.nostroke()
        dh = 60 * creature.health
        _ctx.fill(1,1,1,0.4*alpha)
        _ctx.rect(x, y-dh, 10, dh)

    def dashboard_portrait(self, creature, x, y, alpha=1.0):
    
        # A thumbnail picture of the creature
        # and it's name.
        r = 80
        _ctx.fontsize(12)
        _ctx.align(CENTER)   
        _ctx.fill(1,1,1,0.6*alpha)
        _ctx.text(creature.name.upper(), x-r/2, y+60, width=r)
        _ctx.fill(0,0,0,0.25*alpha)
        _ctx.stroke(1,1,1,0.6*alpha)
        _ctx.strokewidth(1)
        _ctx.oval(x-r/2, y-r/2, r, r)
        _ctx.image(creature.image_clipped, x-75, y-75, alpha=alpha)
    
    def dashboard(self, x, y, alpha=1.0):
        
        # Information about the current game,
        # the creatures, their health, etc.
        self.dashboard_portrait(self.predator, x, y, alpha)
        self.dashboard_portrait(self.prey, x+90, y, alpha)
        if not self.predator.dying():
            self.dashboard_meter(self.predator, x-5, y-50, alpha)
        if self.flock:
            x += 85 -  7.5*(len(self.flock.creatures)-1)
            for creature in self.flock.creatures:
                self.dashboard_meter(creature, x, y-50, alpha)
                x += 15
        self.dashboard_clock(_ctx.WIDTH-85, y, alpha)
    
    def setup(self):
        
        if not self.flock:
            import os
            prey = os.path.basename(choice(files("creatures/*")))
            predator = os.path.basename(choice(files("creatures/*")))
            self.load(prey, predator)
        self.done = False
        self.i = 0
    
    def frame(self):
        
        _ctx.image("g/arena.jpg", 0, 0, width=_ctx.WIDTH, height=_ctx.HEIGHT)
    
        #flock.physics.goal(MOUSEX, MOUSEY, 0)
        #fill(0, 0, 0, 0.2)
        #oval(MOUSEX-30, MOUSEY-30, 60, 60)
        
        if not self.flock or self.predator.dying():
            self.i += 2
        
        self.i += 1
        if self.i > self.frames or self.done: 
            self.done = True
            return
            
        # These values are multiplied with each alpha,
        # simulating a fade in and a fade out.
        fin = min(25, self.i) * 0.04
        fout = min(25, self.frames-self.i) * 0.04

        # Keep the flock onscreen
        if self.flock:
            self.flock.physics.goal(_ctx.WIDTH/2, _ctx.HEIGHT/2, 20) 
            if random() > 0.5: self.flock.physics.nogoal()
            self.flock.update()
        
        if not self.predator.dying():
            self.predator.update()
        
        # The predator chases the flock.
        # Flocking creatures that are within range
        # scatter and evade the predator.
        if not self.predator.dying() and self.flock:
            self.predator.chase(self.flock)
            for creature in self.flock.creatures:
                if creature.threatened(self.predator):
                    creature.evade(self.predator)
                else:
                    creature.physics.nogoal()
                    creature.flocking = True
                if creature.attacked(self.predator):
                    self.predator.fight(creature)
                if creature.fighting(self.predator):
                    creature.fight(self.predator)
                if random() > 0.9 and creature.state == FIGHTING:
                    creature.fight(self.predator)
                if creature.dying():
                    food = creature.fitness * 0.5
                    self.predator.health = min(self.predator.health+food, self.predator.fitness)
                    self.flock.creatures.remove(creature)
                    if len(self.flock.creatures) == 0: 
                        self.flock = None
                        self.predator.state = ROAMING
                        self.predator.physics.goal(_ctx.WIDTH/2, _ctx.HEIGHT/2, 0)
                if self.predator.dying():
                    self.predator.state = ROAMING
                    self.predator.y = -2000
                    for creature in self.flock.creatures:
                        creature.flocking = True
                    self.flock.physics.goal(-2000, -2000, 0)

        _ctx.fill(1,1,1, 0.75)
        _ctx.font("Helvetica-Bold")

        # Draw all the creatures.
        # Display their health levels when fighting.
        if self.flock:
            for creature in self.flock.creatures:
                creature.draw(alpha=fout)
                if creature.state == FIGHTING:
                    _ctx.fill(1, 1, 1, 0.75*fout)
                    _ctx.fontsize(12)
                    _ctx.text(creature.state.upper(), creature.x, creature.y)
                    _ctx.fontsize(20)
                    _ctx.text(str(int(creature.health*100)), 
                        creature.x, creature.y + _ctx.fontsize())
                    _ctx.fill(1,0,0, 0.75*fout)
                    _ctx.oval(creature.x-4, creature.y-4, 8, 8)

        # Draw the predator.
        # Display his state (i.e. what it is thinking).
        # Display his health when fighting.
        if not self.predator.dying():
            self.predator.draw(alpha=fout)
            _ctx.fill(1, 1, 1, 0.75*fout)
            _ctx.fontsize(12)
            _ctx.text(self.predator.state.upper(), self.predator.x, self.predator.y)
            if self.predator.state == FIGHTING:
                _ctx.fill(1, 1, 1, 0.75*fout)
                _ctx.fontsize(20)
                _ctx.text(str(int(self.predator.health*100)), 
                     self.predator.x, self.predator.y + _ctx.fontsize())
                _ctx.fill(1,0,0, 0.75*fout)
                _ctx.oval(self.predator.x-4, self.predator.y-4, 8, 8)
            #_ctx.line(predator.x, predator.y, predator.prey.x, predator.prey.y)
        
        self.dashboard(65, 520, alpha=fin*fout)


if __name__ == '__builtin__':
    speed(100)
    size(800,600)

    def setup():
        import pprint
        global a
        a = Animation()
        fls = files("creatures/*")
        shuffle(fls)
        shuffle(fls)
        c1 = fls.pop().split('/')[1]
        c2 = fls.pop().split('/')[1]
        pprint.pprint((c1,c2))
        # a.load("Timude", "Docole", flock=3)
        a.load(c1, c2, flock=5)
        a.setup()
        a.polarise()
    
    def draw():
        global a
        a.frame()
