import math
from math import *

s = 250

size( s, s)
 
a = 2
 
var("seeds", NUMBER, 100, 20, 1000)
semi = int(seeds)
 
var("angle", NUMBER, 2.39983333, 0.0, 6.28320000)
#angle = 1.5708 # = 90°
 
var("dim", NUMBER, 1, 0, 2)
 
var("dif", NUMBER, 0, 0, 0.01)
 
 
var("goldenRatio", BOOLEAN, False)
if goldenRatio:
    angle = 2.39983333
    
print( "---" )
print( "angle", angle )
print( "seeds", semi )
 
translate (WIDTH/2, HEIGHT/2)
 
for i in range(semi):
    x = a* sqrt(i) * cos(i* angle)
    y = a* sqrt(i) * sin(i* angle)
    
    rr = dim+(i*dif)
    
    oval(x-(rr/2), y-(rr/2), rr, rr)