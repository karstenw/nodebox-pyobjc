import pprint
pp = pprint.pprint

import numpy

from AppKit import NSBitmapImageRep, NSDeviceRGBColorSpace

colors = ximport("colors")

PUREPYTHON = False


def makeColorlookup( iterations ):
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
            colorcache[idx+3] = 255
        else:
            colorcache[idx+0] = int(c.red   * 255)
            colorcache[idx+1] = int(c.green * 255)
            colorcache[idx+2] = int(c.blue  * 255)
            colorcache[idx+3] = 255
    return colorcache



def handlecoordinate(value, name):
    global fsize, xpos, ypos, delta, iterations, const_real, const_imag, limit, zoom
    if name == "fsize":
        fsize = int(value)
    elif name == "xpos":
        xpos = float(value)
    elif name == "ypos":
        ypos = float(value)
    elif name == "delta":
        delta = float(value)
        zoom = 1 / delta
        #print "delta", delta
        #print "zoom", zoom
    elif name == "zoom":
        zoom = float(value)
        delta = 1 / zoom
        print "delta", delta
        print "zoom", zoom
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
    pp( (fsize, xpos, ypos, delta, iterations, const_real, const_imag, limit ) )
    render( fsize, xpos, ypos, delta, iterations, const_real, const_imag, limit )


delta = 4.0
var("fsize", NUMBER, 400, 300, 1100, handler=handlecoordinate)
var("xpos", NUMBER, 0.0, -6.0, 6.0, handler=handlecoordinate)
var("ypos", NUMBER, 0, -3.5, 3.5, handler=handlecoordinate)
# var("delta", NUMBER, 4.0, 0.0001, 20.0, handler=handlecoordinate)
var("zoom", NUMBER, 0.25, 0.01, 20.0, handler=handlecoordinate)
var("iterations", NUMBER, 64, 0, 256, handler=handlecoordinate)
var("const_real", NUMBER, 0.0, 0.0, 2.0, handler=handlecoordinate)
var("const_imag", NUMBER, 0.0, 0.0, 2.0, handler=handlecoordinate)
var("limit", NUMBER, 2.0, 0.01, 6.00, handler=handlecoordinate)


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
    pixels = numpy.zeros(width * height * 4, dtype=numpy.uint8)
    for y in xrange( height ):
        for x in xrange( width ):
            xc = xpos + float(x) / width * dx
            yc = ypos + float(y) / height * dy
            # v = mandelbrot(xc, yc, iterations, const_real, const_imag, limit)

            z = complex(xc, yc)
            o = complex(0, 0)
            res = 0
            for i in xrange(iterations):
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

    # clut = makeColorlookup( iterations )
    result = fractalimage(clut, width,height, iterations,xpos,ypos,dx,dy,const_real,const_imag,limit)
    # out = PIL.Image.frombytes( 'RGBA', (w,h), result, decoder_name='raw')

    return result


def render(fsize, xpos, ypos, d, i, const_real, const_imag, limit):
    half = d / 2.0
    left = xpos - half
    top = ypos - half
    W = H = fsize
    size(W, H)
    n = W * H
    clut = makeColorlookup( i )
    if PUREPYTHON:
        pixels = iterPixels(W, H, i, left, d, top, d, const_real, const_imag, clut, limit)
    else:
        pixels = dofractal(W, H, i, left, d, top, d, const_real, const_imag, clut, limit)
    
    bytes = makeImage( pixels, W, H)
    image(None, 0, 0, data=bytes)

render(fsize, xpos, ypos, delta, iterations, const_real, const_imag, limit)

