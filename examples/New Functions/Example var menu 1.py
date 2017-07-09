# size(0,0)
background(0.7)

speed( 2 )

import itertools
import pprint


# Set the font and create the text path.
fonts = fontnames()

chars = (u"abcdefghijklmnopqrstuvwxyzäöüß"
         u"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ"
         u"!§$%&/()=¡“¶¢[]|{}≠»„‰¸˝ˇÁÛØ∏°ÅÍ™ÏÌÓıˆﬂŒÆ‡ÙÇ◊‹›˘˛÷—")

announcefont = "Chicago" if "Chicago" in fonts else "Helvetica"

randomfont = "--RANDOM FONT--"
fontMenu = [ randomfont ]
fontMenu.extend( fonts )
currentFont = randomfont


# cycle through chars again and again
zeichenquelle = itertools.cycle( chars )


def selectFont( fontname ):
    global currentFont
    currentFont = fontname

var("Font", MENU, default=selectFont, value=fontMenu)


def setup():
    background(0.7)


def box( b ):
    push()
    oldfill = fill( None )
    nofill()
    oldstrokewidth = strokewidth( 0.5 )
    oldstroke = stroke( 0 )
    x, y = b.origin.x, b.origin.y
    w, h = b.size.width, b.size.height
    rect( x,y,w,h)
    pop()
    fill( oldfill )
    strokewidth( oldstrokewidth )
    stroke( oldstroke )


def label( p, s ):
    push()
    fs = fontsize(9)
    f = font( "Geneva" )
    fl = fill( 0 )
    x, y, = p
    text( s, x+4,y-4 )

    pop()
    fontsize(fs)
    font( f )
    fill( fl )


def marker(p, style):
    push()
    oldfill = fill( None )
    nofill()
    r = 5
    if style == 1:
        fill(1,0,0, 0.6)
        r = 3
    d = 2 * r
    oldstrokewidth = strokewidth( 0.5 )
    oldstroke = stroke( 0 )
    x, y, = p
    oval( x-r, y-r, d, d )
    pop()
    fill( oldfill )
    strokewidth( oldstrokewidth )
    stroke( oldstroke )


def draw():
    background( 0.7 )
    
    if currentFont == randomfont:
        f = choice( fonts )
    else:
        f = currentFont
    char = zeichenquelle.next()
    fontsize( 750 )

    tp = textpath(char, 100, 850, width=WIDTH, font=f)
    fill(0.85,0.85,0.85, 0.5)
    stroke(0)
    strokewidth(0.5)
    drawpath( tp.copy() )
    fontsize(30)
    font( announcefont )
    s = u"%s  %s" % (char, f)
    fill(1)
    text(s, 10, 35, outline=False)
    print f

    # remember last point
    currentpoint = (0,0)

    # box around the char
    box( tp.bounds )
    idx = 0
    for segment in tp:
        p = (segment.x, segment.y)
        cmd = segment.cmd
        if cmd in (MOVETO, LINETO):
            # make a on-curve point
            marker(p,0)
        elif cmd == CURVETO:
            # make a on-curve point
            marker(p, 0)

            # make 2 of-curve points
            ctrl1 = (segment.ctrl1.x, segment.ctrl1.y)
            marker( ctrl1, 1)
            ctrl2 = (segment.ctrl2.x, segment.ctrl2.y)
            marker( ctrl2, 1)
            line(currentpoint[0], currentpoint[1],ctrl1[0], ctrl1[1])
            line(p[0], p[1],ctrl2[0], ctrl2[1])
        else:
            pass
        label( p, str(idx) )
        currentpoint = p
        idx += 1

