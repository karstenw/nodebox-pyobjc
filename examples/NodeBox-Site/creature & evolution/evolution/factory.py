
from __future__ import print_function

import os
import importlib
try:
    reload = importlib.reload
except:
    pass

import math
sin = math.sin
cos = math.cos
radians = math.radians


from random import choice
from nodebox.util import files, random
from nodebox.graphics import CENTER, LEFT
from creatures import Creature
from uberwords import uberword

class Components:
    
    def __init__(self):
        
        self.images = {}
        
        for folder in files("factory/*"):
            type = os.path.basename(folder)
            self.images[type] = []
            for png in files(folder+"/*"):
                self.images[type].append(png)
            
    def head(self): return choice(self.images["head"])
    def body(self): return choice(self.images["body"])
    def tail(self): return choice(self.images["tail"])
    def paddle(self): return choice(self.images["paddle"])
    def spike(self): return choice(self.images["spike"])

class Factory:
    
    def __init__(self):
        
        self.components = Components()
    
    def label(self, name1="", name2=""):
        
        # Recombines two given names
        # if they have the same length.
        if len(name1) == len(name2) > 0:
            name3 = ""
            for i in range(len(name1)):
                name3 += choice((name1[i], name2[i]))
            return name3
        
        # Returns Africanish names for creatures.
        return uberword(6, True)
        
    def dna(self, creature=None):
        
        # If a given creature,
        # return that creature's dna:
        # the Factory.creature() method
        # will create a copy of the creature.
        if creature:
            return (creature.flippers,
                    creature.tentacles,
                    creature.heads,
                    creature.tails,
                    creature.cores,
                    creature.knob)
        
        flippers = []
        tentacles = []
        heads = []
        tails = []
        cores = []
        
        # Fetch random components
        # to construct a creature with.
        if random() > 0.5: 
            flippers.append(self.components.paddle())
        spike = self.components.spike()
        for i in range(random(5)*2): tentacles.append(spike)
        if random() > 0.8: 
            heads.append(self.components.head())
        body = self.components.body()
        for i in range(random(2,5)): cores.append(body)
        knob = self.components.body()
        
        return (flippers, tentacles, heads, tails, cores, knob)
        
    def recombine(self, dna1, dna2=None):
        
        # Recombines the DNA of two creatures,
        # either both given or one random (mutation).
        # Traverses all the properties in the DNA,
        # i.e. the components a creature is built of,
        # and stuffs them randomly from both creatures
        # into the DNA of a third creature.
        # This DNA can then be passed to Factory.creature()
        if dna2 == None: dna2 = self.dna()
        dna3 = [[],[],[],[],[], None]
        for i in range(len(dna1)):
            if type(dna1[i]) == list:
                n = random(len(dna1[i]), len(dna2[i]))
                for j in range(n):
                    if len(dna1[i]) == 0: x = None
                    else: x = choice(dna1[i])
                    if len(dna2[i]) == 0: y = None
                    else: y = choice(dna2[i])
                    z = choice((x,y))
                    if z != None: dna3[i].append(z)
            else:
                x = dna1[i]
                y = dna2[i]
                dna3[i] = choice((x, y))
            
        return dna3
        
    def creature(self, dna=None, errors=False, names=("","")):
        
        creature = Creature()
        creature.name = self.label(names[0],names[1])
        
        # Creatures are rendered against a grey background,
        # which gives a neutral colorisation.
        # The empty.png fixes a weird PhotoBot compositing bug.
        photobot = _ctx.ximport("photobot")
        reload(photobot)
        canvas = photobot.canvas(400, 400)
        canvas.fill((128,128,128,0))
        canvas.layer("factory/empty.png", 0, 0)
                
        x = 200
        y = 200
        
        # Construct a dna of components to build a creature with.
        # Either the Factory.dna() returns some random components,
        # or you can supply your own dna,
        # for example something returned from Factory.recombine()
        # which exchanges the dna of two creatures.
        if dna == None:
            flippers, tentacles, heads, tails, cores, knob = self.dna()
        else:
            flippers, tentacles, heads, tails, cores, knob = dna

        # The bottom layer is (optionally) 
        # made up of left and right flippers.
        # Flippers enhance the creature's velocity.
        creature.velocity = 0.5
        if len(flippers) > 0:
            flipper = flippers[0]
            w, h = _ctx.imagesize(flipper)
            j = canvas.layer(flipper, x-w, y-h/2)
            canvas.layers[j].brightness(1.2)
            canvas.layers[j].duplicate()
            canvas.layers[j].flip()
            canvas.layers[j].translate(x, y-h/2)
            creature.velocity += min(1,w*h/10000) * 0.5
            creature.flippers.append(flipper)

        # This rules out genetic flaws 
        # originating from recombination,
        # things like 3 tentacles or mixed tentacles.
        if not errors:
            if len(tentacles) > 0 and len(tentacles) % 2 == 1:
                del tentacles[0]
            for i in range(len(tentacles)):
                tentacles[i] = tentacles[0]

        # On top of flippers come 0-8 tentacles.
        # Tentacles enhance the creature's ferocity.            
        if len(tentacles) > 0:
            n = len(tentacles)
            i = 0
            
            for tentacle in tentacles:
                w, h = _ctx.imagesize(tentacle)
                j = canvas.layer(tentacle, x-w/2, y-h/2)
                canvas.layers[j].brightness(1.3)
                if n <= 5: a = -90+90/n + 180/n * i
                else: a = -180 + 360/n * i
                if tentacle.find("cel-26") > 0 and i == 3 and n > 4: 
                    if n == 6: a -= 180
                    if n == 8: a -= 135
                    canvas.layers[j].flip()
                if tentacle.find("cel-33") > 0 and i == 0 and n > 4:
                    if n == 6: a -= 180
                    if n == 8: a -= 180
                    canvas.layers[j].flip()
                dx = h/2 * sin(radians(a)) + x-w/2
                dy = h/2 * cos(radians(a)) + y-h/2
                if -180 < a < 0: canvas.layers[j].flip()
                canvas.layers[j].translate(int(dx), int(dy))
                canvas.layers[j].rotate(a)
                creature.tentacles.append(tentacle)
                i += 1
            creature.ferocity = 1.0 * n / 8 * min(1,w*h/15000)

        # Below the body comes (optionally) a head.
        # A head enhances the creature's cunning.
        if len(heads) > 0:
            head = heads[0]
            w, h = _ctx.imagesize(head)
            j = canvas.layer(head, x-w/2, y-h+50)
            canvas.layers[j].brightness(1.2)
            creature.cunning = 0.3
            creature.heads.append(head)
        
        # On top comes the body.
        # The body determines the creature's fitness:
        # more volume and layers add more fitness.
        # The numer of layers influences cunning as well.
        creature.fitness = 0.25
        if len(cores) > 0:
            n = len(cores)
            s = (0,0)
            for core in cores:
                creature.cores.append(core)
                w, h = _ctx.imagesize(core)
                j = canvas.layer(core, x-w/2, y-h/2)
                canvas.layers[j].brightness(1.2)
                s = (max(s[0],w), max(s[1],h))
            creature.fitness += min(1, s[0]*s[1]/100000) * 0.4
            creature.fitness += 1.0 * n/5 * 0.35
            creature.cunning += 0.7 * n/5

        # Desaturate the creature
        canvas.flatten()
        canvas.layers[1].desaturate()
        canvas.layers[1].brightness(1.2)

        # A bluish glow emanates from the creature.
        canvas.fill((0,150,255))
        canvas.layers[-1].multiply()
        canvas.gradient(photobot.RADIAL)
        canvas.layers[-1].mask()
        
        # Put another body on top,
        # this is the creature's "knob",
        # since it is colored it tends to stick out.
        if knob:
            w, h = _ctx.imagesize(knob)
            j = canvas.layer(knob, x-w/2, y-h/2)
            #canvas.layers[j].duplicate()
            #canvas.layers[j+1].desaturate()
            #canvas.layers[j+1].opacity(50)
            canvas.layers[j].brightness(1.2)  
            canvas.layers[j].multiply()  
            creature.knob = knob
        
        # Create the creature image
        path = "creatures/"+creature.name
        creature.image = path+"/"+creature.name+".png"
        try:
            os.mkdir(path)
        except:
            print( creature.name, "was overwritten" )
        creature.image = canvas.export(creature.image)
        
        # Create the dropshadow
        # Brightness must not be adjusted on the alpha mask.
        canvas.flatten()
        canvas.layers[1].desaturate()
        img = canvas.layers[1].img
        alpha = canvas.layers[1].img.split()[3]
        canvas.layers[1].brightness(0.1)
        canvas.layers[1].img.putalpha(alpha)
        canvas.layers[1].blur()
        
        path = "creatures/"+creature.name
        creature.shadow = path+"/"+creature.name+"-shadow.png"
        creature.shadow = canvas.export(creature.shadow)
        
        # Create smaller thumbnails
        w = 150
        h = 150
        canvas = photobot.canvas(w,h)
        canvas.layer(creature.image)
        canvas.layers[1].scale(w,h)
        creature.image_small = path+"/"+creature.name+"-small.png"
        creature.image_small = canvas.export(creature.image_small)
        canvas = photobot.canvas(w,h)
        canvas.layer(creature.shadow)
        canvas.layers[1].scale(w,h)
        creature.shadow_small = path+"/"+creature.name+"-shadow-small.png"
        creature.shadow_small = canvas.export(creature.shadow_small)

        # Create a clipped thumbnail to place in a circle.
        canvas = photobot.canvas(w,h)
        canvas.layer(creature.image_small)
        canvas.layer("factory/circle.jpg")
        canvas.layers[2].invert()
        canvas.layers[2].mask()
        creature.image_clipped = path+"/"+creature.name+"-clipped.png"
        creature.image_clipped = canvas.export(creature.image_clipped)
        
        # Store the creature's statistics in a file
        f = open(path+"/dna.txt", "w")
        f.write(creature.name+"\n")
        f.write(str(creature.fitness)+"\n")
        f.write(str(creature.cunning)+"\n")
        f.write(str(creature.velocity)+"\n")
        f.write(str(creature.ferocity)+"\n")
        f.write(",".join(creature.cores)+"\n")
        f.write(",".join(creature.heads)+"\n")
        f.write(",".join(creature.tails)+"\n")
        f.write(",".join(creature.tentacles)+"\n")
        f.write(",".join(creature.flippers)+"\n")
        f.write(str(creature.knob)+"\n")
        f.close()
        
        return creature

