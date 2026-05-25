

from __future__ import print_function

class Creature:
    
    def __init__(self):
        
        # The creature's name.
        self.name = ""
        
        # Statistics that describe
        # the creature's behavior.
        self.fitness = 0
        self.cunning = 0
        self.velocity = 0
        self.ferocity = 0
    
        # The creature's body components,
        # it's DNA structure.
        self.cores = []
        self.heads = []
        self.tails = []
        self.tentacles = []
        self.flippers = []
        self.knob = None
    
        # A path storing a PNG of the creature
        # and a dropshadow.
        self.image = None
        self.shadow = None
        self.image_small = None
        self.shadow_small = None
        self.image_clipped = None
        
    def spawn(self, name):
        
        # Load a creature from file,
        # stored in the folder with the given name.
        try:
            dna = open("creatures/"+name+"/dna.txt").readlines()
        except:
            print("Can't find", name, "creature")
            return

        self.name = dna[0].strip()
        self.fitness = float(dna[1])
        self.cunning = float(dna[2])
        self.velocity = float(dna[3])
        self.ferocity = float(dna[4])
        
        components = [self.cores, 
                      self.heads, 
                      self.tails, 
                      self.tentacles, 
                      self.flippers]
        for i in range(len(components)):
            component = components[i]
            for x in dna[5+i].split(","):
                x = x.strip("\n")
                if x != "": component.append(x)

        self.knob = dna[10].strip()
        self.image = "creatures/"+name+"/"+name+".png"
        self.shadow = "creatures/"+name+"/"+name+"-shadow.png"
        self.image_small = "creatures/"+name+"/"+name+"-small.png"
        self.shadow_small = "creatures/"+name+"/"+name+"-shadow-small.png"
        self.image_clipped = "creatures/"+name+"/"+name+"-clipped.png"
