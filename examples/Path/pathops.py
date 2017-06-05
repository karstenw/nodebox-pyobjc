size(600, 1000)

# pathmatics functions
nofill()
stroke(0)

def label(s,x,y):
    """put a black label preserving fill color."""
    push()
    c = fill()
    fill(0)
    text(s,x,y)
    fill(c)
    pop()


def circlepath(x, y, r):
    """Make a circle with curveto."""
    
    r2 = r *  0.5555 # 

    autoclosepath(close=True)
    beginpath(x, y-r)
    curveto(x+r2, y-r, x+r, y-r2, x+r, y)
    curveto(x+r,  y+r2, x+r2, y+r, x , y+r)
    curveto(x-r2, y+r, x-r, y+r2, x-r, y)
    curveto(x-r, y-r2, x-r2, y-r, x, y-r)
    return endpath(draw=False)


# normal
c1 = circlepath( 200, 100, 100)
c2 = circlepath( 300, 100, 100)

drawpath(c1)
drawpath(c2)
label("Normal", 420, 100)
print "Path c1 intersects path c2:", c1.intersects(c2)

# flatness should always be 0.5
var("flatness", NUMBER, 0.6, 0.1, 5.0)
print "flatness:", flatness

# union
c1 = circlepath( 200, 300, 100)
c2 = circlepath( 300, 300, 100)

drawpath(c1.union(c2, flatness=flatness))
label("Union", 420, 300)


# difference
c1 = circlepath( 200, 500, 100)
c2 = circlepath( 300, 500, 100)

drawpath(c1.difference(c2, flatness=flatness))
label("Difference", 420, 500)


# intersect
c1 = circlepath( 200, 700, 100)
c2 = circlepath( 300, 700, 100)

drawpath(c1.intersect(c2, flatness=flatness))
label("Intersection", 420, 700)

# xor
fill(0)
c1 = circlepath( 200, 900, 100)
c2 = circlepath( 300, 900, 100)

drawpath(c1.xor(c2, flatness=flatness))
label("XOR", 420, 900)

