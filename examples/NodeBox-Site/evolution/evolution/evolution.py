
import importlib
try:
    reload = importlib.reload
except:
    pass

size(800, 600)
speed(100)


factory = ximport("factory")
reload(factory)

arena = ximport("arena")
reload(arena)

TRANSITION_FROM_FACTORY = 40
TRANSITION_FROM_ARENA = 140

e = ""

class Evolution:
    
    def __init__(self):
        
        self.factory = factory.Animation()
        self.arena = arena.Animation()
        
        self.genes = []
        self.fittest = None
        self.predator = None
        self.prey = None
        
        self.transition = 0
        self.i = 0
        self.message = ""
        
def setup():
    
    global e
    
    e = Evolution()
    e.factory.setup()
    e.factory.tag = "predator:"
    
    e.factory.frames = 350
    e.arena.frames = 700
    
def draw():
   
    global e
    
    # In between transition of backgrounds,
    # and some score messages that are displayed.
    if e.i < e.transition:
        e.i += 1
        a = 1.0 * e.i / e.transition
        fin = min(20, e.i) * 0.05
        fout = min(20, e.transition-e.i) * 0.05
        if e.transition == TRANSITION_FROM_FACTORY:
            image("g/factory.jpg", 0, 0, width=_ctx.WIDTH, height=_ctx.HEIGHT)
            image("g/arena.jpg", 0, 0, width=_ctx.WIDTH, height=_ctx.HEIGHT, alpha=a)
        if e.transition == TRANSITION_FROM_ARENA:
            image("g/arena.jpg", 0, 0, width=_ctx.WIDTH, height=_ctx.HEIGHT)
            image("g/factory.jpg", 0, 0, width=_ctx.WIDTH, height=_ctx.HEIGHT, alpha=a)
            font("Helvetica-Bold", 20)
            align(CENTER)
            
            y = (600 - textheight(e.message.upper())) * 0.5
            fill(0,0,0, 0.1*fin*fout)
            text(e.message.upper(), 160, y+10, width=500)
            
            fill(1,1,1, 0.75*fin*fout)
            text(e.message.upper(), 150, y, width=500)

    # The animation ix inside the factory or the arena.
    # Let those objects do the rendering.
    else:
        e.transition = 0
        e.i = 0
        e.message = ""
        if not e.factory.done: e.factory.draw()
        if not e.arena.done: e.arena.frame()
    
    # In between preparation of stuff.
    if e.factory.done and e.arena.done:

        # Get the spawned predator from the factory,
        # prepare to spawn some prey.
        if e.predator == None:
            e. predator = e.factory.creature
            e.factory.creature = None
            e.factory.mutated = False
            e.factory.recombined = False
            e.factory.parents = []
            e.factory.setup()
            e.factory.tag = "prey:"
        
        # Get the spawned prey from the factory,
        # prepare the arena with the prey and predator.
        elif e.prey == None:
            e.prey = e.factory.creature
            e.factory.creature = None
            e.arena.load(e.prey.name, e.predator.name)
            e.arena.setup()
            e.transition = TRANSITION_FROM_FACTORY
        
        # If the match was a draw, mutate the predator.
        # If the prey won it becomes the predator in the next fight.
        # If the predator won, use it to recombine new predator's.
        else:
            e.fittest = None
            if e.arena.predator.dying(): e.fittest = e.arena.prey
            if e.arena.flock == None: e.fittest = e.arena.predator
            if e.fittest == None:
                e.factory.mutate(e.predator.name)
                e.message = ("The match was a draw.\n"
                             "Retrying with a mutation of the "
                             "%s predator.") % (e.predator.name,)
            elif e.fittest.name == e.prey.name:
                e.factory.spawn(e.prey.name)
                e.message = ("The %s prey is fit enough "
                             "to hunt other creatures.") % (e.prey.name,)
            elif e.fittest.name == e.predator.name:
                e.genes.append(e.predator)
                e.message = ("The %s predator is fit enough\n"
                             "to join the gene pool.") % (e.predator.name,)
                if len(e.genes) >= 2:
                    c1 = e.genes[-1]
                    c2 = e.genes[-2]
                    e.factory.recombine(c1.name, c2.name)
                    e.message += ( "\nGeneration " + str(len(e.genes))
                                 + " will be recombined from " + c1.name)
                    if c1.name != c2.name: e.message += " and "+c2.name
                    e.message += " genes."
            e.prey = None
            e.predator = None
            e.factory.setup()
            e.factory.tag = "predator:"
            e.transition = TRANSITION_FROM_ARENA
