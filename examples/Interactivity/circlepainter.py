size(800, 800)
import time
colormode(RGB)

speed(60)

def setup():
    # ovallist is the list of ovals we created by moving the mouse.
    global ovallist
    stroke(0)
    strokewidth(1)
    ovallist = []

class Blob:
    def __init__(self, x, y, c, r):
        self.x, self.y = x, y
        self.color = c
        self.radius = r

    def draw(self):
        fill(self.color)
        stroke(0)
        strokewidth(1)
        oval(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)
        




def draw():
    global ovallist

    x = MOUSEX 
    y = MOUSEY
    if 0:
        if x > WIDTH or y > HEIGHT:
            return
    b = mousedown
    if b:
        d = random()
        r = random(10, 20)
        c = color(0,d,0,0.4)
        ovallist.append( Blob(x,y,c,r) )
    for blob in ovallist:
        blob.draw()