class Animation:
    
    def __init__(self):
        
        self.factory = Factory()
        self.creature = None
        
        self.recombined = False
        self.mutated = False
        self.parents = []
        
        self.tag = ""
        
        self.frames = 600
        self.i = 0
        self.done = True
        
    def spawn(self, creature):
        
        self.creature = Creature()
        self.creature.spawn(creature)
        return self.creature
        
    def recombine(self, creature1, creature2):
        
        c1 = Creature()
        c1.spawn(creature1)
        dna1 = self.factory.dna(c1)
        
        if creature2 != None:
            c2 = Creature()
            c2.spawn(creature2)
            dna2 = self.factory.dna(c2)
        else:
            c2 = None
            dna2 = None
        
        dna3 = self.factory.recombine(dna1, dna2)
        if c2 == None: names = (c1.name, self.factory.label())
        else: names = (c1.name, c2.name)
        self.creature = self.factory.creature(dna3, names=names)
        
        self.recombined = True
        self.parents = [c1, c2]
        return self.creature
        
    def mutate(self, creature):
        
        c = self.recombine(creature, None)
        self.mutated = True
        return c
        
    def setup(self):
        
        if not self.creature:
            self.creature = self.factory.creature()
        self.done = False
        self.i = 0
    
    def draw(self):
        
        _ctx.image("g/factory.jpg", 0, 0, width=_ctx.WIDTH, height=_ctx.HEIGHT) 
        
        self.i += 1
        if self.i > self.frames or self.done: 
            self.done = True
            return

        # These values are multiplied with each alpha,
        # simulating a fade in and a fade out.
        fin = min(100, self.i-10) * 0.01
        fout = min(100, self.frames-self.i) * 0.01

        # Fluid spring motion
        w, h = _ctx.imagesize(self.creature.image)
        x = (_ctx.WIDTH-w)/2
        y = (_ctx.HEIGHT-h)/2
        d = (1+sin(radians(self.i % 360))) * 0.5
        
        _ctx.nofill()
        _ctx.stroke(1,1,1,0.5*fin*fout)
        _ctx.strokewidth(0.5)
        #_ctx.oval(x+w/2-75, y+h/2-75, 150, 150)
        _ctx.nostroke()
        
        # Draw the creature and it's dropshadow.
        # The creature rotates slowly,
        # and zooms in and out.
        # An arrow indicates it's heading.
        _ctx.push()
        _ctx.scale(0.4+d*0.8)
        _ctx.rotate(self.i*2)
        _ctx.image(self.creature.image, x, y, alpha=fin*fout)
        _ctx.image(self.creature.shadow, x+15, y+15, alpha=(0.3-d*0.2)*fin*fout)
        _ctx.translate(0, -h/4)
        #_ctx.skew(-d*5)
        _ctx.rotate(90)
        _ctx.fill(1,1,1,0.75*fin*fout)
        _ctx.arrow(x+w/2, y+h/2, 30)
        _ctx.fill(0,0,0,(0.2-d*0.1)*fin*fout)
        _ctx.arrow(x+w/2+15, y+h/2+15, 25)
        _ctx.pop()
        
        x += w/2
        y += h/2+120
        
        # The creature's statistics in legible format.
        _ctx.fill(1,1,1,0.75*fin*fout)
        _ctx.align(LEFT)
        _ctx.lineheight(0.95)
        _ctx.font("Helvetica-Bold", 10)
        s  = "FITNESS " + str(int(self.creature.fitness*100)) + " / 100\n"
        s += "CUNNING " + str(int(self.creature.cunning*100)) + " / 100\n"
        s += "VELOCITY " + str(int(self.creature.velocity*100)) + " / 100\n"
        s += "FEROCITY " + str(int(self.creature.ferocity*100)) + " / 100\n"
        _ctx.text(s, x, y)
        #_ctx.fill(0,0,0,0.1*fin*fout)
        #_ctx.text(s, x+10, y+10)
        
        # Label indicating recombination or mutation.
        if self.recombined: label = "RECOMBINED"
        if self.mutated: label = "MUTATED"
        if not self.recombined and not self.mutated: label = "SPAWNED"
        dw = _ctx.textwidth(label)
        dh = _ctx.fontsize()
        _ctx.fill(1,1,1,0.75*fin*fout)
        _ctx.rect(x+5, y-30, dw, dh*1.2)
        _ctx.fill(0,0,0,0.1*fin*fout)
        _ctx.rect(x+10, y-30+10, dw, dh*1.3)
        _ctx.fill(0,0,0, 0.65*fin*fout)
        _ctx.text(label, x+5, y-30+_ctx.fontsize())
        
        # The creature's name.
        _ctx.fill(1,1,1,0.75*fin*fout)
        _ctx.fontsize(20)
        _ctx.text(self.creature.name.upper(), x, y-40)
        _ctx.fill(0,0,0,0.1*fin*fout)
        _ctx.text(self.creature.name.upper(), x+10, y-40+10)

        #An optional caption tag you can define.
        _ctx.fontsize(10)
        #_ctx.fill(0,0,0,0.1*fin*fout)
        #_ctx.text(self.tag.upper(), x+10, y-60+10)
        _ctx.fill(1,1,1,0.6*fin*fout)
        _ctx.text(self.tag.upper(), x, y-60)
        
        # When recombining,
        # display a snapshot of the ancestors.
        if self.recombined:
            x =  -10
            y = _ctx.HEIGHT - 160
            _ctx.fill(0,0,0,0.1*fin*fout)
            _ctx.stroke(1,1,1,0.6*fin*fout)
            _ctx.strokewidth(1)
            r = 80
            _ctx.oval(x+75-r/2, y+75-r/2, r, r)
            _ctx.image(self.parents[0].image_clipped, x, y, alpha=fin*fout)
            if self.parents[1] != None:
                _ctx.oval(x+90+75-r/2, y+75-r/2, r, r)
                _ctx.image(self.parents[1].image_clipped, x+90, y, alpha=fin*fout)
            _ctx.fontsize(12)
            _ctx.align(CENTER)
            _ctx.fill(1,1,1,0.6*fin*fout)
            _ctx.text(self.parents[0].name.upper(), x+75-r/2, y+135, width=r)
            if self.parents[1] != None:
                _ctx.text(self.parents[1].name.upper(), x+95+75-r/2, y+135, width=r)

