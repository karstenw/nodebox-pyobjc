
from __future__ import print_function

import math
import time

import pprint
pp = pprint.pprint

from AppKit import NSBitmapImageRep, NSDeviceRGBColorSpace

colors = ximport("colors")


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v *= 1.0
        return (v, v, v)
    i = int( h * 6.) # XXX assume int() truncates!
    f = ( h * 6.) - i
    p = float(1.0 * (v * (1. - s)))
    q = float(1.0 * (v * (1. - s * f)))
    t = float(1.0 * (v * (1. - s * (1.-f))))
    v *= 1.0
    i %= 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)



def makeColorlookupOLD( iterations, maxi ):
    #clr1 = colors.rgb(0.6, 0.8, 1.0)
    #clr2 = colors.rgb(0.0, 0.2, 0.4)
    #g = colors.gradient(clr1, clr2, steps=iterations)
    g = colors.range(h=(0.0,1.0), s=(0.25,0.75), b=(0.0,1.0), a=(1.0,1.0), 
                     grayscale=False, name="", length=iterations)

    colorcache = bytearray( iterations * 4 )
    for i in range(iterations):
        idx = i * 4
        c = g[i]
        if i == 0:
            colorcache[idx+0] = 0
            colorcache[idx+1] = 0
            colorcache[idx+2] = 0
            colorcache[idx+3] = 255
        else:
            colorcache[idx+0] = int(c.red   * 255)
            colorcache[idx+1] = int(c.green * 255)
            colorcache[idx+2] = int(c.blue  * 255)
            colorcache[idx+3] = 255
    return bytes( colorcache )


def paletteBlueish( i, maxi ):
    log_it = math.log( float(i) )
    r = int( 255 * (1 + math.cos(3.320 * log_it)) / 2.0 )
    g = int( 255 * (1 + math.cos(0.974 * log_it)) / 2.0 )
    b = int( 255 * (1 + math.cos(0.412 * log_it)) / 2.0 )
    a = 255
    return r,g,b,a

def paletteOther( i, maxi ):
    r = (255 - i*30) % 255
    g = 100
    b = 100
    a = 255
    return r,g,b,a


h = 100/255.0
s = 100/255.0

def paletteHLS( i, maxi ):
    v = i / float( maxi)
    r,g,b = hsv_to_rgb( h, s, v )
    r = int( 255 * r )
    g = int( 255 * g )
    b = int( 255 * b )
    # pp( (i, maxi, r,g,b) )
    return r,g,b,255
    

def paletteOrange(i, maxi):
    h = i / float(maxi)
    s = i / float(maxi)
    v = i / float(maxi)
    r,g,b = hsv_to_rgb( h, s, v )
    r = int( 255 * r )
    g = int( 255 * g )
    b = int( 255 * b )
    return r,g,b,255

    
paletteMakers = dict(
    Old=makeColorlookupOLD,
    Blueish=paletteBlueish,
    Other=paletteOther,
    HLS=paletteHLS)
    

def makeColorlookup( iterations ):
    colorcache = bytearray( iterations * 4 )
    colorcache[0] = colorcache[1] = colorcache[2] = 0
    colorcache[3] = 255
    for i in range(1, iterations):
        idx = i * 4
        
        if 1:
            r,g,b,a = paletteBlueish( i, iterations )
        elif False:
            r,g,b,a = paletteHLS( i, iterations )
        elif True:
            r,g,b,a = paletteOrange( i, iterations )
        elif 0.0:
            r,g,b,a = makeColorlookupOLD( i, iterations )
        else:
            r,g,b,a = paletteOther( i, iterations )
        colorcache[idx+0] = r
        colorcache[idx+1] = g
        colorcache[idx+2] = b
        colorcache[idx+3] = a

    return bytes( colorcache )




