sl = ximport("strokelib")

linecapitems = dict(
    FLAT    = sl.linecap_flat,
    ROUNDED = sl.linecap_rounded)

transformitems = dict( 
    UNIFORM  = sl.transform_uniform,
    EXPAND   = sl.transform_expand,
    CONTRACT = sl.transform_contract,
    SMOOTH   = sl.transform_smooth)


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

transfrm = transformitems['SMOOTH']
linecp = linecapitems['FLAT']


def makeoutline( startx, starty, ctrl1x, ctrl1y,
                 ctrl2x, ctrl2y, endx, endy,
                 width, transform, linecap, fixedangle=ang,
                 path1=1, path2=1, dbg=1  ):
    # PATH 1
    nofill()
    stroke(0)
    strokewidth(1)

    path = sl.makepath( startx, starty, ctrl1x, ctrl1y, ctrl2x, ctrl2y, endx, endy )

    strokewidth( width )
    path = sl.outline_stroke(path, debug=dbg, fixedangle=fixedangle)

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
        path = sl.outline_stroke(path, linecap=linecp, transform=transfrm, debug=True, fixedangle=ang)
        strokewidth(1)
        fill(0.4,0,0.4,0.25)
        drawpath(path)

def handler(val, name):
    global transfrm, linecp, startx, starty, ctrl1x, ctrl1y, ctrl2x, ctrl2y, endx, endy, width, ang
    
    if name == 'Transform':
        transfrm = transformitems[val]
    elif name == 'Linecap':
        linecp = linecapitems[val]
    elif name == 'startx':
        startx = int( val )
    elif name == 'starty':
        starty = int( val )
    elif name == 'ctrl1x':
        ctrl1x = int( val )
    elif name == 'ctrl1y':
        ctrl1y = int( val )
    elif name == 'ctrl2x':
        ctrl2x = int( val )
    elif name == 'ctrl2y':
        ctrl2y = int( val )
    elif name == 'endx':
        endx = int( val )
    elif name == 'endy':
        endy = int( val )
    elif name == 'width':
        width = int( val )
    elif name == 'ang':
        ang = float( val )
    
    makeoutline(startx, starty, ctrl1x, ctrl1y,
                ctrl2x, ctrl2y, endx, endy,
                width, transfrm, linecp, ang )

var('Transform', MENU, default="SMOOTH", handler=handler, menuitems=list(transformitems.keys()))
var('Linecap', MENU, default="FLAT", handler=handler, menuitems=list(linecapitems.keys()))
var('startx', NUMBER, 100, 0, 800, handler=handler )
var('starty', NUMBER, 100, 0, 800, handler=handler )
var('ctrl1x', NUMBER, 334, 0, 800, handler=handler )
var('ctrl1y', NUMBER,  49, 0, 800, handler=handler )
var('ctrl2x', NUMBER, 257, 0, 800, handler=handler )
var('ctrl2y', NUMBER, 400, 0, 800, handler=handler )
var('endx', NUMBER, 400, 0, 800, handler=handler )
var('endy', NUMBER, 377, 0, 800, handler=handler )
var('width', NUMBER, 30, 1, 200, handler=handler )
var('ang', NUMBER, 0, 0, 360, handler=handler )

makeoutline(startx, starty, ctrl1x, ctrl1y,
                ctrl2x, ctrl2y, endx, endy,
                width, transfrm, linecp, ang )