size(1000,750)

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

canvas = coreimage.canvas(1000, 750)

l = canvas.layer( path )
p = l.pixels()
canvas.draw()

fill(1)

fill(0.2)

dotsize = 12
dothalf = dotsize / 2

dotmul = 1.0
# dotmul = 1/1.4142
# dotmul = 1.4142

inset = 0

sqsize = dotsize - inset
alpha = 0.9

if inset > 0:
    insethalf = inset / 2
else:
    insethalf = 0

xcols = WIDTH / (dotsize - 1)
ycols = HEIGHT / (dotsize - 1)

def pixcol(p, x, y, o, a):
    clr = p.get_pixel(x + o, y + o)
    try:
        clr._set_alpha( a )
    except:
        pass
    return clr

for x, y in grid(xcols, ycols, dotsize, dotsize):
    clr = pixcol(p, x, y, dothalf, alpha)
    fill(clr)
    oval(x + insethalf,
         y + insethalf,
         sqsize * dotmul,
         sqsize * dotmul)

