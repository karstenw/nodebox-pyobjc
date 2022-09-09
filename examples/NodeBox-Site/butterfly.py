#size (400, 400)
dbg = False

if dbg:
	background(0.7, 0.7, 0.7)

from math import sin, cos, pi, exp
import sys

#translate(150, 150)

#scale(60, 60)

# strokewidth(2)

if dbg:
	stroke(0.3, 0.3, 0.3, 1)
else:
	stroke(0, 0, 0, 1)

n = 12

twopi = 2 * pi

l = n * twopi

theta = 0.0

stepwidth = 0.04

print( "l: ", l )
print( "steps: ", l / stepwidth )

while theta < l:
	r = exp( cos( theta )) - 2 * cos( 4 * theta ) + ( sin( theta / 12 ) ) ** 5

	x = r * cos(theta)
	y = r * sin(theta)

	xx = (x * 40) + 175
	yy = (y * 40) + 175

	# print xx, yy

	if (theta == 0.0):
		line(xx, yy, xx, yy)
	else:
		line(xOld, yOld, xx, yy)

	xOld = xx
	yOld = yy

	theta += stepwidth
