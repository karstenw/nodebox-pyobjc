size(800, 600)
background(0.23, 0.21, 0.15)

import pprint
pp=pprint.pprint

if 1:
    # use a random font
    fonts = fontnames()
    f = choice(fonts)
else:
    f = "Georgia-Bold"
    #f = "TeXGyreTermes-Regular"
    f = "Coda-Heavy"

font( f, 216 )
print(f)

string = "hairy"

def maketextpath( s, x, y ):
    path = textpath( s, x, y)
    b = path.bounds
    x,y,w,h = (float(b.origin.x), float(b.origin.y),
               float(b.size.width), float(b.size.height) )
    cx = x + (w / 2)
    cy = y + (h / 2)
    return path, x,y,w,h,cx,cy

# center rect
centerX, centerY = WIDTH/2, HEIGHT/2

# initial rect
ix,iy = 40, 250
path1, x,y,w,h,px,py = maketextpath( string, ix, iy )
rectOrig = (x,y,w,h)

dx = centerX - px
dy = centerY - py

path, x,y,w,h,px,py = maketextpath( string, ix+dx, iy+dy)
rectMoved = (x,y,w,h)

stroke(1)
nofill()
if 0:
    rect( *rectOrig )
    rect( *rectMoved )

for contour in path.contours:    
    prev = None
    n = int(contour.length / 1)
    for pt in contour.points( n ):     
    
        nofill()
        stroke(1, 0.75)
        strokewidth(random(0.25, 0.5))
        
        if prev != None:
            autoclosepath(False)
            beginpath(prev.x, prev.y)            
            curveto(
                pt.ctrl1.x - random(30), 
                pt.ctrl1.y,
                pt.ctrl2.x, 
                pt.ctrl2.y + random(30),
                pt.x, 
                pt.y
            )
            curveto(
                pt.ctrl1.x + random(10), 
                pt.ctrl1.y,
                pt.ctrl2.x, 
                pt.ctrl2.y - random(10),
                pt.x + random(-20, 20),
                pt.y + random(-10, 10)
            )  
            endpath()
            
        prev = pt
