

"""
Metaballs & marching squares in Nodebox.

Original:
https://github.com/Mimkaa/Metaballs-marching_squares_alg-

Other influences:
https://github.com/nagy135/pyballs

Ground Zero; where it all began. Headers and footers here (made with webgl?):
https://lucumr.pocoo.org/2026/2/13/the-final-bottleneck/


"""

import sys
import os
import time
import math
import pprint
pp = pprint.pprint
import random as rnd
import numpy as np

import pdb

# vec = squeaklib.Point


# define some colors (R, G, B)
colormode(RGB, 255)
WHITE = color(255, 255, 255)
BLACK = color(0, 0, 0)
DARKGREY = color(40, 40, 40)
LIGHTGREY = color(100, 100, 100)
GREEN = color(0, 255, 0)
RED = color(255, 0, 0)
YELLOW = color( 210, 210, 210)
BLUE = color(0,0,255)


playfield = 512
size( playfield, playfield )

FPS = 30
TITLE = "Metaballs"
BGCOLOR = DARKGREY

TILESIZE = 20
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE

nblobs = 6
blobminradius, blobmaxradius = 16, 64
blobinset = 8

dbg = 1
# dbgbreak = 0
markers = 1

circles = 0
DRAWGRID = 1
HEATMAP = 0

newfields = 0
timeit = 0

squaregrid = np.zeros( (GRIDWIDTH+1, GRIDHEIGHT+1) )


class Blob:
    def __init__(self, posx, posy, r):
        self.pos = Point( posx, posy )
        self.radius = r
        angl = rnd.uniform( 0, math.pi * 2 )
        self.vel = Point( math.cos(angl),
                          math.sin(angl) ) * rnd.randint(5,20)
    
    def update(self, dt):
        self.pos += self.vel * dt
        delta = self.radius / 2
        if self.pos.x > WIDTH+delta or self.pos.x < -delta:
            self.vel.x *= -1
        if self.pos.y > HEIGHT+delta or self.pos.y < -delta:
            self.vel.y *= -1
    
    def show(self):
        if 1 and circles:
            push()
            oldc = stroke( LIGHTGREY )
            oldw = strokewidth( 1.0 )
            nofill()
            circle( self.pos.x, self.pos.y, self.radius )
            pop()
            stroke( oldc )
            strokewidth( oldw )

blobs = [
    Blob( rnd.randint( blobinset,  WIDTH - (2*blobinset)),
                       rnd.randint( blobinset, HEIGHT - (2*blobinset)),
                       rnd.randint( blobminradius, blobmaxradius ))]



def makeblobs( n ):
    global blobs
    # pdb.set_trace()
    print("makeblobs()", len(blobs), n)
    l = len( blobs )
    if n < l:
        blobs = blobs[:n]
    elif n > l:
        while len(blobs) < n:
            blobs.append(
                Blob( rnd.randint( blobinset,  WIDTH - (2*blobinset)),
                       rnd.randint( blobinset, HEIGHT - (2*blobinset)),
                       rnd.randint( blobminradius, blobmaxradius )) )
    
    return
    
    old =  [
        Blob( rnd.randint( blobinset,  WIDTH - (2*blobinset)),
            rnd.randint( blobinset, HEIGHT - (2*blobinset)),
            rnd.randint( blobminradius, blobmaxradius )) for i in range( n )]

makeblobs( nblobs )



def setup():
    global blobs
    makeblobs(nblobs)
    

def handler( val, name ):
    global circles, playfield, TILESIZE, GRIDWIDTH, GRIDHEIGHT, squaregrid, nblobs, blobs, DRAWGRID, HEATMAP, blobminradius, blobmaxradius, markers
    
    if name == "circles":
        circles = 0
        if val > 0:
            circles = 1
    elif name == "playfield":
        playfield = int(val)
        size(playfield,playfield)
        GRIDWIDTH = WIDTH // TILESIZE
        GRIDHEIGHT = HEIGHT // TILESIZE
        squaregrid = np.zeros( (GRIDWIDTH+1, GRIDHEIGHT+1) )
        blobminradius = WIDTH // 64
        blobmaxradius = WIDTH // 8
        makeblobs(nblobs)
    elif name == "TILESIZE":
        TILESIZE = int(val)
        GRIDWIDTH = WIDTH // TILESIZE
        GRIDHEIGHT = HEIGHT // TILESIZE
        squaregrid = np.zeros( (GRIDWIDTH+1, GRIDHEIGHT+1) )
    elif name == "nblobs":
        nblobs = int( val )
        makeblobs(nblobs)
    elif name == "DRAWGRID":
        DRAWGRID = int( val )
    elif name == "HEATMAP":
        HEATMAP = int( val )
    elif name == "markers":
        markers = int(val)


