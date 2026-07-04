from random import seed

# export as tiff and use with Icon Composer"

i = 0
cubesize = 111.2223
n = 3
offset = 3

strokew = 2.8284

depthscale = 0.5
cubedepth = cubesize * depthscale

cell = n * cubesize + n * cubedepth + 2*offset + 3.5

size( cell, cell )
#size(1280, 1280 )
print("WIDTH:", WIDTH)

background(1)

animate = 0

if animate:
    speed( 2 )

def cube(x, y, width, depth):
    colormode(HSB)
    f = fill()
    s = stroke()
    if f != None and f.brightness != 1:
        s = color(f.hue, f.saturation+0.2, f.brightness-0.4)
    
    nostroke()
    # stroke(s)
    
    if 0:
        #back
        if f != None:
            fill(f)
        rect(x, y, width, width)
    
    if 0:
        #bottom
        beginpath(x, y+width)
        lineto(x-depth, y+width+depth)
        lineto(x-depth+width, y+width+depth)
        lineto(x+width, y+width)
        endpath()
    
    if 0:
        #left
        beginpath(x, y)
        lineto(x-depth, y+depth)
        lineto(x-depth, y+width+depth)
        lineto(x, y+width)
        endpath()
    
    if 1:
        #top
        # delta color for side planes
        if f != None:
            fill(f.hue, f.saturation-0, f.brightness-0.15)
        beginpath(x, y)
        lineto(x+width, y)
        lineto(x+width-depth, y+depth)
        lineto(x-depth, y+depth)
        endpath()
    
    if 1:
        #right
        # delta color for side planes
        if f != None:
            fill(f.hue, f.saturation-0, f.brightness-0.15)
        beginpath(x+width, y)
        lineto(x+width-depth, y+depth)
        lineto(x+width-depth, y+width+depth)
        lineto(x+width, y+width)
        endpath()
    
    # restore and redo some strokes
    if s != None:
        stroke(s)
    # nostroke()
    if 1:
        # top front
        line(x, y, x+width, y)
        
        # upper left diagonal
        line(x, y, x-depth, y+depth)
        
        # back right down
        line(x+width, y, x+width, y+width)
        
        # lower right diagonal
        line(x+width, y+width, x+width-depth, y+width+depth)
        
        # lower right diagonal
        line(x+width, y+width, x+width-depth, y+width+depth)
        
        
        line(x, y+width, x-depth, y+width+depth)
        line(x+width, y, x+width-depth, y+depth)
    
    if 1:
        #front
        if f != None:
            fill(f)
        rect(x-depth, y+depth, width, width)
    
    x += depth
    y += depth


def setup():
    seed( i )

def draw():
    global i 
    i = i + 1
    # i = 15
    
    kwfork = 15
    extended = 29
    classic = 55
    seed(i)
    seed( kwfork )
    # seed( extended )
    # seed( classic )
    # seed(11)
    
    #print("seed( %i )" % (i,))

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

