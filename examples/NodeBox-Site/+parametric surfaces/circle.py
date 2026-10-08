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
 
eq = circle_equation(240, 4.5)
x, y = next( eq )
 
autoclosepath(False)
translate(WIDTH/2, HEIGHT/2)
beginpath(x, y)
for i in range(74):
    x, y = next( eq )
    lineto(x, y)
endpath()
