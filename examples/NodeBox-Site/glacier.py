size(1200, 900)
halfwidth = int( WIDTH / 2 )
halfheight = int( HEIGHT / 2 )

from random import shuffle
 
hexwork = {}
 
class Hex:
 
    def __init__(self, x, y, w, spacing=0):
 
        #Creates a new hexagonal at position x, y
        #with the given width w, and optional spacing.
        #Adds itself to the hexwork list.
 
        self.x = x
        self.y = y
        self.w = w
        self.spacing = spacing
 
        self.sides = []
        for i in range(6): 
            self.sides.append(None) 
        global hexwork
        hexwork[(self.x,self.y)] = self
        self.index = len(hexwork)
 
    def draw(self, tag=False, visit=None):
 
        #Draws this hexagonal on screen.
        #Optionally, tags the hexagonal with its index
        #in the hexwork list.
 
        #Additionally, you can supply a visit function
        #that accepts this self as a parameter.
 
        if visit != None:
            visit(self)
 
        w = self.w * 0.5
        star(self.x, self.y, 6, w, w*1.155)
 
        if tag:
            fontsize(w*0.25)
            f = fill()
            fill(f.r, f.g, f.b, 1)
            align(CENTER)
            text(str(self.index),
                 self.x - self.w * 0.5,
                 self.y,
                 self.w)
            fill(f)
 
    def rdraw(self, tag=False, visit=None, degrade=True, root=None):
 
        #Recursive draw:
        #draw all neighbours as well,
        #and their neighbours, and so on.
 
        if degrade == True: 
            f = fill()
            fill(f.r, f.g, f.b, f.a * 0.98)
 
        self.draw(tag, visit)

        if root != None:
            line(self.x,self.y,root.x,root.y)

        for side in self.sides:
            if side != None and side != root:
                side.rdraw(tag, visit, degrade, root=self)
 
    def grow(self, max_=6):
 
        #Creates neighbouring hexes for this hexagonal.
        #Creates all neighbours by default, or a given max
        #of random neighbours.
 
        if max_ < 1 or max_ > 12: return
 
        #The centerpoint offsets for neighbouring hexes.
 
        
        center = [(0,-1),
                  (-0.865,-0.5),
                  (-0.865,0.5),
                  (0,1),
                  (0.865,0.5),
                  (0.865,-0.5)]
 
        shuffle(center)
        center = center[:max_]
        #center.sort() #doesn't do what supposed to do
 
        #Create neighbours only if the neighbour does
        #not exist yet: if it is not defined by this
        #hex as a neighbour already, or its position
        #occurs in the hexwork list (and thus it is
        #already defined as someone else's neighbour).
 
        for i in range(max_):
            dx, dy = center[i]
            dx = dx * (self.w+self.spacing) + self.x
            dy = dy * (self.w+self.spacing) + self.y

            global hexwork

            if self.sides[i] == None and not (dx,dy) in hexwork:
                self.sides[i] = Hex(dx, dy, self.w)
                self.sides[i].sides[(i+3)%6] = self
 
    def rgrow(self, max_=6):
 
        #Recursive growth:
        #grow neighbours for this hex,
        #grow neighbours for each neighbour, and so on.
 
        if max_ > 0:
            self.grow(max_=max_)
            for side in self.sides:
                if side != None: 
                    side.rgrow(max_-1)
 
def visit(hex):                      
    scale(random(0.98,1.01))
    rotate(0.1)
 
root = Hex(halfwidth, halfheight, 70, spacing=100)
root.rgrow(max_=6)
 
nofill()
stroke(0.2,0.2,0.2)
strokewidth(0.5)
rect(0,0,WIDTH,HEIGHT)
 
font("Arial")
r = random(0.5,1)
fill(0,0.5,r,0.75)
stroke(0,0.5,r,0.75)
strokewidth(0.25)
root.rdraw( tag=True, visit=visit )
