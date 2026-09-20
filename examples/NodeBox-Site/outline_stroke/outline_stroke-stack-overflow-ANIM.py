# Source - https://stackoverflow.com/q/40689189

# Posted by user7173404, modified by community. See post 'Timeline' for change history

# Retrieved 2026-09-08, License - CC BY-SA 3.0

# heavily modified, adapted to strokelib & made runnable - kw 2026-09-08/10
# I am not sure if the visible animation was the authors intent but as always:
# I learned a lot


sl = ximport("strokelib")

from math import sin, cos, degrees, radians, pi
# from random import choice


animate = True

if animate:
    speed( 20 )

width = 8


FLAT    = sl.linecap_flat
ROUNDED = sl.linecap_rounded
 
UNIFORM  = sl.transform_uniform
EXPAND   = sl.transform_expand
CONTRACT = sl.transform_contract
SMOOTH   = sl.transform_smooth


# colors
alpha = 255

colormode( RGB, 255 )
LEMONCHIFFON = color(200,205,108,alpha)
LIGHTBLUE = color(52,86, 163,alpha)
STEELBLUE = color(70, 130,180,alpha)
ROYALBLUE = color(65,105,225,alpha)
colormode( RGB )

colors = ( LEMONCHIFFON, LIGHTBLUE, STEELBLUE, ROYALBLUE )


offset = 5
angleincrement = 9


class Stroke:
    
    def __init__(self, center, ang, col):
        self.cx, self.cy = center
        self.angle = ang
        self.length = random( 50, 60 )
        self.color = col 
        self.derivatives()
    
    def derivatives(self):
        self.halflength = self.length / 2
        self.top = coordinates( self.cx, self.cy, self.halflength, self.angle )
        self.bottom = coordinates( self.cx, self.cy, self.halflength, self.angle+180 )
    
    def draw(self):
        # move
        self.angle += angleincrement
        if self.color == STEELBLUE:
            self.cx -= offset
            self.cy -= offset
        else:
            self.cx += offset
            self.cy += offset
        self.derivatives()
        
        strokewidth( width )
        
        if 1:
            h = self.halflength * sin( radians(self.angle) )
            w = self.halflength * cos( radians(self.angle) )
            x0 = self.cx - w
            y0 = self.cy + h
            x1 = self.cx + w
            y1 = self.cy - h
            path = BezierPath()
            path.moveto(x0, y0)
            path.lineto(x1,y1)
            path = sl.outline_stroke(path,
                                     linecap=ROUNDED,
                                     transform=SMOOTH, #CONTRACT,
                                     precision=2,
                                     debug=False,
                                     )
        
        else:
            #reset()
            rotate( self.angle )
            align(CENTER)
            path = BezierPath()
            x0, y0 = self.top
            x1, y1 = self.bottom
            path.moveto( x0, y0 )
            path.lineto( x1,y1 )
            path = sl.outline_stroke(path,
                                     linecap=ROUNDED,
                                     transform=SMOOTH, #CONTRACT,
                                     precision=2,
                                     debug=False,
                                     )
        
        fill(self.color)
        strokewidth(4)
        drawpath(path)
        strokewidth(0)

    def move(self):
        self.angle += pi/20
        if self.color == STEELBLUE:
            self.cx -= offset
            self.cy -= offset
        else:
            self.cx += offset
            self.cy += offset


# total = 800
total = 100

w, h = 800,600

inset = 10

size( w, h )

allstrokes = []

def setup():
    for i in range(total):
        cx = random( inset, w-inset )
        cy = random( inset, h-inset )
        
        thiscolor = choice( colors )
        
        ang = choice( [pi/15, pi/20] )
        ang = choice( (12, 9) )
        ang = random( 7, 15 )
        allstrokes.append( Stroke( (cx, cy), ang, thiscolor ) )



def draw():
    for strk in allstrokes:
        strk.draw()


if not animate:
    draw()

