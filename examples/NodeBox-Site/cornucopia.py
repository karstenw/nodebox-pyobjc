cornu = ximport("cornu")
 
transform(CORNER)
translate(20, 600)
scale(0.2)

nofill()
stroke(0)
strokewidth(3)


font("Zapfino", 1.0)
 
path = textpath("2023", 0, 0)
points = []

for pt in path:
    if pt.cmd == LINETO or pt.cmd == CURVETO:
        points.append((pt.x, pt.y))
        if random() > 0.8:
            points.append((pt.x+random(-0.05,0.05), 
                           pt.y+random(-0.05,0.05)))
 
cornu.drawpath(points)
