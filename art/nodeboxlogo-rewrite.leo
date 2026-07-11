<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="karstenw.20260702150854.2" a="E"><vh>@clean nodeboxlogo-rewrite.py</vh>
<v t="karstenw.20260702150922.1"><vh>Declarations</vh></v>
<v t="karstenw.20260702150922.3" a="E"><vh>cube</vh>
<v t="karstenw.20260710155254.1"><vh>&lt;&lt; helpers &gt;&gt;</vh></v>
</v>
<v t="karstenw.20260702150922.4"><vh>setup</vh></v>
<v t="karstenw.20260702150922.5"><vh>draw</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20260702150854.2">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20260702150922.1">from random import seed
from itertools import cycle

# export as tiff and use with Icon Composer"

i = 0
cubesize = 225.5
n = 3
offset = 2

strokew = 4.5

depthscale = 0.5
cubedepth = cubesize * depthscale

cell = n * cubesize + n * cubedepth + 2*offset + 3.5

size( cell, cell )
#size(1280, 1280 )
# print("WIDTH:", WIDTH)

background( None )

coins = cycle( [random() for i in range(10000)] )
    
joinstyle( ROUND )
capstyle( ROUND )
autoclosepath( True )

animate = 0

if animate:
    speed( 8 )

</t>
<t tx="karstenw.20260702150922.3">def cube(x, y, width, depth):
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
    
    &lt;&lt; helpers &gt;&gt;
    
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
    

</t>
<t tx="karstenw.20260702150922.4">def setup():
    seed( i )


</t>
<t tx="karstenw.20260702150922.5">def draw():
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
                
                if random() &gt; 0.5:
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

</t>
<t tx="karstenw.20260710155254.1">def coin():
    if next(coins) &gt; 0.5:
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

</t>
</tnodes>
</leo_file>
