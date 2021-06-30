
from __future__ import print_function

size(1350, 550)
# BitBop -- a fun demonstration of path.contains.
#
# The textpath command returns a BezierPath of the text that can
# be manipulated or, as demonstrated here, queried using path.contains.
# A grid is generated and everywhere a point in the path is encountered,
# a random square is drawn.

background(0.8, 0.7, 0)
fill(0.1, 0.1, 0.2)

# Set the font and create the text path.
fonts = fontnames()
fsize = 300
f = choice( fonts )
print( f )
font(f, fsize)
align(LEFT)
tp = textpath("NodeBox", 0, fsize+80, width=WIDTH)


# Here are the variables that influence the composition:
resx = 400 # The horizontal resolution
resy = 200 # The vertical resolution
rx = 6.0 # The horizontal randomness each point has
ry = 6.0 # The vertical randomness each point has
dotsize = 4.0 # The maximum size of one dot. 
dx = WIDTH / float(resx) # The width each dot covers
dy = HEIGHT / float(resy) # The height each dot covers

# We create a grid of the specified resolution.
# Each x,y coordinate is a measuring point where
# we check if it falls within the path.
for x, y in grid(resx, resy):
    sz = random(dotsize)
    # Create the point that will be checked
    px = x*dx-sz
    py = y*dy-sz
    # Only do something if the point falls within the path bounds.
    # You could add an "else" statement, that draws something in the
    # empty positions.
    if tp.contains(px, py):
        # Change the color for each point -- try it out!
        # fill(0, 0, random(), random())
        oval(px+random(-rx, rx), 
             py+random(-ry, ry), 
             sz, sz)

