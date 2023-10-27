
from __future__ import print_function

import time
import numpy
from AppKit import NSBitmapImageRep, NSDeviceRGBColorSpace

colors = ximport("colors")

background( None )
def makeColorlookup( iterations, blackAlpha=255 ):
    """Create a color lookup table"""
    #clr1 = colors.rgb(0.6, 0.8, 1.0)
    #clr2 = colors.rgb(0.0, 0.2, 0.4)
    #g = colors.gradient(clr1, clr2, steps=iterations)
    g = colors.range(h=(0.0,1.0), s=(0.25,0.75), b=(0.0,1.0), a=(1.0,1.0), 
                     grayscale=False, name="", length=iterations)

    colorcache = numpy.zeros(iterations * 4, dtype=numpy.uint8)
    for i in range(iterations):
        idx = i * 4
        c = g[i]
        if i == 0:
            colorcache[idx+0] = 0
            colorcache[idx+1] = 0
            colorcache[idx+2] = 0
            colorcache[idx+3] = blackAlpha
        else:
            colorcache[idx+0] = int(c.red   * 255)
            colorcache[idx+1] = int(c.green * 255)
            colorcache[idx+2] = int(c.blue  * 255)
            colorcache[idx+3] = 255
    return colorcache


def makeImage( pixels, W, H ):
    """Make a TIFF representation usable for the 'image' command"""
    b = (pixels, None, None, None, None)
    img = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(b, W, H, 8, 4, True, False, NSDeviceRGBColorSpace, W * 4, 32 )
    return img.TIFFRepresentation()


def render(fsize, fsizey, xpos, ypos, d, i, d1, d2, limit):
    
    half = d / 2.0
    left = xpos - half
    r = fsize / float(fsizey)
    dy = d / r
    
    top = ypos - half
    top = ypos - (dy / 2.0)
    
    W = fsize
    H = fsizey
    size(W, H)
    n = W * H
    clut = makeColorlookup( i, blackAlpha=255 )

    pixels = fractalimage(clut, W,H, i,left,top,d,dy,d1,d2,limit)

    bytes = makeImage( pixels, W, H)
    image(None, 0, 0, data=bytes)


imgsize = 4096 # 16384
start = time.time()
render(imgsize,imgsize,
       -0.75,
       0,
       2.7,
       256, 0.0,0.0,4.0)
end = time.time()
print( "%i pixel in %.3f sec" % (imgsize*imgsize, end-start) )
print( "%.3f pixel/sec" % ((imgsize*imgsize) / (end-start)) )
print()


