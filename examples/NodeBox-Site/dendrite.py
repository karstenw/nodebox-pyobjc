size(400, 400)

speed(100)

from random import seed
from math import sin
 
lines = []
down = False
 
def append_line():
    global down
    if mousedown:
        if len(lines) > 0 and lines[-1] == (MOUSEX, MOUSEY):
            return
        if down:
            lines.append((LINETO, MOUSEX, MOUSEY, FRAME))
        else:
            down = True
            lines.append((MOVETO, MOUSEX, MOUSEY, FRAME))
    else:
        down = False
        
 
def draw_line():
    if len(lines) == 0: return
    nofill()
    stroke(1,1,1,0.5)
    strokewidth(0.25)
    p = BezierPath()
    for cmd, x, y,t in lines:
        if cmd == MOVETO:
            p.moveto(x, y)
        else:
            p.lineto(x, y)
    p.inheritFromContext()
    p.draw()    
 
def draw_ch_line():
    for i in range(5):
        seed(i)
        if len(lines) == 0: return
        nofill()
        stroke(1,1,1,0.5)
        strokewidth(0.2)
        p = BezierPath()
        for cmd, x, y, t in lines:
            d = sin((FRAME - t) / 10.0) * 10.0
            x += random(-d, d) 
            y += random(-d, d)
            if cmd == MOVETO:
                p.moveto(x, y)
            else:
                p.lineto(x, y)
        p.inheritFromContext()
        p.draw()    
 
def setup():
    pass
 
def draw():
    background(0.25,0.0,0.1)
    append_line()
    draw_ch_line()
