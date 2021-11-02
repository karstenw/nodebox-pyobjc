import pdb

import AppKit

from . import cocoa
graphics_impl = cocoa

BEVEL = cocoa.BEVEL
BOOLEAN = cocoa.BOOLEAN
BUTTON = cocoa.BUTTON
BUTT = cocoa.BUTT
BezierPath = cocoa.BezierPath
CENTER = cocoa.CENTER
CENTER = cocoa.CENTER
CLOSE = cocoa.CLOSE
CMYK = cocoa.CMYK
CORNER = cocoa.CORNER
CURVETO = cocoa.CURVETO
Canvas = cocoa.Canvas
ClippingPath = cocoa.ClippingPath
Color = cocoa.Color
DEFAULT_HEIGHT = cocoa.DEFAULT_HEIGHT
DEFAULT_WIDTH = cocoa.DEFAULT_WIDTH
Grob = cocoa.Grob
HSB = cocoa.HSB
Image = cocoa.Image
JUSTIFY = cocoa.JUSTIFY
LEFT = cocoa.LEFT
LINETO = cocoa.LINETO
MENU = cocoa.MENU
MITER = cocoa.MITER
MOVETO = cocoa.MOVETO
NORMAL = cocoa.NORMAL
FORTYFIVE = cocoa.FORTYFIVE
NUMBER = cocoa.NUMBER
NodeBoxError = cocoa.NodeBoxError
Oval = cocoa.Oval
PathElement = cocoa.PathElement
Point = cocoa.Point
RGB = cocoa.RGB
RIGHT = cocoa.RIGHT
ROUND = cocoa.ROUND
Rect = cocoa.Rect
SQUARE = cocoa.SQUARE
TEXT = cocoa.TEXT
Text = cocoa.Text
Transform = cocoa.Transform
Variable = cocoa.Variable
cm = cocoa.cm
inch = cocoa.inch
mm = cocoa.mm


# from nodebox.util import _copy_attr, _copy_attrs
import nodebox.util
_copy_attr = nodebox.util._copy_attr
_copy_attrs = nodebox.util._copy_attrs

import nodebox.geo

# add graphics commands from cocoa
__all__ = list(graphics_impl.__all__)
__all__.extend(['Context'])


# py3 stuff
py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int

