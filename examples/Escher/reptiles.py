# background(0.8)
background(None)

import math

debug = 0

r30 = math.radians( 30)
c30 = math.cos( r30 )

# the reptile consists of 3 different segments; each used twice
seg1 = (
    ( 0.0,  0.0),
    ( 2.2,  2.2),
    ( 4.0,  2.2),
    ( 6.3, -0.5),
    ( 5.0, -3.0),
    ( 5.8, -3.8),
    ( 7.5, -3.7),
    ( 7.8, -3.0),
    ( 7.0, -2.0),
    ( 8.0,  0.0))

seg2 = (
    ( 0.0,  0.0),
    (-1.0,  2.0),
    ( 1.0,  2.5),
    ( 3.8,  1.3),
    ( 4.5,  0.0),
    ( 4.8, -3.0),
    ( 3.0, -4.8),
    ( 6.8, -3.2),
    ( 8.0, -0.8),
    ( 8.0,  0.0))

seg3 = (
    ( 0.0,  0.0),
    ( 1.0,  2.5),
    ( 0.7,  4.8),
    ( 2.8,  4.0),
    ( 2.8,  2.9),
    ( 2.1,  0.25),
    ( 4.0, -0.5),
    ( 5.3, -1.75),
    ( 8.0,  0.0))


def getsegment( segment, start, end, reverse):
    # get a list of coordinates for segment adapted between start and end

    # All the segments for one reptile need to be drawn in one go, so
    # instead of rotating them, they are drawn strictly clockwise.
    
    # to achieve that, half of the segments need to be reversed.

    if 0: #debug:
        segment = ( (0,0), (4,1), (4,-1), (8,0))
    seg = segment[:]

    if reverse:
        seg = []
        for i in segment:
            x,y = i
            # get this ugly constant out
            seg.append( (8.0-x, -y) )
        seg.reverse()

    a = angle( start[0], start[1], end[0], end[1] )
    s = distance( start[0], start[1], end[0], end[1] )
    r = math.radians( a )
    cosr = math.cos(r)
    sinr = math.sin(r)

    #print "scale:", s
    #print "angle:", a
    result = []

    for p in seg:
        px, py = p
        if 1: # reverse:
            # segments were constructed in an y-switched coordinate system; correct it
            py = py * -1.0
            #px = px * -1.0

        # scale
        px *= s/8
        py *= s/8
        
        # rotate
        px2 = px * cosr - py * sinr
        py2 = px * sinr + py * cosr

        # translate
        px2 += start[0]
        py2 += start[1]

        result.append( (px2, py2) )

    return result


def verticalhexagon(x, y, radius):
    # flat top/bottom
    height = radius * c30
    halfradius = radius / 2.0

    return [
        ( x + radius    ,  y),
        ( x + halfradius  , y + height),
        ( x - halfradius  , y + height),
        ( x - radius      , y),
        ( x - halfradius  , y - height),
        ( x + halfradius  , y - height)]

def veroffsets(x, y, radius, shift):
    shifts = {
         0: (2,4,2,4,2,4),
         1: (5,3,5,3,5,3),
         2: (4,0,4,0,4,0),
         3: (1,5,1,5,1,5),
         4: (0,2,0,2,0,2),
         5: (3,1,3,1,3,1)}
    shifts = {
         0: (2,4,2,4,2,4),
         1: (3,5,3,5,3,5),
         2: (4,0,4,0,4,0),
         3: (5,1,5,1,5,1),
         4: (0,2,0,2,0,2),
         5: (1,3,1,3,1,3)}
             
    height = radius * c30
    halfradius = radius / 2.0
    side = 1.5 * radius
    up = 2 * height

    s = shifts[shift]
    return [
        ( x + side , y - height, s[0]),
        ( x + side , y + height, s[1]),
        ( x        , y + up,     s[2]),
        ( x - side , y + height, s[3]),
        ( x - side , y - height, s[4]),
        ( x        , y - up,     s[5])]

def horizontalhexagon(x, y, radius):
    # flat left/right
    height = radius * c30
    halfradius = radius / 2.0
    return [
        ( x + 0     , y - radius),
        ( x + height, y - halfradius),
        ( x + height, y + halfradius),
        ( x + 0     , y + radius),
        (x - height , y + halfradius),
        (x - height , y - halfradius)]

