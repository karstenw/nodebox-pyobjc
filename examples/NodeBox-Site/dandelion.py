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
 
def cultivate(path, points=100, length=100, d=70):
    """ Grows hairs jutting outwards from the path.
    """
    beginpath(0, 0)
    for pt in path.points(points):
        # At each point on the path we draw a random curve,
        # jutting outwards perpendicular to the point's angle.
        a = geo.angle(pt.x, pt.y, pt.ctrl1.x, pt.ctrl1.y)
        dx, dy = geo.coordinates(pt.x, pt.y, length, a+90)
        moveto(pt.x, pt.y)
        curveto(
            pt.x + random(-d, d), 
            pt.y + random(-d, d), 
            dx + random(-d, d), 
            dy + random(-d, d), 
            dx, 
            dy
        )
    return endpath(draw=False)
 
#############################################################################
 
def dandelion(clr, x, y, r=100, points=100, d=70):
    
    """ Draws a fluffy ball in the given color.
    
    Parameters x and y determines the position of the ball, r its radius.
    Layers of ovals that diminish in size are constructed.
    The number of points controls how many curves are drawn of each oval.
    Decreasing d yields more straight curves.
    
    """
 
    nofill()
    stroke(0)
    strokewidth(0.15)
    autoclosepath(False)
 
    # Create n ovals diminishing in radius.
    # We'll grow hairs on each of the ovals.
    n = int(r * 1.3)
    
    # The gradient also has n steps, from dark to light.
    clr = colors.color(clr)
    g = colors.gradient(
        clr.darken(1.0),
        clr,
        clr.lighten(1.0).desaturate(0.4),
        steps=n
    )
 
    for i in range(n):
        # Use the current step to color the hairs on this oval.
        stroke(g[i])
        # Combined with shadows, this gives a realistic sense of depth.
        # Shadows are darker on the outside.
        a = 0.75 - 0.25 * float(i)/n
        colors.shadow(alpha=a, dx=0, dy=30, blur=10)
        # Calculate individual points on each oval.
        # Smaller ovals have fewer curves, and curves are shorter.
        path = oval(x-r+i*0.5, y-r+i*0.5, r*2-i, r*2-i, draw=False)
        drawpath(
            cultivate(
                path, 
                points=int(points - i*0.2), 
                length=r-i + random(n-i)/3, 
                d=d))
        
#############################################################################
 
# Use the colors library to render shadows and gradients.
colors = ximport("colors")
clr = colors.color(0.9, 0.3, 0.5)
 
bg = color(0.55, 0.55, 0.50)
size(700, 700)
background(bg)
 
bg = clr.complement.desaturate(0.6)
colors.gradientfill(
    rect(0, 0, WIDTH, HEIGHT, draw=False),
    bg.darken(0.25),
    bg.lighten(0.25),
    spread=0.75
)
 
#############################################################################
 
dandelion(clr, 350, 350, r=125, d=100)