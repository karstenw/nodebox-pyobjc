# Geometric functionality

import math

try:
    # Faster C versions.
    import cGeo
    isqrt = inverse_sqrt = cGeo.fast_inverse_sqrt
    angle = cGeo.angle
    distance = cGeo.distance
    coordinates = cGeo.coordinates

except ImportError:
    def inverse_sqrt(x):
        return 1.0 / math.sqrt(x)
    
    isqrt = inverse_sqrt

    def angle(x0, y0, x1, y1):
        return math.degrees( math.atan2(y1-y0, x1-x0) )

    def distance(x0, y0, x1, y1):
        return math.sqrt(math.pow(x1-x0, 2) + math.pow(y1-y0, 2))
    
    def coordinates(x0, y0, distance, angle):
        x1 = x0 + math.cos(math.radians(angle)) * distance
        y1 = y0 + math.sin(math.radians(angle)) * distance
        return x1, y1


try:
    import bwdithering
    dither = bwdithering.dither

except ImportError, err:
    print
    print '-' * 40
    print
    print err
    print 
    print '-' * 40
    print
    def dither(*args):
        print "You lost."

try:
    import fractal
    fractalimage = fractal.fractalimage
except ImportError, err:
    print
    print '-' * 40
    print
    print err
    print 
    print '-' * 40
    print
    def fractalimage(*args):
        print "You lost."


def reflect(x0, y0, x1, y1, d=1.0, a=180):
    d *= distance(x0, y0, x1, y1)
    a += angle(x0, y0, x1, y1)
    x, y = coordinates(x0, y0, d, a)
    return x, y

