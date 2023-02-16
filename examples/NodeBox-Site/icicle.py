size(600, 600)
 
def point(x=WIDTH, y=HEIGHT):
 
  return (random(x),random(y))
 
def abstract():
 
  x, y = point()
  beginpath(x,y)
  for i in range(1,random(20)):
    x, y = point(0,HEIGHT/i)
    lineto(x,y)
  endpath() 
 
  if random(100) > 80:
    w = random(20,80)
    oval(x-w*0.5,y-w*0.5,w,w)
 
fill(0.95,1,1)
rect(0,0,WIDTH,HEIGHT)
 
stroke(0,0.5,random(0.5,0.75),0.3)
strokewidth(0.25)
for i in range(40):
  fill(0,0.5,random(0.5,0.75),0.1 * 0.04*i)
  abstract()
 
nofill()
stroke(0.2,0.2,0.2)
strokewidth(0.5)
rect(0,0,WIDTH,HEIGHT)
 
fill(1,1,1,0.6)
rotate(-90)
font("Futura", 20)
text("ICICLE", -10, 80)