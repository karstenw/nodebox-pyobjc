size(800,600)

import pprint
#pprint.pprint(globals())
coreimage = ximport("coreimage")

import imagewells
loadImageWell = imagewells.loadImageWell

imagewell = loadImageWell(  bgsize=( 2048, 1024 ),
                            minsize=( 512, 512 ),
                            pathonly=True,
                            tabfilename=True)

path = choice( imagewell['tiles'] )
print( len(imagewell['tiles']),  path )
w,h = imagesize( path )
ratio = w/h



canvas = coreimage.canvas(800,600)



l = canvas.layer( path ) #"LP-17.07.09_08_small.jpg")
p = l.pixels()
canvas.draw()

fill(1)

fill(0.2)

square = 10
sqhalf = square / 2

inset = 0

if inset > 0:
    insethalf = inset / 2
else:
    insethalf = 0

sqsize = square - inset
alpha = 0.65

xcols = WIDTH / square
ycols = HEIGHT / square

def pixcol(p, x, y, o, a):
    clr = p.get_pixel(x + o, y + o)
    try:
        clr._set_alpha( a )
    except:
        pass
    return clr

for x, y in grid(xcols, ycols, square, square):
    clr = pixcol(p, x, y, sqhalf, alpha)
    fill(clr)
    rect(x + insethalf, y + insethalf,
         sqsize, sqsize)