playfieldsizes = [256, 320, 512, 640, 768, 1024]
var("playfield", MENU, default=512, handler=handler, menuitems=playfieldsizes)


gridsizes = [8, 12, 16, 20, 24, 28, 32]
var("TILESIZE", MENU, default=20, handler=handler, menuitems=gridsizes)

blobcounts = list(range(1,25))
var("nblobs", MENU, default=8, handler=handler, menuitems=blobcounts )

var("circles", BOOLEAN, False, False, True, handler=handler)

var("DRAWGRID", BOOLEAN, False, False, True, handler=handler)

var("HEATMAP", BOOLEAN, False, False, True, handler=handler)

var("markers", BOOLEAN, False, False, True, handler=handler)

markers

# UNUSED
NORTH, SOUTH, EAST, WEST = list(range(4))


def pline( p1, p2 ):
    # draw a line between 2 points
    line( p1.x, p1.y, p2.x, p2.y )
    if 1 and markers:
        push()
        oldc = stroke( RED )
        oldw = strokewidth( 1.0 )
        
        circle( p1.x, p1.y, 4 )
        pop()
        stroke( oldc )
        strokewidth( oldw )


def transscale( value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def distance_vec( vec1, vec2 ):
    return math.sqrt(   (vec1.x - vec2.x) ** 2
                      + (vec1.y - vec2.y) ** 2)


def draw_grid():
    # LIGHTGREY
    push()
    oldc = stroke( LIGHTGREY )
    oldw = strokewidth( 0.334 )
    nofill()
    for x in range(0, WIDTH, TILESIZE):
        line( x, 0, x, HEIGHT)
    for y in range(0, HEIGHT, TILESIZE):
        line( 0, y, WIDTH, y)
    pop()
    stroke( oldc )
    strokewidth( oldw )
    

def update_fields():
    global blobs
    # update the squaregrid
    if blobs is None:
        makeblobs(nblobs)

    maxsum = 0
    dist = distance
    for i in range(GRIDWIDTH+1):
        for j in range(GRIDHEIGHT+1):
            sum = 0
            x = i * TILESIZE
            y = j * TILESIZE
            p = Point( x, y )
            
            for blob in blobs:
                pos = blob.pos
                d = distance(pos.x, pos.y, x, y)
                #d = distance_vec(pos, p )
                #d = dist(pos.x, pos.y, x, y)
                if d == 0:
                    d = 1
                sum += (blob.radius * 0.667) / d
            squaregrid[i][j] = sum
            if sum > maxsum:
                maxsum = sum
    # update blobs
    delta = 1 / FPS
    for b in blobs:
        b.update( 0.25 )
    return maxsum


def update_fields2():
    global blobs
    # update the squaregrid
    # pdb.set_trace()
    xygrids = []
    for blob in blobs:
        xsquares = np.zeros( GRIDWIDTH+1 )
        for x in range( GRIDWIDTH+1 ):
            xc = x * TILESIZE
            xsquares[x] = (blob.pos.x - xc)**2
        ysquares = np.zeros( GRIDHEIGHT+1 )
        for y in range( GRIDHEIGHT+1 ):
            yc = y * TILESIZE
            ysquares[y] = (blob.pos.y - yc)**2
        xygrids.append( (xsquares, ysquares) )
    
    
    arr = np.ones( (GRIDWIDTH+1, GRIDHEIGHT+1) )
    for i, blob in enumerate(blobs):
        X, Y = np.meshgrid( np.array(xygrids[i][0]),
                            np.array(xygrids[i][1]))
        arr *= 20_000
        arr /= (X+Y)
        
    norm = np.linalg.norm( arr.clip(0,500) )
    arr /= norm
    
    arr *= 20000
    arr %= 255

    maxsum = 0
    dist = distance
    for i in range(GRIDWIDTH+1):
        for j in range(GRIDHEIGHT+1):
            sum = 0
            x = i * TILESIZE
            y = j * TILESIZE
            p = Point( x, y )
            for blob in blobs:
                pos = blob.pos
                d = distance(pos.x, pos.y, x, y)
                #d = distance_vec(pos, p )
                #d = dist(pos.x, pos.y, x, y)
                if d == 0:
                    d = 1
                sum += (blob.radius * 0.667) / d
            squaregrid[i][j] = sum
            if sum > maxsum:
                maxsum = sum
    # update blobs
    delta = 1 / FPS
    for b in blobs:
        b.update( 0.25 )
    return maxsum


def update_grid(): # blobs, grid ):
    xygrids = []
    for blob in blobs:
        xsquares = np.zeros( WIDTH )
        ysquares = np.zeros( WIDTH )
        for x in range(WIDTH):
            xsquares[x] = (blob.pos.x - x)**2
        for y in range( HEIGHT ):
            ysquares[y] = (blob.pos.y - y)**2
        xygrids.append( (xsquares, ysquares) )
    
    arr = np.ones( (GRIDWIDTH+1, GRIDHEIGHT+1) )
    for i, blob in enumerate(blobs):
        X, Y = np.meshgrid( np.array(xygrids[i][0]),
                            np.array(xygrids[i][1]))
        arr *= 20_000
        arr /= (X+Y)
        
    norm = np.linalg.norm( arr.clip(0,500) )
    arr /= norm
    
    arr *= 20000
    arr %= 255
    






def get_state( a, b, c, d):
    # gets number of case based on its  binary representation
    return a * 8 + b * 4 + c * 2 + d * 1

def find_lerp_factor(val1, val2, iso_val):
    t = (iso_val - val1) / (val2 - val1)
    return max(min(1, t), 0)


def linear_interp(val1, val2, start, end):
    
    tilesize = end - start
    # return start + ( 0.5 * tilesize)
    dist = val2 - val1
    if dist == 0:
       dist = 1
    
    result = start + ( (1-val1) / dist ) * tilesize

    #t = (1-val1) * dist
    #t =  (val1 / dist)
    # result = start + ( t * tilesize)
    if 0 and dbg:
        print("linear_interp:", (val1, val2, start, end))
        pdb.set_trace()
        pp( locals() )
        
    return result



speed( FPS )

def setup():
    pass

maxtime = mintime = 0
def draw():
    global maxtime, mintime
    start = time.time()
    background( BLACK )
    
    update = update_fields
    if newfields > 0:
        update = update_fields2
    
    maxsum = update()
    s1 = time.time()
    if timeit:
        print( "fields: %.4fs" % (s1 - start) )
    
    
    if 0:
        if FRAME // 100 == 0:
            print("maxsum:", maxsum)

    if HEATMAP:
        # nofill()
        strokewidth( 0 )
        for i in range(GRIDWIDTH+1):
            for j in range(GRIDHEIGHT+1):
                #clo = transscale(squaregrid[i][j], 0, 100 , 0, 255)
                clo = squaregrid[i][j]
                #stroke( clo, clo, clo, 127)
                fill( 0, 0, clo, 127 )
                # circle( i*TILESIZE, j*TILESIZE, 5 )
                rect( i*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE )
    
    if DRAWGRID:
        draw_grid()

    # draw blobs
    for blob in blobs:
        blob.show()
    s2 = time.time()
    if timeit:
        print( "blobs: %.4fs" % (s2 - s1) )
    
    strokewidth( 1.5 )
    stroke( LIGHTGREY )
    
    # outlines
    for j in range(GRIDHEIGHT):
        for i in range(GRIDWIDTH):
            x = i * TILESIZE
            y = j * TILESIZE
            
            xend = x + TILESIZE
            yend = y + TILESIZE
            
            topleft = squaregrid[i][j]
            topright = squaregrid[i+1][j]
            bottomright = squaregrid[i+1][j+1]
            bottomleft = squaregrid[i][j+1]
            
            # top mid
            toppoint = linear_interp( topleft, topright, x, xend)
            a = Point( toppoint, y )
            
            # right mid
            righpoint = linear_interp( topright, bottomright, y, yend)
            b = Point( xend, righpoint )
            
            # bottom mid
            bottompoint = linear_interp( bottomleft, bottomright, x, xend)
            c = Point( bottompoint, yend)
            
            # left mid
            leftpoint = linear_interp(topleft, bottomleft, y, yend)
            d = Point( x, leftpoint)
            
            state = get_state( int(topleft),
                               int(topright),
                               int(bottomright),
                               int(bottomleft))

            if 0 < state <15:
                # pline(a,b)
                # pline(b,c)
                # pline(c,d)
                # pline(c,a)
                pass
            
            if 1:
                # 0001
                if state == 1:
                    pline( c, d )
                # 0010
                elif state == 2:
                    pline( b, c )
                # 0011
                elif state==3:
                    pline(b,d)
                # 0100
                elif state==4:
                    pline(a,b)
                # 0101
                elif state==5:
                    pline(a,d)
                    pline(c,b)
                # 0110
                elif state==6:
                    pline(a,c)
                # 0111
                elif state==7:
                    pline(a,d)
                # 1000
                elif state==8:
                    pline(d,a)
                # 1001
                elif state==9:
                    pline(a,c)
                # 1010
                elif state==10:
                    pline(d,a)
                    pline(c,b)
                # 1011
                elif state==11:
                    pline(a,b)
                # 1100
                elif state==12:
                    pline(d,b)
                # 1101
                elif state==13:
                    pline(c,b)
                # 1110
                elif state==14:
                    pline(c,d)
            
                elif state == 15:
                    pass
    stop = time.time()
    if timeit:
        print( "outlines: %.4fs" % (stop - s2) )
        print( "draw(): %.4fs" % (stop - start) )
        print()

