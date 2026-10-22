import pprint
pp = pprint.pprint

import math
import time

from AppKit import NSBitmapImageRep, NSDeviceRGBColorSpace



def paletteBlue( i, maxi ):
    log_it = math.log( float(i) )
    r = int( 255 * (1 + math.cos(3.320 * log_it) ) / 2 )
    g = int( 255 * (1 + math.cos(0.974 * log_it) ) / 2 )
    b = int( 255 * (1 + math.cos(0.412 * log_it) ) / 2 )
    a = 255
    return r,g,b,a


def paletteOther( i, maxi ):
    r = (255 - i*30) % 255
    g = 100
    b = 100
    a = 255
    return r,g,b,a


fsize = 600
xpos = 0.0
ypos = -0.75
delta = 0.5
iterations = 100
const_real = 0.0
const_imag = 0.0
limit = 4.0

palette = paletteBlue



def makeColorlookup( iterations ):
    colorcache = bytearray( iterations * 4 )
    colorcache[0] = colorcache[1] = colorcache[2] = 0
    colorcache[3] = 255
    for i in range(1, iterations):
        idx = i * 4
        r,g,b,a = palette( i, iterations )
        colorcache[idx+0] = r
        colorcache[idx+1] = g
        colorcache[idx+2] = b
        colorcache[idx+3] = a
    return bytes( colorcache )


def makeImage( pixels, W, H ):
    b = (pixels, None, None, None, None)
    img = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(b, W, H, 8, 4, True, False, NSDeviceRGBColorSpace, W * 4, 32 )
    return img.TIFFRepresentation()


def iterPixels(width, height, iterations, xpos, dx, ypos, dy, const_real, const_imag, clut, limit):
    pixels = bytearray( width * height * 4 )
    for y in range( height ):
        for x in range( width ):
            xc = xpos + float(x) / width * dx
            yc = ypos + float(y) / height * dy

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


def render(fsize, xpos, ypos, d, i, const_real, const_imag, limit):
    half = d / 2.0
    left = xpos - half
    top = ypos - half
    W = H = fsize
    size(W, H)
    n = W * H
    clut = makeColorlookup( i )

    start = time.time()
    pixels = iterPixels(W, H, i, left, d, top, d, const_real, const_imag, clut, limit)
    print( "%ix%i = %i pixel in %.4fs" % (W,H,W*H,time.time()-start ) )

    bytes = makeImage( pixels, W, H)
    image(None, 0, 0, data=bytes)


if 1: #__name__ in ('__main__', '__builtin__'):
    render(fsize, xpos, ypos, delta, iterations, const_real, const_imag, limit)


