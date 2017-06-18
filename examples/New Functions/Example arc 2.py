import math

background(0.6)
nofill()
stroke(0)

def mark(x,y,size=10, col=color(255,0,0)):
    push()
    d = size / 2.0
    stroke(col)
    line(x-d-0.5,y-d-0.5,x+d+0.5,y+d+0.5)
    line(x-d-0.5,y+d+0.5,x+d+0.5,y-d-0.5)
    pop()

def label(s,x,y):
    push()
    # save fill value
    f = fill()
    fill(1)
    text(s, x, y+20)
    fill(0)
    text(s, x+1, y+21)
    # restore fill value
    fill(f)
    pop()


radius = 200
startangle = 270
endangle = 0
strokewidth(3)
stroke( 0,0,1 )
arc( 210, 210, radius, startangle, endangle)
label("blue arc( 210, 210, radius, 270, 0)",420,70)
mark(210,210)

stroke( 0 )
strokewidth(1)
line(210, 210, 210, 10)
line(210, 210, 410, 210)

arc( 210, 210, radius, startangle-180, endangle-180)
label("arc( 210, 210, 200, 90, -180)",100,290)


nofill()
stroke( 1,0,0 )
autoclosepath(close=False)
x, y = 210, 10
r = 200
r2 = r *  0.556
beginpath(x, y)
curveto(x+r2, y, x+r, y+r-r2, x+r, y+r)
endpath()
label("red curveto( 321.2, 10, 410, 98.8, 410, 210 )",420,90)
mark(x,y)
mark(321.2, 10)
mark(410, 98.8)
mark(410, 210)


x, y = 210, 620
r = 200

stroke( 0,1,1 )
rect(x-r, y-r, 2*r, 2*r)

nofill()
stroke(0)
strokewidth(2.5)
oval( x-r, y-r, 2*r, 2*r)
label("black oval( 10, 420, 400, 400, )", 420, 420)


stroke( 1,1,0 )
strokewidth(1)
fill(0.5, 0.5, 0)

r = r-2
r2 = r *  0.556

autoclosepath(close=True)
beginpath(x, y-r)
curveto(x+r2, y-r, x+r, y-r2, x+r, y)
curveto(x+r,  y+r2, x+r2, y+r, x , y+r)
curveto(x-r2, y+r, x-r, y+r2, x-r, y)
curveto(x-r, y-r2, x-r2, y-r, x, y-r)
endpath()
label("yellow:", 420, 470)
label("beginpath( 210, 422 )", 420, 500)
label("curveto( 320.088, 422, 408, 509.912, 408, 620 )", 420, 530)
label("curveto( 408, 730.088, 320.088, 818, 210, 818 )", 420, 560)
label("curveto( 99.912, 818, 12, 730.088, 12, 620 )", 420, 590)
label("curveto( 12, 509.912, 99.912, 422, 210, 422 )", 420, 620)
label("endpath()", 420, 650)

