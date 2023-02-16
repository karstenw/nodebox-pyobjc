#############################################################################
 
# Copyright (c) 2008 Tom De Smedt.
 
__author__    = "Tom De Smedt"
__version__   = "1.9.4"
__copyright__ = "Copyright (c) 2008 Tom De Smedt"
__license__   = "GPL"
 
#############################################################################
 
# The geo library bundles the commands discussed in:
# http://nodebox.net/code/index.php/Math
from nodebox import geo
 
def strand(n, x0, y0, x1, y1, x2, y2, x3, y3, d1=30, d2=30, draw=True):
    """ Like a curveto() command, but draws a bundle of n curves.
    """
    beginpath(x0, y0)
    for j in range(n):
        moveto(x0, y0)
        curveto(
            x1 + random(-d1, d1), 
            y1 + random(-d1, d1), 
            x2 + random(-d2, d2), 
            y2 + random(-d2, d2),
            x3,
            y3
        )
    return endpath(draw)
 
#############################################################################
 
def fountain(clr,
             n=50,
             d=400,
             angle=5.0,
             iterations=50):
 
    """ Draws a pattern of elegant curves in the given color.
    
    The pattern is based on many strands of curves moving together.
    Increasing n produces more curves per strand.
    Decreasing d makes smaller strands.
    The angle controls how copies of a strand are rotated.
    A strand progresses fluidly into another strand,
    and more iterations yield more consecutive strands.
    
    """
 
    nofill()
    stroke(clr)
    strokewidth(0.15)
    autoclosepath(False)
    transform(CORNER)
 
    # Start from a random position, with a random curve handle.
    x0, y0 = random(WIDTH), random(HEIGHT)
    x1, y1 = x0+random(-d,d), y0+random(-d,d)
    x3, y3 = x0, y0
 
    for i in range(iterations):
        # Curve to a new position,
        # located no further away than d.
        x3, y3 = x3+random(-d,d), y3+random(-d,d)
        x2, y2 = x3+random(-d,d), y3+random(-d,d)
        path = strand(
            n, x0, y0, x1, y1, x2, y2, x3, y3, 
            d1=random(100), 
            d2=random(100),
            draw=False
        )
 
        # Draw rotating versions of the strand.
        # The starting point is marked with an oval.
        for j in range(8):
            rotate(angle)
            if i == 0:
                fill(1,0.1)
                oval(x0-10, y0-10, 20, 20)
                nofill()
            drawpath(path.copy())
        reset()
        
        # Reflect the next strand's handle from the previous,
        # so they fit together fluidly.
        x0, y0 = x3, y3
        x1, y1 = geo.reflect(x3, y3, x2, y2, a=180)
 
#############################################################################
 
size(700, 700)
clr = color(0.7, 0.8, 0.9)
background(clr)
 
try:
    # Try to render shadows and gradients using the colors library.
    colors = ximport("colors")
    colors.shadow(alpha=0.8, blur=5)
    bg = colors.color(clr).analog(20, d=0.1).darker(0.3)
    colors.gradientfill(
        rect(0, 0, WIDTH, HEIGHT, draw=False),
        bg.darken(0.2),
        bg.lighten(0.3),
        spread=0.75)
except:
    pass
 
#############################################################################
 
fountain(clr)