def handlecoordinate(value, name):
    global fsize, xpos, ypos, delta, iterations, const_real
    global const_imag, limit, zoom, h, s, USE_C_EXT

    if name == "fsize":
        fsize = int(value)
    elif name == "xpos":
        xpos = float(value)
        print( "xpos", xpos )
    elif name == "ypos":
        ypos = float(value)
    elif name == "delta":
        delta = float(value)
        zoom = 1 / delta
        #print( "delta", delta )
        #print( "zoom", zoom )
    elif name == "zoom":
        zoom = float(value)
        delta = 1 / zoom
        #print( "delta", delta )
        #print( "zoom", zoom )
    elif name == "iterations":
        iterations = int( value )
    elif name == "const_real":
        const_real = float( value )
        # const_imag = const_real
    elif name == "const_imag":
        const_imag = float( value )
        #const_real = const_imag
    elif name == "limit":
        limit = float( value )
    elif name == "h":
        h = float( value )
    elif name == "s":
        s = float( value )
    elif name == "USE_C_EXT":
        USE_C_EXT = bool( value )
    elif name == "Palette":
        pass
    # pp( (fsize, xpos, ypos, delta, iterations, const_real, const_imag, limit ) )
    render( fsize, xpos, ypos, delta, iterations, const_real, const_imag, limit )


delta = 4.0 #0.5
inity = -0.75 # -1.75

var("fsize", NUMBER, 600, 300, 1200, handler=handlecoordinate)
var("xpos", NUMBER,  0.0, -6.0, 6.0, handler=handlecoordinate)
var("ypos", NUMBER,  0.0, -3.5, 3.5, handler=handlecoordinate)
# var("delta", NUMBER, 4.0, 0.0001, 20.0, handler=handlecoordinate)
var("zoom", NUMBER, 1.0/delta, 0.01, 5.0, handler=handlecoordinate)
var("iterations", NUMBER, 100, 0, 1000, handler=handlecoordinate)
var("const_real", NUMBER, 0.0, 0.0, 2.0, handler=handlecoordinate)
var("const_imag", NUMBER, 0.0, 0.0, 2.0, handler=handlecoordinate)
var("limit", NUMBER, 4.0, 0.01, 6.00, handler=handlecoordinate)
#var("h", NUMBER, 0.5,  0.0, 1.00, handler=handlecoordinate)
#var("s", NUMBER, 0.5,  0.0, 1.00, handler=handlecoordinate)
var("USE_C_EXT", BOOLEAN, True, False, True, handler=handlecoordinate)
#var("Palette", MENU, default="Blueish", handler=handlecoordinate, menuitems=["HLS", "Blueish", "Other", "Old"])


def makeImage( pixels, W, H ):
    # pixels2 = pixels.tobytes()
    # b = (pixels2, None, None, None, None)
    b = (pixels, None, None, None, None)
    # pixels2 = (''.join(pixels), None, None, None, None)
    img = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(b, W, H, 8, 4, True, False, NSDeviceRGBColorSpace, W * 4, 32 )
    return img.TIFFRepresentation()


def mandelbrot(x, y, depth, cr, ci, l):
    z = complex(x, y)
    o = complex(0, 0)
    for i in range(depth):
        if abs(o) <= l:
            o = o*o + z
        else:
            return( i )
    return( 0 )


def iterPixels(width, height, iterations, xpos, dx, ypos, dy, const_real, const_imag, clut, limit):
    pixels = bytearray( width * height * 4 )
    for y in range( height ):
        for x in range( width ):
            xc = xpos + float(x) / width * dx
            yc = ypos + float(y) / height * dy
            # v = mandelbrot(xc, yc, iterations, const_real, const_imag, limit)

            z = complex(xc, yc)
            o = complex(0, 0)
            res = 0
            for i in range(iterations):
                if abs(o) <= limit:
                    o = o*o + z
                else:
                    res = i
                    break
            
            idx = res * 4
            o = (y * width + x) * 4
            for z in range(4):
                pixels[o+z] = clut[idx+z]
    return pixels


def dofractal( width, height, iterations, xpos, dx, ypos, dy, const_real, const_imag, clut, limit ):
    return fractalimage(clut, width,height, iterations,xpos,ypos,dx,dy,const_real,const_imag,limit)


def render(fsize, xpos, ypos, d, i, const_real, const_imag, limit):
    clut = makeColorlookup( i )
    half = d / 2.0
    left = xpos - half
    top = ypos - half
    W = H = fsize
    size(W, H)
    n = W * H

    start = time.time()

    if USE_C_EXT:
        pixels = dofractal(W, H, i, left, d, top, d, const_real, const_imag, clut, limit)
    else:
        pixels = iterPixels(W, H, i, left, d, top, d, const_real, const_imag, clut, limit)
    bytes = makeImage( pixels, W, H)
    image(None, 0, 0, data=bytes)

    print( "%ix%i = %i pixel in %.4fs" % (W,H,W*H,time.time()-start ) )


render(fsize, xpos, ypos, delta, iterations, const_real, const_imag, limit)

