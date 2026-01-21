
size( 1440, 900 )


fonts = fontnames()


def menuhandler( value, name ):
    global typeface, text, size, stitches
    if name == 'typeface':
        typeface = value
    elif name == 'text':
        text = value
    elif name == 'size':
        size = int(value)
    elif name == 'stitches':
        stitches = int( value )
    run()
    


# var("typeface", TEXT, "Times-Bold")
var("typeface", MENU, default=menuhandler, value=fonts)


var("text", TEXT, " LetterKnitter", handler= menuhandler)
var("size", NUMBER, 70, 10, 200, handler= menuhandler)
var("stitches", NUMBER, 400, 10, 1000, handler=menuhandler)
 
def stitch(txt, x, y, n=1000):
    
    """ Stitches a given string of text (with n stitches).
    
    Creates a text path and finds n points on the path.
    Connects each consecutive point with a little curve.
    Sometimes connects to a random point on the path.
    
    """
    
    p = textpath(txt, x, y)
    pt0 = p.point(0)
    autoclosepath(False)
    beginpath(pt0.x, pt0.y)
    
    for i in range(int(n)):    
        t = float(i) / n
        pt1 = p.point(t)
        d = fontsize() * 0.05
        curveto(
            pt0.x, 
            pt1.y, 
            pt1.x + d, 
            pt0.y + d, 
            pt1.x, 
            pt1.y
        )
        
        if random() > 0.995:
            pti = p.point(random())
            curveto(
                pt0.x, 
                pt1.y + d*10, 
                pti.x + d, 
                pti.y + d, 
                pti.x, 
                pti.y
            )
            
        pt0.x = pt1.x
        pt0.y = pt1.y
 
    endpath()

def run(): 
    nofill()
    stroke(0.2)
    strokewidth(0.5)
    font(typeface, size)
    
    stitch(text, 50, 450, n=stitches)

run()

