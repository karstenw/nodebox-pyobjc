from random import seed
from itertools import cycle

# export as tiff and use with Icon Composer"

i = 0
cubesize = 225.8888
n = 3
offset = 2

strokew = 4.5

depthscale = 0.5
cubedepth = cubesize * depthscale

cell = n * cubesize + n * cubedepth + 2*offset + 3.5

size( cell, cell )
#size(1280, 1280 )
print("WIDTH:", WIDTH)

background( None )

coins = cycle( [random() for i in range(10000)] )
    
joinstyle( ROUND )
capstyle( ROUND )
autoclosepath( True )

animate = 0

if animate:
    speed( 8 )

def cube(x, y, width, depth):
    """
    cube origin is back top left corner. back plane is numbered 0-3,
    front plane is numbered 0-3
    
     b0--b1
     /|  /|
   f0--f1 | 
    |b3-|b2
    |/  |/
   f3--f2
    
    """
    # cubepoints
    # front point 0
    f0 = x-depth, y+depth
    f1 = x-depth+width, y+depth
    f2 = x-depth+width, y+depth+width
    f3 = x-depth, y+depth+width
    
    # back point 0
    b0 = x,y
    b1 = x+width,y
    b2 = x+width,y+width
    b3 = x,y+width
    
    def coin():
        if next(coins) > 0.5:
            return True
        return False

    def cubeline( start, end ):
        # draw a line between two cube corners
        x1,y1 = start
        x2,y2 = end
        line( x1,y1, x2,y2 )


    def cuberect( p1,p2,p3,p4):
        # draw a rect between 4 cube corners
        beginpath( *p1 )
        lineto( *p2 )
        lineto( *p3 )
        lineto( *p4 )
        endpath()

    
    colormode(HSB)
    f = fill()
    s = stroke()
    if f != None and f.brightness != 1:
        s = color(f.hue, f.saturation+0.2, f.brightness-0.4)
    
    nostroke()
    # stroke(s)
    
    if 0:
        #back plane (b0,b1,b2,b3)
        if f != None:
            fill(f)
        rect(x, y, width, width)
    
    if 0:
        #bottom  
        cuberect( b3, b2, f2, f3 )
    
    if 1: #coin():
        #left
        cuberect( b0, b3, f3, f0 )
    
    # delta color for side planes
    if f != None:
        fill(f.hue, f.saturation-0, f.brightness-0.15)
    
    if 1: #coin():
        #top
        cuberect( b0, b1, f1, f0 )
    
    # delta color for side planes
    if f != None:
        fill(f.hue, f.saturation-0, f.brightness-0.15)
    
    if 1: #coin():
        #right
        cuberect( b1, b2, f2, f1 )
    
    # restore and redo some strokes
    if s != None:
        stroke(s)
    
    # nostroke()
    if 1:
        # top back
        cubeline( b0, b1 )
        
        # upper left diagonal
        cubeline( b0, f0 )
        
        # back right down
        cubeline( b1, b2 )
        
        # lower right diagonal
        cubeline( b2, f2 )
        
        # lower left diagonal
        cubeline( b3, f3 )
        
        # upper right diagonal
        cubeline( b1, f1 )
    
    if 1: #coin():
        #front
        if f != None:
            fill(f)
        rect(x-depth, y+depth, width, width)
    

def setup():
    seed( i )


def draw():
    global i 
    i = i + 1
    
    # different seed values for certain results - uncomment accordingly
    # for animation seed( i ) should be active
    kwfork = 15
    extended = 29
    classic = 55
    
    #seed( kwfork )
    #seed( extended )
    seed( classic )
    # seed(11)
    
    if animate:
        seed(i)
        print("seed( %i )" % (i,))
    
    strokewidth( strokew )
    
    colormode(RGB)
    c = color( 0.05, 0.65, 0.85)
    c.brightness += 0.2

    
    # from left to right
    for x in range( n ):
        
        # from bottom to top
        for y in range( n ):
            
            # baseline y farthest plane
            bottom = cubesize * n + 1
            
            # from back to front
            for z in range( n ):
                stroke(0.1)
            
                colormode(RGB)
                
                dr = (1-c.r)/(n-1) * (x*0.85+y*0.15+z*0.05) * 1.1
                dg = (1-c.g)/(n-1) * (x*0.85+y*0.15+z*0.05) * 1.2
                db = (1-c.b)/(n-1) * (x*0.85+y*0.15+z*0.05) * 1.1
                fill(1.2-dr, 1.1-dg, 1.2-db)
                
                if random() > 0.5:
                    nostroke()
                    nofill()
                
                dx = cubesize * x - cubedepth * z
                dy = bottom - cubesize * y + cubedepth * z
            
                transform(CORNER)
                translate( offset + cubesize + cubedepth, -cubesize)
                #scale( 1.01 )
                cube(dx, dy, cubesize, cubedepth)
                # print(dx, dy)
                reset()

if not animate:
    draw()

