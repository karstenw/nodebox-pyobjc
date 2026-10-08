# markmeyer-parametric4b

size(550, 550)
colormode(HSB)
background(0.2, 0.02, 0.2)
nofill()
stroke(0.2, 0.1, 0.8, 0.7)
strokewidth(0.25)

from math import sin, cos

def circle_equation(r, dt):
    center_x = 0.0
    center_y = 0.0
    t = 0.0
    while True:
        x = center_x + cos(t) * r
        y = center_y + sin(t) * r
        yield x, y
        t += dt
 
eq1 = circle_equation(100, 1.00)
eq2 = circle_equation(150, 1.75)
x1, y1 = next( eq1 )
x2, y2 = next( eq1 )
 
autoclosepath(False)
translate(WIDTH/2, HEIGHT/2)
beginpath(x1+x2, y1+y2)
for i in range(360*2):
    lineto(x1+x2, y1+y2)
    x1, y1 = next( eq1 )
    x2, y2 = next( eq2 )
endpath()
