sl = ximport("strokelib")

FLAT    = sl.linecap_flat
ROUNDED = sl.linecap_rounded
 
UNIFORM  = sl.transform_uniform
EXPAND   = sl.transform_expand
CONTRACT = sl.transform_contract
SMOOTH   = sl.transform_smooth


startx = 100
starty = 100
ctrl1x = 334
ctrl1y =  49
ctrl2x = 257
ctrl2y = 400
endx = 400
endy = 377

ang = 0
width = 30

path1 = 1
path2 = 1


# PATH 1
nofill()
stroke(0)
strokewidth(1)

path = sl.makepath( startx, starty, ctrl1x, ctrl1y, ctrl2x, ctrl2y, endx, endy )

strokewidth( width )
path = sl.outline_stroke(path, debug=True, fixedangle=ang)

nofill()
if path1: 
    strokewidth(1)
    fill(0.4, 0, 0.4, 0.25)
    drawpath(path)


# PATH 2
nofill()
stroke(0)
strokewidth(1)

path = sl.makepath( startx, starty, ctrl1x, ctrl1y, ctrl2x, ctrl2y, endx, endy )

strokewidth( width - 2 )
if path2:
    path = sl.outline_stroke(path, transform=SMOOTH, debug=True, fixedangle=ang)
    strokewidth(1)
    fill(0.4,0,0.4,0.25)
    drawpath(path)