class Context(object):
    
    KEY_UP = graphics_impl.KEY_UP
    KEY_DOWN = graphics_impl.KEY_DOWN
    KEY_LEFT = graphics_impl.KEY_LEFT
    KEY_RIGHT = graphics_impl.KEY_RIGHT
    KEY_BACKSPACE = graphics_impl.KEY_BACKSPACE
    KEY_TAB = graphics_impl.KEY_TAB
    KEY_ESC = graphics_impl.KEY_ESC

    NORMAL = graphics_impl.NORMAL
    FORTYFIVE = graphics_impl.FORTYFIVE


    def __init__(self, canvas=None, ns=None):

        """Initializes the context.
        
        Note that we have to give the namespace of the executing script, 
        which is a hack to keep the WIDTH and HEIGHT properties updated.
        Python's getattr only looks up property values once: at assign time."""

        if canvas is None:
            canvas = Canvas()
        if ns is None:
            ns = {}
        self.canvas = canvas
        self._ns = ns
        self._imagecache = {}
        self._vars = []
        self._resetContext()

    def _resetContext(self):
        self._outputmode = RGB
        self._colormode = RGB
        self._colorrange = 1.0
        self._fillcolor = self.Color()
        self._strokecolor = None
        self._strokewidth = 1.0
        self._capstyle = BUTT
        self._joinstyle = MITER
        self.canvas.background = self.Color(1.0)
        self._path = None
        self._autoclosepath = True
        self._transform = Transform()
        self._transformmode = CENTER
        self._transformstack = []
        self._fontname = "Helvetica"
        self._fontsize = 24
        self._lineheight = 1.2
        self._align = LEFT
        self._noImagesHint = False
        self._oldvars = self._vars
        self._vars = []

    def ximport(self, libName):
        
        lib = __import__(libName)
        self._ns[libName] = lib
        lib._ctx = self
        return lib
        
    ### Setup methods ###

    def size(self, width, height):
        if width == 0 and height == 0:
            # set to main screen size
            allsc = AppKit.NSScreen.screens()
            mainscreen = allsc[0]
            mainframe = mainscreen.frame()
            width = mainframe.size.width
            height = mainframe.size.height

        self.canvas.width = width
        self.canvas.height = height
        self._ns["WIDTH"] = width
        self._ns["HEIGHT"] = height

    def _get_width(self):
        return self.canvas.width

    WIDTH = property(_get_width)

    def _get_height(self):
        return self.canvas.height

    HEIGHT = property(_get_height)

    def speed(self, speed):
        self.canvas.speed = speed
        
    def background(self, *args):
        if len(args) > 0:
            if len(args) == 1 and args[0] is None:
                self.canvas.background = None
            else:
                self.canvas.background = self.Color(args)
        return self.canvas.background

    def outputmode(self, mode=None):
        if mode is not None:
            self._outputmode = mode
        return self._outputmode


    ### Variables ###

    def var(self, name, type,
            default=None, min=0, max=100, value=None,
            handler=None, menuitems=None):
        # pdb.set_trace()
        v = Variable(name, type, default, min, max, value, handler, menuitems)
        self.addvar(v)
        return v


    def addvar(self, v):
        oldvar = self.findvar(v.name)
        if oldvar is not None:
            if oldvar.compliesTo(v):
                v.value = oldvar.value
        self._vars.append(v)
        self._ns[v.name] = v.value

    def findvar(self, name):
        for v in self._oldvars:
            if v.name == name:
                return v
        return None


    ### Objects ####

    def _makeInstance(self, clazz, args, kwargs):
        """Creates an instance of a class defined in this document.        
           This method sets the context of the object to the current context."""
        inst = clazz(self, *args, **kwargs)
        return inst

    def BezierPath(self, *args, **kwargs):
        return self._makeInstance(BezierPath, args, kwargs)

    def ClippingPath(self, *args, **kwargs):
        return self._makeInstance(ClippingPath, args, kwargs)

    def Rect(self, *args, **kwargs):
        return self._makeInstance(Rect, args, kwargs)

    def Oval(self, *args, **kwargs):
        return self._makeInstance(Oval, args, kwargs)

    def Color(self, *args, **kwargs):
        return self._makeInstance(Color, args, kwargs)

    def Image(self, *args, **kwargs):
        # this creates a cocoa.Image instance. Devious.
        return self._makeInstance(Image, args, kwargs)

    def Text(self, *args, **kwargs):
        return self._makeInstance(Text, args, kwargs)


    ### Primitives ###

    def rect(self, x, y, width, height, roundness=0.0, draw=True, **kwargs):
        BezierPath.checkKwargs(kwargs)
        p = self.BezierPath(**kwargs)
        if roundness == 0:
            p.rect(x, y, width, height)
        else:
            curve = min(width*roundness, height*roundness)
            p.moveto(x, y+curve)
            p.curveto(x, y, x, y, x+curve, y)
            p.lineto(x+width-curve, y)
            p.curveto(x+width, y, x+width, y, x+width, y+curve)
            p.lineto(x+width, y+height-curve)
            p.curveto(x+width, y+height, x+width, y+height, x+width-curve, y+height)
            p.lineto(x+curve, y+height)
            p.curveto(x, y+height, x, y+height, x, y+height-curve)
            p.closepath()
        p.inheritFromContext(kwargs.keys())

        if draw:
            p.draw()
        return p

    def oval(self, x, y, width, height, draw=True, **kwargs):
        BezierPath.checkKwargs(kwargs)
        path = self.BezierPath(**kwargs)
        path.oval(x, y, width, height)
        path.inheritFromContext(kwargs.keys())

        if draw:
            path.draw()
        return path

    ellipse = oval


    def circle(self, cx, cy, rx, ry=None, draw=True, **kwargs):
        if ry == None:
            ry = rx
        width = 2 * rx
        height = 2 * ry
        x = cx - rx
        y = cy - ry
        return self.oval( x, y, width, height, draw=draw, **kwargs )


    def arc(self, x, y, r, startAngle, endAngle, draw=True, **kwargs):
        BezierPath.checkKwargs(kwargs)
        path = self.BezierPath(**kwargs)
        path.arc(x, y, r, startAngle, endAngle)
        path.inheritFromContext(kwargs.keys())
        if draw:
            path.draw()
        return path

    def line(self, x1, y1, x2, y2, draw=True, **kwargs):
        BezierPath.checkKwargs(kwargs)
        p = self.BezierPath(**kwargs)
        p.line(x1, y1, x2, y2)
        p.inheritFromContext(kwargs.keys())
        if draw:
            p.draw()
        return p

    def star(self, startx, starty, points=20, outer= 100, inner = 50, draw=True, **kwargs):
        BezierPath.checkKwargs(kwargs)
        from math import sin, cos, pi

        p = self.BezierPath(**kwargs)
        p.moveto(startx, starty + outer)

        for i in range(1, int(2 * points)):
            angle = i * pi / points
            x = sin(angle)
            y = cos(angle)
            if i % 2:
                radius = inner
            else:
                radius = outer
            x = startx + radius * x
            y = starty + radius * y
            p.lineto(x,y)

        p.closepath()
        p.inheritFromContext(kwargs.keys())
        if draw:
            p.draw()
        return p


    # a working arrow implementation shold be here



    def arrow(self, x, y, width=100, type=NORMAL, draw=True, **kwargs):

        """Draws an arrow.

        Draws an arrow at position x, y, with a default width of 100.
        There are two different types of arrows: NORMAL and trendy FORTYFIVE
        degrees arrows.  When draw=False then the arrow's path is not ended,
        similar to endpath(draw=False)."""

        BezierPath.checkKwargs(kwargs)
        if type==NORMAL:
            return self._arrow(x, y, width, draw, **kwargs)
        elif type==FORTYFIVE:
            return self._arrow45(x, y, width, draw, **kwargs)
        else:
            raise NodeBoxError( "arrow: available types for arrow() "
                                "are NORMAL and FORTYFIVE\n")

    def _arrow(self, x, y, width, draw, **kwargs):

        head = width * .4
        tail = width * .2

        p = self.BezierPath(**kwargs)
        p.moveto(x, y)
        p.lineto(x-head, y+head)
        p.lineto(x-head, y+tail)
        p.lineto(x-width, y+tail)
        p.lineto(x-width, y-tail)
        p.lineto(x-head, y-tail)
        p.lineto(x-head, y-head)
        p.lineto(x, y)
        p.closepath()
        p.inheritFromContext(kwargs.keys())
        if draw:
            p.draw()
        return p

    def _arrow45(self, x, y, width, draw, **kwargs):

        head = .3
        tail = 1 + head

        p = self.BezierPath(**kwargs)
        p.moveto(x, y)
        p.lineto(x, y+width*(1-head))
        p.lineto(x-width*head, y+width)
        p.lineto(x-width*head, y+width*tail*.4)
        p.lineto(x-width*tail*.6, y+width)
        p.lineto(x-width, y+width*tail*.6)
        p.lineto(x-width*tail*.4, y+width*head)
        p.lineto(x-width, y+width*head)
        p.lineto(x-width*(1-head), y)
        p.lineto(x, y)
        p.inheritFromContext(kwargs.keys())
        if draw:
            p.draw()
        return p


    ### Path Commands ###

    def beginpath(self, x=None, y=None):
        self._path = self.BezierPath()
        self._pathclosed = False
        if x != None and y != None:
            self._path.moveto(x,y)

    def moveto(self, x, y):
        if self._path is None:
            raise NodeBoxError("No current path. Use beginpath() first.")
        self._path.moveto(x,y)

    def lineto(self, x, y):
        if self._path is None:
            raise NodeBoxError("No current path. Use beginpath() first.")
        self._path.lineto(x, y)

    def curveto(self, x1, y1, x2, y2, x3, y3):
        if self._path is None:
            raise(NodeBoxError, "No current path. Use beginpath() first.")
        self._path.curveto(x1, y1, x2, y2, x3, y3)

    def closepath(self):
        if self._path is None:
            raise NodeBoxError("No current path. Use beginpath() first.")
        if not self._pathclosed:
            self._path.closepath()

    def endpath(self, draw=True):
        if self._path is None:
            raise NodeBoxError("No current path. Use beginpath() first.")
        if self._autoclosepath:
            self.closepath()
        p = self._path
        p.inheritFromContext()
        if draw:
            p.draw()
        self._path = None
        self._pathclosed = False
        return p

    def drawpath(self, path, **kwargs):
        BezierPath.checkKwargs(kwargs)
        if isinstance(path, (list, tuple)):
            path = self.BezierPath(path, **kwargs)
        else: # Set the values in the current bezier path with the kwargs
            for arg_key, arg_val in kwargs.items():
                setattr(path, arg_key, _copy_attr(arg_val))
        path.inheritFromContext(kwargs.keys())
        path.draw()

    def autoclosepath(self, close=True):
        self._autoclosepath = close

    def findpath(self, points, curvature=1.0):
        from . import bezier
        path = bezier.findpath(points, curvature=curvature)
        path._ctx = self
        path.inheritFromContext()
        return path


    ### Clipping Commands ###

    def beginclip(self, path):
        cp = self.ClippingPath(path)
        self.canvas.push(cp)
        return cp

    def endclip(self):
        self.canvas.pop()


    ### Transformation Commands ###

    def push(self): #, all=False):
        top = (self._transform.matrix,)
        if False: # all:
            top = (self._align, self._autoclosepath, self._capstyle, self._colormode,
                   self._fillcolor, self._fontname, self._fontsize, self._joinstyle,
                   self._lineheight, self._outputmode, self._strokecolor,
                   self._strokewidth, self._transformmode, self._transform.matrix)
        self._transformstack.append(top)

    def pop(self):
        try:
            top = self._transformstack.pop()
        except IndexError as e:
            raise NodeBoxError( "pop: too many pops!" )
        if len(top) > 1:
            self._align, self._autoclosepath, self._capstyle, self._colormode,
            self._fillcolor, self._fontname, self._fontsize, self._joinstyle,
            self._lineheight, self._outputmode, self._strokecolor,
            self._strokewidth, self._transformmode, self._transform.matrix = top
        else:
            self._transform.matrix = top[0]

    def transform(self, mode=None):
        if mode is not None:
            self._transformmode = mode
        return self._transformmode
        
    def translate(self, x, y):
        self._transform.translate(x, y)
        
    def reset(self):
        self._transform = Transform()

    def rotate(self, degrees=0, radians=0):
        self._transform.rotate(-degrees,-radians)

    def translate(self, x=0, y=0):
        self._transform.translate(x,y)

    def scale(self, x=1, y=None):
        self._transform.scale(x,y)

    def skew(self, x=0, y=0):
        self._transform.skew(x,y)


    ### Color Commands ###

    color = Color

    def colormode(self, mode=None, range=None):
        if mode is not None:
            self._colormode = mode
        if range is not None:
            self._colorrange = float(range)
        return self._colormode

    def colorrange(self, range=None):
        if range is not None:
            self._colorrange = float(range)
        return self._colorrange

    def nofill(self):
        self._fillcolor = None

    def fill(self, *args):
        if len(args) > 0:
            self._fillcolor = self.Color(*args)
        return self._fillcolor

    def nostroke(self):
        self._strokecolor = None

    def stroke(self, *args):
        if len(args) > 0:
            self._strokecolor = self.Color(*args)
        return self._strokecolor

    def strokewidth(self, width=None):
        if width is not None:
            self._strokewidth = max(width, 0.0001)
        return self._strokewidth
        
    def capstyle(self, style=None):
        if style is not None:
            if style not in (BUTT, ROUND, SQUARE):
                raise NodeBoxError( 'Line cap style should be BUTT,'
                                    ' ROUND or SQUARE.')
            self._capstyle = style
        return self._capstyle

    def joinstyle(self, style=None):
        if style is not None:
            if style not in (MITER, ROUND, BEVEL):
                raise NodeBoxError( 'Line join style should be MITER,'
                                    ' ROUND or BEVEL.')
            self._joinstyle = style
        return self._joinstyle


    ### Font Commands ###

    def font(self, fontname=None, fontsize = None):
        if fontname is not None:
            if not Text.font_exists(fontname):
                raise NodeBoxError('Font "%s" not found.' % fontname )
            else:
                self._fontname = fontname
        if fontsize is not None:
            self._fontsize = fontsize
        return self._fontname

    def fontsize(self, fontsize=None):
        if fontsize is not None:
            self._fontsize = fontsize
        return self._fontsize

    def lineheight(self, lineheight=None):
        if lineheight is not None:
            self._lineheight = max(lineheight, 0.01)
        return self._lineheight

    def align(self, align=None):
        if align is not None:
            self._align = align
        return self._align

    def textwidth(self, txt, width=None, **kwargs):
        """Calculates the width of a single-line string."""
        return self.textmetrics(txt, width, **kwargs)[0]

    def textheight(self, txt, width=None, **kwargs):
        """Calculates the height of a (probably) multi-line string."""
        return self.textmetrics(txt, width, **kwargs)[1]

    def text(self, txt, x, y, width=None, height=None, outline=False, draw=True, **kwargs):
        Text.checkKwargs(kwargs)
        txt = self.Text(txt, x, y, width, height, **kwargs)
        txt.inheritFromContext(kwargs.keys())
        if outline:
            path = txt.path
            if draw:
                path.draw()
            return path
        else:
            if draw:
                txt.draw()
            return txt

    def textpath(self, txt, x, y, width=None, height=None, **kwargs):
        # pdb.set_trace()
        Text.checkKwargs(kwargs)
        txt = self.Text(txt, x, y, width, height, **kwargs)
        txt.inheritFromContext( list( kwargs.keys()) )
        return txt.path

    def textmetrics(self, txt, width=None, height=None, **kwargs):
        txt = self.Text(txt, 0, 0, width, height, **kwargs)
        txt.inheritFromContext(kwargs.keys())
        return txt.metrics

    def alltextmetrics(self, txt, width=None, height=None, **kwargs):
        txt = self.Text(txt, 0, 0, width, height, **kwargs)
        txt.inheritFromContext(kwargs.keys())
        return txt.allmetrics


    ### Image commands ###

    def image(self, path, x, y, width=None, height=None, alpha=1.0,
                    data=None, draw=True, **kwargs):
        img = self.Image(path, x, y, width, height, alpha, data=data, **kwargs)
        img.inheritFromContext( kwargs.keys() )
        if draw:
            img.draw()
        return img

    def imagesize(self, path, data=None):
        img = self.Image(path, data=data)
        return img.size
        
    ### Canvas proxy ###

    def save(self, fname, format=None):
        self.canvas.save(fname, format)


    ## cGeo

    def isqrt( self, v):
        return nodebox.geo.isqrt( v )

    def angle(self, x0, y0, x1, y1):
        return nodebox.geo.angle( x0, y0, x1, y1)

    def distance(self, x0, y0, x1, y1):
        return nodebox.geo.distance( x0, y0, x1, y1)

    def coordinates(self, x0, y0, distance, angle):
        return nodebox.geo.coordinates(x0, y0, distance, angle)

    def reflect(self, x0, y0, x1, y1, d=1.0, a=180):
        return nodebox.geo.reflect(x0, y0, x1, y1, d, a)

    ## 

    def dither(self, imagebytes, w, h, typ, threshhold):
        return nodebox.geo.dither(imagebytes, w, h, typ, threshhold)

    ## 

    def fractalimage( self, clut, w,h,iterations,x1,y1,dx,dy,nreal,nimag,limit):
        return nodebox.geo.fractalimage(clut, w,h,iterations,x1,y1,
                                            dx,dy,nreal,nimag,limit)

