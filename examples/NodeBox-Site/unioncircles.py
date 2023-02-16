H = 800.0
W = 800.0

size(W,H)

d = random( WIDTH / 6 )

c = oval(random(WIDTH), random(HEIGHT), d, d, draw=False)
 
for i in range(250):
    d = random(WIDTH/9)
    o = oval(random(WIDTH), random(HEIGHT), d, d, draw=False)
    c = c.union(o)
nofill()
stroke(0)
drawpath(c)
