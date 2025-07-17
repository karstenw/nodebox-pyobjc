cornu = ximport("cornu")

size( 1600, 900 )
transform(CORNER)
translate(60, 400)
scale(0.1)

nofill()
stroke(0)
strokewidth(4.5)

names = fontnames()
f = choice( names )
font( f, 1.500 )
print( "Font:", f)

path = textpath("Nodebox", 0, 0)
points = []

delta = 0.05

for pt in path:
    if pt.cmd in (LINETO, CURVETO):
        points.append((pt.x, pt.y))
        if random() > 0.8:
            points.append((pt.x+random(-delta, delta), 
                           pt.y+random(-delta, delta)))
 
cornu.drawpath(points)
