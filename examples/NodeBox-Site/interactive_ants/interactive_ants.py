try:
    ants = ximport("ants")
    colors = ximport("colors")
 
except:
    ants = ximport("__init__")
    reload(ants)
 
size(500,500)
speed(200)
 
clr = colors.rgb(0.6, 0.4, 0, 0.5)
 
def setup():    
    
    # Starts a colony with 30 ants in it.
    global colony, has_clicked
    colony = ants.colony(20, WIDTH/2, HEIGHT/2, 100)
    
    # Add some food in the vicinity of the colony.
    for i in range(0):
        x = 50 + random(WIDTH-100)
        y = 50 + random(HEIGHT-100)
        s = random(20,40)
        colony.foodsources.append(ants.food(x,y,s))
 
 
        
def draw():
    global colony, has_clicked
 
    if mousedown:
        if not has_clicked:
            x = MOUSEX
            y = MOUSEY
            s = random(20,40)
            colony.foodsources.append(ants.food(x,y,s))
            has_clicked = True
    else:
        has_clicked = False
    
    image("dirt3.jpg", 0, 0)
    
    # Draw the hoarded food in the colony.
    s = colony.food
    #colony hole
    #strokewidth(10)
    #stroke(1, .5, .4)
    #fill(0, 0, 0)
    #oval(245, 245, 20, 20)
    nostroke()
    
    # Draw each foodsource in green.
    # Watch it shrink as the ants eat away its size parameter!
    #fill(0.6,0.8,0)
    fill(0.6, 0.4, 0, 0.6)
    for f in colony.foodsources:
        #food source
        oval(f.x-f.size/2, f.y-f.size/2, f.size, f.size)
           
    for ant in colony:
        
        #stroke(0,0,0, 0.4)
        strokewidth(1)
        nofill()
        autoclosepath(False)
        
        # Draw the pheromone trail for each ant.
        # Ants leave a trail of scent from the foodsource,
        # enabling other ants to find the food as well!
        if len(ant.trail) > 0:
            beginpath(ant.trail[0].x, ant.trail[0].y)
            for p in ant.trail: lineto(p.x, p.y)
            endpath()
        
        nostroke()
        # ant color no food
        fill(0,0,0, 0.8)
        
        # Change ant color when carrying food.
        if ant.has_food:
            fill(0,0,0)
        
            
        # The main ant behaviour:
        # 1) follow an encountered trail,
        # 2) harvest nearby food source,
        # 3) bring food back to colony,
        # 4) wander aimlessly
        ant.forage()
        rect(ant.x, ant.y, 3, 3)