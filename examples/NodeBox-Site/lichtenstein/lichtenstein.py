size(1000, 750)
fill(1)
rect(0, 0, WIDTH, HEIGHT)
 
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

width = 300
height = int(round(width / ratio))

canvas = coreimage.canvas( width, height )
l = canvas.append( path )
l.desaturate()
p = l.pixels()
 
colormode(RGB, 255)
w,h = l.size()

dotsize = 5
dotsize2 = dotsize * 2
for x, y in grid( w/dotsize, h / dotsize, dotsize,dotsize):
    clr = p.get_pixel(x,y)
    fill(0)
    
    cellsize = dotsize2 * (1-clr.r)
    oval(x,y, cellsize, cellsize )