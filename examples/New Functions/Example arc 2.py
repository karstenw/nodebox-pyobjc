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
    fill(1)
    text(s, x, y+20)
    fill(0)
    text(s, x+1, y+21)
    pop()


radius = 200
startangle = 270
endangle = 0

arc( 210, 210, radius, startangle, endangle)

line(210, 210, 210, 10)
line(210, 210, 410, 210)

arc( 210, 210, radius, startangle-180, endangle-180)


nofill()
stroke( 1,1,0 )
autoclosepath(close=False)
x, y = 210, 10
r = 200
r2 = r *  0.5555 # 
beginpath(x, y)
curveto(x+r2, y, x+r, y+r-r2, x+r, y+r)
endpath()



x, y = 210, 620
r = 200
r2 = r *  0.5555 # 

stroke( 0,1,1 )
rect(x-r, y-r, 2*r, 2*r)

nofill()
stroke(0)
strokewidth(2.5)
oval( x-r, y-r, 2*r, 2*r)


stroke( 1,1,0 )
strokewidth(1)
fill(0.5, 0.5, 0)

r = r-2
r2 = r *  0.5555 # 

autoclosepath(close=True)
beginpath(x, y-r)
curveto(x+r2, y-r, x+r, y-r2, x+r, y)
curveto(x+r,  y+r2, x+r2, y+r, x , y+r)
curveto(x-r2, y+r, x-r, y+r2, x-r, y)
curveto(x-r, y-r2, x-r2, y-r, x, y-r)
endpath()

