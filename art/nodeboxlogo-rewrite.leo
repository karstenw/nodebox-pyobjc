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
<v t="karstenw.20260702150922.2"><vh>bar</vh></v>
<v t="karstenw.20260702150922.3"><vh>cube</vh></v>
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
</t>
<t tx="karstenw.20260702150922.2">    colormode(HSB)
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
    
</t>
<t tx="karstenw.20260702150922.3">    x += depth
    y += depth


</t>
<t tx="karstenw.20260702150922.4">def setup():
    seed( i )

</t>
<t tx="karstenw.20260702150922.5">def draw():
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
</tnodes>
</leo_file>