def horoffsets(x, y, radius, shift):
    shifts = {
         0: (4,2,4,2,4,2),
         1: (3,5,3,5,3,5),
         2: (0,4,0,4,0,4),
         3: (5,1,5,1,5,1),
         4: (2,0,2,0,2,0),
         5: (1,3,1,3,1,3)}
             
    height = radius * c30
    halfradius = radius / 2.0
    
    side = 2*height
    up = 1.5*radius
    corner = height
    s = shifts[shift]
    return [
        ( x + height , y - up,  s[0]),
        ( x + side   , y     ,  s[1]),
        ( x + height , y + up,  s[2]),

        ( x - height , y + up,  s[3]),
        ( x - side   , y     ,  s[4]),
        ( x - height , y - up,  s[5])]


def reptile(x, y, radius, rot, shift, vert):

    if vert:
        h = verticalhexagon( x, y, radius )
    else:
        h = horizontalhexagon( x, y, radius )

    s = shift
    while s > 0:
        s -= 1
        t = h.pop()
        h.insert(0, t)

    hseg = [
        (h[0], h[1], seg1, 1),
        (h[1], h[2], seg1, 0),
        (h[2], h[3], seg3, 1),
        (h[3], h[4], seg3, 0),
        (h[4], h[5], seg2, 1),
        (h[5], h[0], seg2, 0)]

    result = []

    for part in hseg:
        p1 = part[0]
        p2 = part[1]
        seg = part[2]
        rev = part[3]
        
        s = getsegment( seg, p1, p2, rev)
        result.extend( s )

    # debug stuff
    if debug:
        push()
        nofill()
        stroke(0,0,1,0.5)
        autoclosepath(1)
        beginpath()
        hl = list(h)
        p0 = hl.pop(0)
        textmarker((x,y-25), str(shift), 25)

        moveto( *p0 )
        #textmarker(p0, "h1", 20)
        nofill()
        i=2
        for p in hl:
            lineto( *p )
            # textmarker(p, "h"+str(i), 20)
            nofill()
            i += 1
        endpath(1)
        pop()
    return result

def textmarker(p, s, fsize):
    #return
    push()
    px, py = p
    fill(0.66, 0.66, 0.66, 0.66)
    if fsize > 25:
        fill(0.33, 0.33, 0.33, 0.66)
    fontsize(fsize)
    w = textwidth( s ) / 2.0
    h = textheight(s)
    text(s, px-w, py+h+1)
    pop()

def drawlines( lines, close=False):
    # return
    start = lines[0]
    
    autoclosepath(False)
    if close:
        autoclosepath(True)
    beginpath()
    moveto( *start )
    last = start
    i = 0
    # textmarker(start, str(i), 8)
    nofill()
    if close:
        fill( random(), random(), random(), random()/4.0)
    for l in lines[1:]:
        i += 1
        if l != last:
            lineto( *l )
            #textmarker( l, str(i),8)
            #nofill()
        last = l
        
    p = endpath()
    stroke(0)
    #nofill()
    drawpath( p )

def inrect( px,py,rd,t,l,b,r):
    if px+rd < l or px-rd > r:
        return False
    if py+rd < t or py-rd > b:
        return False
    return True


def hexfill( sx,sy,s,rd,vert,t,l,b,r):
    result = [ (sx,sy,s) ]
    start = hashcoordinates( sx,sy )
    locations = { (start): s }
    
    hexcoords = generate(sx,sy,rd,s,vert)

    while len(hexcoords) > 0:
        
        tmp = hexcoords.pop(0)
        px,py,ps = tmp
        
        if inrect(px,py,rd,t,l,b,r):
            cx,cy = hashcoordinates(px,py)
            if not (cx,cy) in locations:
                locations[ (cx,cy) ] = None
                result.append( tmp )
                tmp = generate(px,py,rd,ps,vert)
                hexcoords.extend( tmp )
    return result

def hashcoordinates( x,y,res=2 ):
    x = int( round(x,res) * ( 10**res ))
    y = int( round(y,res) * ( 10**res ))
    return (x,y)

def generate(x,y,r,s, horver=True):
    """
    """
    result = [ (x,y,s) ]
    offsets = horoffsets
    if horver:
        offsets = veroffsets
    for i in offsets(x, y, r, s):
        result.append( i )
    return result

def tileReptiles( x,y, orientation, radius, hexType, *rectangle):
    items = hexfill( x,y, orientation, radius, hexType, *rectangle)
    print "#items:",len(items)
    for item in items:
        px, py, ps = item
        rd = reptile( px, py, radius, 0, ps, hexType)
        drawlines( rd, 1 )

nofill()
stroke(0)
strokewidth(0.25)

radius = 50
frame = (100, 100,500,500 )
x,y = frame[2] - frame[0], frame[3] - frame[1]

tileReptiles(x, y, 0, radius, 1, *frame)

