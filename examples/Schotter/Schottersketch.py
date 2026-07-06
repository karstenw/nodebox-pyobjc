#
# inspired by
# https://github.com/abey79/vsketch
#
# http://www.medienkunstnetz.de/works/schotter/
# Georg Nees
#

from random import seed

columns = 12
rows = 22

unit = 35

inset = 2

rotationscale = 1.0
translationscale = 0.5

damp = 1

w = (1 + columns + 2 * inset) * unit
h = (3 + rows + 2 * inset) * unit
size( w, h )

# seed( 0 )

for row in range(rows):
    
    ang = rotationscale * (row+1)
    offset = translationscale * (row+1)
    
    push()
    reset()
    align( CENTER )
    nofill()
    stroke( 0 )
    strokewidth( 1 )
    translate( inset*unit, (inset+1)*unit )

    for column in range( columns ):
        x = column * unit
        y = row * unit

        xoff = random( -offset, offset )
        yoff = random( -offset, offset )
        translate( xoff, yoff )
        
        rot = random( -ang, ang )
        rotate( rot )

        rect( x,y, unit, unit )
        
        # prevent rotation & translation
        # accumulation over the row
        if damp:
            rotate( -rot )
            translate( -xoff, -yoff )
    pop()
