# markmeyer-parametric6b

from math import sin, cos

size(550, 550)

colormode(HSB)

background(0.2, 0.02, 0.2)

fill(0.6, 0.1, 0.2, 0.005)

stroke(0.2, 0.1, 0.8, 0.7)
strokewidth( 0.25 )


def circle_equation(r, dt):
    center_x = 0.0
    center_y = 0.0
    t = 0.0
    while True:
        x = center_x + sin(t) * r
        y = center_y + cos(t) * r
        yield x, y
        t += dt
 
eq1 = circle_equation(250, 4 )
eq2 = circle_equation(400, -4)
x1, y1 = next(eq1)
x2, y2 = next(eq2)
 
translate(WIDTH/2, HEIGHT/2)
autoclosepath(False)
for i in range( 360 ):
    beginpath(-60, 0)
    curveto(x1, y1, x2, y2, 60, 0)

    x1, y1 = next( eq1 )
    x2, y2 = next( eq2 )
    curveto(x2, y2, x1, y1, 0, -20)

    x1, y1 = next( eq1 )
    x2, y2 = next( eq2 )
    curveto(x1, y1, x2, y2, -60, 0)

    endpath()

