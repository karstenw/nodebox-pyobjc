import os
import warnings

# from random import choice, shuffle
import random
choice = random.choice
shuffle = random.shuffle

import objc
super = objc.super

# import pdb

# from AppKit import *
import AppKit
NSBezierPath = AppKit.NSBezierPath
NSColor = AppKit.NSColor
NSGraphicsContext = AppKit.NSGraphicsContext

NSView = AppKit.NSView

NSDeviceCMYKColorSpace = AppKit.NSDeviceCMYKColorSpace
NSDeviceRGBColorSpace = AppKit.NSDeviceRGBColorSpace
NSAffineTransform = AppKit.NSAffineTransform
NSImage = AppKit.NSImage
NSImageCacheNever = AppKit.NSImageCacheNever
NSCompositeSourceOver = AppKit.NSCompositeSourceOver
NSLeftTextAlignment = AppKit.NSLeftTextAlignment
NSFont = AppKit.NSFont
NSMutableParagraphStyle = AppKit.NSMutableParagraphStyle
NSLineBreakByWordWrapping = AppKit.NSLineBreakByWordWrapping
NSParagraphStyleAttributeName = AppKit.NSParagraphStyleAttributeName
NSForegroundColorAttributeName = AppKit.NSForegroundColorAttributeName
NSFontAttributeName = AppKit.NSFontAttributeName
NSTextStorage = AppKit.NSTextStorage
NSLayoutManager = AppKit.NSLayoutManager
NSTextContainer = AppKit.NSTextContainer
NSRectFillUsingOperation = AppKit.NSRectFillUsingOperation
NSGIFFileType = AppKit.NSGIFFileType
NSJPEGFileType = AppKit.NSJPEGFileType
NSJPEGFileType = AppKit.NSJPEGFileType
NSPNGFileType = AppKit.NSPNGFileType
NSTIFFFileType = AppKit.NSTIFFFileType
NSBitmapImageRep = AppKit.NSBitmapImageRep
NSString = AppKit.NSString
NSData = AppKit.NSData
NSAffineTransformStruct = AppKit.NSAffineTransformStruct


import nodebox.util
_copy_attr = nodebox.util._copy_attr
_copy_attrs = nodebox.util._copy_attrs
makeunicode = nodebox.util.makeunicode


try:
    import cPolymagic
except ImportError as e:
    warnings.warn('Could not load cPolymagic: %s' % e)

__all__ = [
        "DEFAULT_WIDTH", "DEFAULT_HEIGHT",
        "inch", "cm", "mm",
        "RGB", "HSB", "CMYK",
        "CENTER", "CORNER",
        "MOVETO", "LINETO", "CURVETO", "CLOSE",
        "MITER", "ROUND", "BEVEL", "BUTT", "SQUARE",
        "LEFT", "RIGHT", "CENTER", "JUSTIFY",
        "NORMAL","FORTYFIVE",
        "NUMBER", "TEXT", "BOOLEAN","BUTTON", "MENU",
        "NodeBoxError",
        "Point", "Grob", "BezierPath", "PathElement", "ClippingPath", "Rect",
        "Oval",
        "Color", "Transform", "Image", "Text",
        "Variable", "Canvas",
        ]

DEFAULT_WIDTH, DEFAULT_HEIGHT = 1000, 1000

# unused
inch = 72.0
cm = inch / 2.54
mm = cm * 10.0


RGB = "rgb"
HSB = "hsb"
CMYK = "cmyk"


MOVETO = AppKit.NSMoveToBezierPathElement
LINETO = AppKit.NSLineToBezierPathElement
CURVETO = AppKit.NSCurveToBezierPathElement
CLOSE = AppKit.NSClosePathBezierPathElement

MITER = AppKit.NSMiterLineJoinStyle
ROUND = AppKit.NSRoundLineJoinStyle # Also used for NSRoundLineCapStyle, same value.
BEVEL = AppKit.NSBevelLineJoinStyle
BUTT = AppKit.NSButtLineCapStyle
SQUARE = AppKit.NSSquareLineCapStyle

LEFT = AppKit.NSLeftTextAlignment
RIGHT = AppKit.NSRightTextAlignment
CENTER = AppKit.NSCenterTextAlignment
JUSTIFY = AppKit.NSJustifiedTextAlignment

# don't want to override justification.CENTER
# CENTER = "center"
CORNER = 4 #"corner"


NORMAL=1
FORTYFIVE=2

NUMBER = 1
TEXT = 2
BOOLEAN = 3
BUTTON = 4
MENU = 5

KEY_UP = 126
KEY_DOWN = 125
KEY_LEFT = 123
KEY_RIGHT = 124
KEY_BACKSPACE = 51
KEY_TAB = 48
KEY_ESC = 53

KEY_ENTER = 76
KEY_RETURN = 36
KEY_SPACE = 49


_STATE_NAMES = {
    '_outputmode':    'outputmode',
    '_colorrange':    'colorrange',
    '_fillcolor':     'fill',
    '_strokecolor':   'stroke',
    '_strokewidth':   'strokewidth',
    '_capstyle':      'capstyle',
    '_joinstyle':     'joinstyle',
    '_transform':     'transform',
    '_transformmode': 'transformmode',
    '_fontname':      'font',
    '_fontsize':      'fontsize',
    '_align':         'align',
    '_lineheight':    'lineheight',
}


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

def _save():
    NSGraphicsContext.currentContext().saveGraphicsState()


def _restore():
    NSGraphicsContext.currentContext().restoreGraphicsState()


class NodeBoxError(Exception):
    pass


class Point(object):

    def __init__(self, *args):
        if len(args) == 2:
            self.x, self.y = args
        elif len(args) == 1:
            self.x, self.y = args[0]
        elif len(args) == 0:
            self.x = self.y = 0.0
        else:
            raise NodeBoxError("Wrong initializer for Point object")

    def __repr__(self):
        return "Point(x=%.3f, y=%.3f)" % (self.x, self.y)
        
    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return (self.x < other.x) and (self.y < other.y)

    def __le__(self, other):
        return (self.x <= other.x) and (self.y <= other.y)

    def __gt__(self, other):
        return (self.x > other.x) and (self.y > other.y)

    def __ge__(self, other):
        return (self.x >= other.x) and (self.y >= other.y)

    def __hash__( self ):
        return hash( (self.x, self.y) )


class Grob(object):
    """A GRaphic OBject is the base class for all DrawingPrimitives."""

    def __init__(self, ctx):
        """Initializes this object with the current context."""
        self._ctx = ctx

    def draw(self):
        """Appends the grob to the canvas.
           This will result in a draw later on, when the scene graph is rendered."""
        self._ctx.canvas.append(self)
        
    def copy(self):
        """Returns a deep copy of this grob."""
        raise NotImplementedError("Copy is not implemented on this Grob class.")
        
    def inheritFromContext(self, ignore=()):
        attrs_to_copy = list(self.__class__.stateAttributes)
        [attrs_to_copy.remove(k) for k, v in _STATE_NAMES.items() if v in ignore]
        _copy_attrs(self._ctx, self, attrs_to_copy)
        
    def checkKwargs(self, kwargs):
        remaining = [arg for arg in kwargs.keys() if arg not in self.kwargs]
        if remaining:
            err = "Unknown argument(s) '%s'" % ", ".join(remaining)
            raise NodeBoxError(err)
    checkKwargs = classmethod(checkKwargs)


class TransformMixin(object):

    """Mixin class for transformation support.
    Adds the _transform and _transformmode attributes to the class."""
    
    def __init__(self):
        self._reset()
        
    def _reset(self):
        self._transform = Transform()
        self._transformmode = CENTER
        
    def _get_transform(self):
        return self._transform
    def _set_transform(self, transform):
        self._transform = Transform(transform)
    transform = property(_get_transform, _set_transform)

    def _get_transformmode(self):
        return self._transformmode
    def _set_transformmode(self, mode):
        self._transformmode = mode
    transformmode = property(_get_transformmode, _set_transformmode)
        
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
        
class ColorMixin(object):
    
    """Mixin class for color support.
    Adds the _fillcolor, _strokecolor and _strokewidth attributes to the class."""

    def __init__(self, **kwargs):
        try:
            self._fillcolor = Color(self._ctx, kwargs['fill'])
        except KeyError:
            self._fillcolor = Color(self._ctx)
        try:
            self._strokecolor = Color(self._ctx, kwargs['stroke'])
        except KeyError:
            self._strokecolor = None
        self._strokewidth = kwargs.get('strokewidth', 1.0)
        
    def _get_fill(self):
        return self._fillcolor
    def _set_fill(self, *args):
        self._fillcolor = Color(self._ctx, *args)
    fill = property(_get_fill, _set_fill)

    def _get_stroke(self):
        return self._strokecolor
    def _set_stroke(self, *args):
        self._strokecolor = Color(self._ctx, *args)
    stroke = property(_get_stroke, _set_stroke)

    def _get_strokewidth(self):
        return self._strokewidth
    def _set_strokewidth(self, strokewidth):
        self._strokewidth = max(strokewidth, 0.0001)
    strokewidth = property(_get_strokewidth, _set_strokewidth)

class BezierPath(Grob, TransformMixin, ColorMixin):
    """A BezierPath provides a wrapper around NSBezierPath."""
    
    stateAttributes = ('_fillcolor', '_strokecolor', '_strokewidth', '_capstyle',
                       '_joinstyle', '_transform', '_transformmode')
    kwargs = ('fill', 'stroke', 'strokewidth', 'capstyle', 'joinstyle')

    def __init__(self, ctx, path=None, **kwargs):
        super(BezierPath, self).__init__(ctx)
        TransformMixin.__init__(self)
        ColorMixin.__init__(self, **kwargs)
        self.capstyle = kwargs.get('capstyle', BUTT)
        self.joinstyle = kwargs.get('joinstyle', MITER)
        self._segment_cache = None
        if path is None:
            self._nsBezierPath = NSBezierPath.bezierPath()
        elif isinstance(path, (list,tuple)):
            self._nsBezierPath = NSBezierPath.bezierPath()
            self.extend(path)
        elif isinstance(path, BezierPath):
            self._nsBezierPath = path._nsBezierPath.copy()
            _copy_attrs(path, self, self.stateAttributes)
        elif isinstance(path, NSBezierPath):
            self._nsBezierPath = path
        else:
            raise NodeBoxError("Don't know what to do with %s." % path)
            
    def _get_path(self):
        s = "The 'path' attribute is deprecated. Please use _nsBezierPath instead."
        warnings.warn(s, DeprecationWarning, stacklevel=2)
        return self._nsBezierPath
    path = property(_get_path)

    def copy(self):
        return self.__class__(self._ctx, self)

    ### Cap and Join style ###

    def _get_capstyle(self):
        return self._capstyle
    def _set_capstyle(self, style):
        if style not in (BUTT, ROUND, SQUARE):
            raise NodeBoxError('Line cap style should be BUTT, ROUND or SQUARE.')
        self._capstyle = style
    capstyle = property(_get_capstyle, _set_capstyle)

    def _get_joinstyle(self):
        return self._joinstyle
    def _set_joinstyle(self, style):
        if style not in (MITER, ROUND, BEVEL):
            raise NodeBoxError('Line join style should be MITER, ROUND or BEVEL.')
        self._joinstyle = style
    joinstyle = property(_get_joinstyle, _set_joinstyle)

    ### Path methods ###

    def moveto(self, x, y):
        self._segment_cache = None
        self._nsBezierPath.moveToPoint_( (x, y) )

    def lineto(self, x, y):
        self._segment_cache = None
        self._nsBezierPath.lineToPoint_( (x, y) )

    def curveto(self, x1, y1, x2, y2, x3, y3):
        self._segment_cache = None
        self._nsBezierPath.curveToPoint_controlPoint1_controlPoint2_(
                                                (x3, y3), (x1, y1), (x2, y2) )

    # relativeMoveToPoint_( NSPoint )
    # relativeLineToPoint_( NSPoint )
    # relativeCurveToPoint:(NSPoint)aPoint
    #           controlPoint1:(NSPoint)controlPoint1
    #           controlPoint2:(NSPoint)controlPoint2
    # appendBezierPathWithOvalInRect_
    # appendBezierPathWithArcFromPoint_(NSPoint)fromPoint
    #                          toPoint_(NSPoint)toPoint
    #                           radius_(CGFloat)radius
    # appendBezierPathWithArcWithCenter:(NSPoint)center
    #                            radius:(CGFloat)radius
    #                        startAngle:(CGFloat)startAngle
    #                          endAngle:(CGFloat)endAngle
    # appendBezierPathWithArcWithCenter:(NSPoint)center
    #                            radius:(CGFloat)radius
    #                        startAngle:(CGFloat)startAngle
    #                          endAngle:(CGFloat)endAngle
    #                         clockwise:(BOOL)clockwise

    def closepath(self):
        self._segment_cache = None
        self._nsBezierPath.closePath()
        
    def setlinewidth(self, width):
        self.linewidth = width

    def _get_bounds(self):
        try:
            if self._nsBezierPath.isEmpty():
                return (0,0) , (0,0)
        except Exception as err:
            print()
            #pdb.set_trace()
            print(err)
            print()
        try:
            cgr = self._nsBezierPath.bounds()
            xy = cgr.origin
            wh = cgr.size
            result = (xy,wh)
            return result
        #try:
        #    return self._nsBezierPath.bounds()
        #except :
        #    # Path is empty -- no bounds
        #    return (0,0) , (0,0)
        except Exception as err:
            print()
            #pdb.set_trace()
            print("Bezierpath._get_bounds() FAILED")
            print(err)
            print()
        return (0,0) , (0,0)

    bounds = property(_get_bounds)

    def contains(self, x, y):
        return self._nsBezierPath.containsPoint_((x,y))

    ### Basic shapes ###

    def rect(self, x, y, width, height):
        self._segment_cache = None
        self._nsBezierPath.appendBezierPathWithRect_( ((x, y),
                                                       (width, height)) )
        
    def oval(self, x, y, width, height):
        self._segment_cache = None
        self._nsBezierPath.appendBezierPathWithOvalInRect_( ((x, y),
                                                             (width, height)) )
    ellipse = oval

    def arc(self, x, y, r, startAngle, endAngle):
        self._segment_cache = None
        self._nsBezierPath.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_(
                                        (x,y), r, startAngle, endAngle)
        
    def line(self, x1, y1, x2, y2):
        self._segment_cache = None
        self._nsBezierPath.moveToPoint_( (x1, y1) )
        self._nsBezierPath.lineToPoint_( (x2, y2) )

    ### List methods ###

    def __getitem__(self, index):
        cmd, el = self._nsBezierPath.elementAtIndex_associatedPoints_(index)
        return PathElement(cmd, el)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        return self._nsBezierPath.elementCount()

    def extend(self, pathElements):
        self._segment_cache = None
        for el in pathElements:
            if isinstance(el, (list, tuple)):
                x, y = el
                if len(self) == 0:
                    cmd = MOVETO
                else:
                    cmd = LINETO
                self.append(PathElement(cmd, ((x, y),)))
            elif isinstance(el, PathElement):
                self.append(el)
            else:
                raise NodeBoxError("Don't know how to handle %s" % el)

    def append(self, el):
        self._segment_cache = None
        if el.cmd == MOVETO:
            self.moveto(el.x, el.y)
        elif el.cmd == LINETO:
            self.lineto(el.x, el.y)
        elif el.cmd == CURVETO:
            self.curveto(el.ctrl1.x, el.ctrl1.y, el.ctrl2.x, el.ctrl2.y, el.x, el.y)
        elif el.cmd == CLOSE:
            self.closepath()
            
    def _get_contours(self):
        from . import bezier
        return bezier.contours(self)
    contours = property(_get_contours)

    ### Drawing methods ###

    def _get_transform(self):
        trans = self._transform.copy()
        if (self._transformmode == CENTER):
            try:
                (x, y), (w, h) = self.bounds
            except Exception as err:
                print()
                # pdb.set_trace()
                print(err)
                print
            deltax = x + w / 2
            deltay = y + h / 2
            t = Transform()
            t.translate(-deltax,-deltay)
            trans.prepend(t)
            t = Transform()
            t.translate(deltax,deltay)
            trans.append(t)
        return trans
    transform = property(_get_transform)

    def _draw(self):
        _save()
        self.transform.concat()
        if (self._fillcolor):
            self._fillcolor.set()
            self._nsBezierPath.fill()
        if (self._strokecolor):
            self._strokecolor.set()
            self._nsBezierPath.setLineWidth_(self._strokewidth)
            self._nsBezierPath.setLineCapStyle_(self._capstyle)
            self._nsBezierPath.setLineJoinStyle_(self._joinstyle)
            self._nsBezierPath.stroke()
        _restore()

    ### Geometry ###

    def fit(self, x=None, y=None, width=None, height=None, stretch=False):

        """Fits this path to the specified bounds.
        
        All parameters are optional; if no parameters are specified,
        nothing will happen. Specifying a parameter will constrain its value:
        
        - x: The path will be positioned at the specified x value 
        - y: The path will be positioned at the specified y value 
        - width: The path will be of the specified width
        - height: The path will be of the specified height
        - stretch: If both width and height are defined, either stretch the path or
                   keep the aspect ratio.
        """

        # (px, py), (pw, ph) = self.bounds
        try:
            (px, py), (pw, ph) = self.bounds
        except Exception as err:
            print()
            print("BezierPath.fit() FAILED.")
            # pdb.set_trace()
            print(err)
            print

        t = Transform()
        if x is not None and y is None:
            t.translate(x, py)
        elif x is None and y is not None:
            t.translate(px, y)
        elif x is not None and y is not None:
            t.translate(x, y)
        else:
            t.translate(px, py)
        if width is not None and height is None:
            t.scale(width / pw)
        elif width is None and height is not None:
            t.scale(height / ph)
        elif width is not None and height is not None:
            if stretch:
                t.scale(width /pw, height / ph)
            else:
                t.scale(min(width /pw, height / ph))
        t.translate(-px, -py)
        self._nsBezierPath = t.transformBezierPath(self)._nsBezierPath

    ### Mathematics ###

    def segmentlengths(self, relative=False, n=10):
        # import bezier
        
        from . import bezier
        if relative: # Use the opportunity to store the segment cache.
            if self._segment_cache is None:
                self._segment_cache = bezier.segment_lengths(self,
                                                            relative=True, n=n)
            return self._segment_cache
        else:
            return bezier.segment_lengths(self, relative=False, n=n)

    def _get_length(self, segmented=False, n=10):
        # import bezier
        from . import bezier
        return bezier.length(self, segmented=segmented, n=n)
    length = property(_get_length)
        
    def point(self, t):
        # import bezier
        from . import bezier
        return bezier.point(self, t)
        
    def points(self, amount=100):
        from . import bezier
        if len(self) == 0:
            raise NodeBoxError("The given path is empty")

        # The delta value is divided by amount - 1, because we also want the
        # last point (t=1.0)
        # If I wouldn't use amount - 1, I fall one point short of the end.
        # E.g. if amount = 4, I want point at t 0.0, 0.33, 0.66 and 1.0,
        # if amount = 2, I want point at t 0.0 and t 1.0
        
        amount = int( amount )
        try:
            delta = 1.0 / (amount-1)
        except ZeroDivisionError:
            delta = 1.0

        for i in range(amount):
            yield self.point( delta*i )
            
    def addpoint(self, t):
        # import bezier
        from . import bezier
        self._nsBezierPath = bezier.insert_point(self, t)._nsBezierPath
        self._segment_cache = None

    ### Clipping operations ###

    def intersects(self, other):
        return cPolymagic.intersects(self._nsBezierPath, other._nsBezierPath)
        
    def union(self, other, flatness=0.6):
        return BezierPath(self._ctx, cPolymagic.union(self._nsBezierPath,
                                                    other._nsBezierPath, flatness))

    def intersect(self, other, flatness=0.6):
        return BezierPath(self._ctx, cPolymagic.intersect(self._nsBezierPath,
                                                    other._nsBezierPath, flatness))

    def difference(self, other, flatness=0.6):
        return BezierPath(self._ctx, cPolymagic.difference(self._nsBezierPath,
                                                    other._nsBezierPath, flatness))

    def xor(self, other, flatness=0.6):
        return BezierPath(self._ctx, cPolymagic.xor(self._nsBezierPath,
                                                    other._nsBezierPath, flatness))


class PathElement(object):

    def __init__(self, cmd=None, pts=None):
        self.cmd = cmd
        if cmd == MOVETO:
            assert len(pts) == 1
            self.x, self.y = pts[0]
            self.ctrl1 = Point(pts[0])
            self.ctrl2 = Point(pts[0])
        elif cmd == LINETO:
            assert len(pts) == 1
            self.x, self.y = pts[0]
            self.ctrl1 = Point(pts[0])
            self.ctrl2 = Point(pts[0])
        elif cmd == CURVETO:
            assert len(pts) == 3
            self.ctrl1 = Point(pts[0])
            self.ctrl2 = Point(pts[1])
            self.x, self.y = pts[2]
        elif cmd == CLOSE:
            assert pts is None or len(pts) == 0
            self.x = self.y = 0.0
            self.ctrl1 = Point(0.0, 0.0)
            self.ctrl2 = Point(0.0, 0.0)
        else:
            self.x = self.y = 0.0
            self.ctrl1 = Point()
            self.ctrl2 = Point()

    def __repr__(self):
        if self.cmd == MOVETO:
            return "PathElement(MOVETO, ((%.3f, %.3f),))" % (self.x, self.y)
        elif self.cmd == LINETO:
            return "PathElement(LINETO, ((%.3f, %.3f),))" % (self.x, self.y)
        elif self.cmd == CURVETO:
            s = "PathElement(CURVETO, ((%.3f, %.3f), (%.3f, %.3f), (%.3f, %.3f))"
            return s % (self.ctrl1.x, self.ctrl1.y,
                        self.ctrl2.x, self.ctrl2.y,
                        self.x, self.y)
        elif self.cmd == CLOSE:
            return "PathElement(CLOSE)"
            
    def __eq__(self, other):
        if other is None:
            return False
        if self.cmd != other.cmd:
            return False
        return (    self.x == other.x and self.y == other.y
                and self.ctrl1 == other.ctrl1 and self.ctrl2 == other.ctrl2 )
        
    def __lt__(self, other):
        return (    (self.x < other.x) and (self.y < other.y)
                and (self.ctrl1 < other.ctrl1) and (self.ctrl2 < other.ctrl2) )

    def __le__(self, other):
        return (    (self.x <= other.x) and (self.y <= other.y)
                and (self.ctrl1 <= other.ctrl1) and (self.ctrl2 <= other.ctrl2) )

    def __gt__(self, other):
        return (    (self.x > other.x) and (self.y > other.y)
                and (self.ctrl1 > other.ctrl1) and (self.ctrl2 > other.ctrl2) )

    def __ge__(self, other):
        return (    (self.x >= other.x) and (self.y >= other.y)
                and (self.ctrl1 >= other.ctrl1) and (self.ctrl2 >= other.ctrl2) ) 


    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash( (self.x, self.y, self.ctrl1, self.ctrl2) )


class ClippingPath(Grob):

    def __init__(self, ctx, path):
        self._ctx = ctx
        self.path = path
        self._grobs = []
        
    def append(self, grob):
        self._grobs.append(grob)
        
    def _draw(self):
        _save()
        cp = self.path.transform.transformBezierPath(self.path)
        cp._nsBezierPath.addClip()
        for grob in self._grobs:
            grob._draw()
        _restore()


class Rect(BezierPath):

    def __init__(self, ctx, x, y, width, height, **kwargs):
        warnings.warn("Rect is deprecated. Use BezierPath's rect method.",
                                            DeprecationWarning, stacklevel=2)
        r = (x,y), (width,height)
        super(Rect, self).__init__(ctx, NSBezierPath.bezierPathWithRect_(r),
                                        **kwargs)

    def copy(self):
        raise NotImplementedError("Please don't use Rect anymore")


class Oval(BezierPath):

    def __init__(self, ctx, x, y, width, height, **kwargs):
        warnings.warn("Oval is deprecated. Use BezierPath's oval method.",
                      DeprecationWarning, stacklevel=2)
        r = (x,y), (width,height)
        super(Oval, self).__init__(ctx, NSBezierPath.bezierPathWithOvalInRect_(r),
                                        **kwargs)

    def copy(self):
        raise NotImplementedError("Please don't use Oval anymore")


class Color(object):

    def __init__(self, ctx, *args):
        self._ctx = ctx
        params = len(args)

        # Decompose the arguments into tuples. 
        if params == 1 and isinstance(args[0], tuple):
            args = args[0]
            params = len(args)

        if params == 1 and args[0] is None:
            clr = NSColor.colorWithDeviceWhite_alpha_(0.0, 0.0)
        elif params == 1 and isinstance(args[0], Color):
            if self._ctx._outputmode == RGB:
                clr = args[0]._rgb
            else:
                clr = args[0]._cmyk
        elif params == 1 and isinstance(args[0], NSColor):
            clr = args[0]
        elif (    params == 1
              and isinstance(args[0], (pstr,punicode))
              and len(args[0]) in (3,4,5,6,7,8,9)):
            # hex param
            try:
                a = args[0]
                # kill hash char
                if a[0] == '#':
                    a = a[1:]
                alpha = 1.0
                n = len(a)
                if n in (3,4):
                    div = 15.0
                    if n == 3:
                        r, g, b = a[:]
                    else:
                        r, g, b, alpha = a[:]
                else:
                    div = 255.0
                    if n == 6:
                        r, g, b = a[:2], a[2:4], a[4:6]
                    else:
                        r, g, b, alpha = a[:2], a[2:4], a[4:6], a[6:8]
                r = int(r, 16) / div
                g = int(g, 16) / div
                b = int(b, 16) / div
                if n in (4,8):
                    alpha = int(alpha, 16) / div
                clr = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, alpha)
            except Exception as err:
                print("Color parsing error: %s" % err)
                clr = NSColor.colorWithDeviceWhite_alpha_(0, 1)

        elif params == 1: # Gray, no alpha
            args = self._normalizeList(args)
            g, = args
            clr = NSColor.colorWithDeviceWhite_alpha_(g, 1)
        elif params == 2: # Gray and alpha
            args = self._normalizeList(args)
            g, a = args
            clr = NSColor.colorWithDeviceWhite_alpha_(g, a)
        elif params == 3 and self._ctx._colormode == RGB: # RGB, no alpha
            args = self._normalizeList(args)
            r,g,b = args
            clr = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, 1)
        elif params == 3 and self._ctx._colormode == HSB: # HSB, no alpha
            args = self._normalizeList(args)
            h, s, b = args
            clr = NSColor.colorWithDeviceHue_saturation_brightness_alpha_(h, s, b, 1)
        elif params == 4 and self._ctx._colormode == RGB: # RGB and alpha
            args = self._normalizeList(args)
            r,g,b, a = args
            clr = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, a)
        elif params == 4 and self._ctx._colormode == HSB: # HSB and alpha
            args = self._normalizeList(args)
            h, s, b, a = args
            clr = NSColor.colorWithDeviceHue_saturation_brightness_alpha_(h, s, b, a)
        elif params == 4 and self._ctx._colormode == CMYK: # CMYK, no alpha
            args = self._normalizeList(args)
            c, m, y, k  = args
            clr = NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(c, m, y, k, 1)
        elif params == 5 and self._ctx._colormode == CMYK: # CMYK and alpha
            args = self._normalizeList(args)
            c, m, y, k, a  = args
            clr = NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(c, m, y, k, a)
        else:
            clr = NSColor.colorWithDeviceWhite_alpha_(0, 1)

        self._cmyk = clr.colorUsingColorSpaceName_(NSDeviceCMYKColorSpace)
        self._rgb = clr.colorUsingColorSpaceName_(NSDeviceRGBColorSpace)

    def __repr__(self):
        return "%s(%.3f, %.3f, %.3f, %.3f)" % (self.__class__.__name__, self.red,
                self.green, self.blue, self.alpha)

    def __hash__( self ):
        return hash( (self.red, self.green, self.blue, self.alpha) )


    def set(self):
        self.nsColor.set()

    def _get_nsColor(self):
        if self._ctx._outputmode == RGB:
            return self._rgb
        else:
            return self._cmyk
    nsColor = property(_get_nsColor)
        

    def copy(self):
        new = self.__class__(self._ctx)
        new._rgb = self._rgb.copy()
        new._updateCmyk()
        return new

    def _updateCmyk(self):
        self._cmyk = self._rgb.colorUsingColorSpaceName_(NSDeviceCMYKColorSpace)

    def _updateRgb(self):
        self._rgb = self._cmyk.colorUsingColorSpaceName_(NSDeviceRGBColorSpace)

    def _get_hue(self):
        return self._rgb.hueComponent()

    def _set_hue(self, val):
        val = self._normalize(val)
        h, s, b, a = self._rgb.getHue_saturation_brightness_alpha_(None, None, None, None)
        self._rgb = NSColor.colorWithDeviceHue_saturation_brightness_alpha_(val, s, b, a)
        self._updateCmyk()
    h = hue = property(_get_hue, _set_hue, doc="the hue of the color")

    def _get_saturation(self):
        return self._rgb.saturationComponent()
    def _set_saturation(self, val):
        val = self._normalize(val)
        h, s, b, a = self._rgb.getHue_saturation_brightness_alpha_(None, None, None, None)
        self._rgb = NSColor.colorWithDeviceHue_saturation_brightness_alpha_(h, val, b, a)
        self._updateCmyk()
    s = saturation = property(_get_saturation,
                              _set_saturation,
                              doc="the saturation of the color")

    def _get_brightness(self):
        return self._rgb.brightnessComponent()

    def _set_brightness(self, val):
        val = self._normalize(val)
        h, s, b, a = self._rgb.getHue_saturation_brightness_alpha_(None, None, None, None)
        self._rgb = NSColor.colorWithDeviceHue_saturation_brightness_alpha_(h, s, val, a)
        self._updateCmyk()
    v = brightness = property(_get_brightness,
                              _set_brightness,
                              doc="the brightness of the color")

    def _get_hsba(self):
        return self._rgb.getHue_saturation_brightness_alpha_(None, None, None, None)

    def _set_hsba(self, values):
        val = self._normalize(val)
        h, s, b, a = values
        self._rgb = NSColor.colorWithDeviceHue_saturation_brightness_alpha_(h, s, b, a)
        self._updateCmyk()
    hsba = property(_get_hsba,
                    _set_hsba,
                    doc="the hue, saturation, brightness and alpha of the color")

    def _get_red(self):
        return self._rgb.redComponent()

    def _set_red(self, val):
        val = self._normalize(val)
        r, g, b, a = self._rgb.getRed_green_blue_alpha_(None, None, None, None)
        self._rgb = NSColor.colorWithDeviceRed_green_blue_alpha_(val, g, b, a)
        self._updateCmyk()
    r = red = property(_get_red, _set_red, doc="the red component of the color")

    def _get_green(self):
        return self._rgb.greenComponent()

    def _set_green(self, val):
        val = self._normalize(val)
        r, g, b, a = self._rgb.getRed_green_blue_alpha_(None, None, None, None)
        self._rgb = NSColor.colorWithDeviceRed_green_blue_alpha_(r, val, b, a)
        self._updateCmyk()
    g = green = property(_get_green, _set_green, doc="the green component of the color")

    def _get_blue(self):
        return self._rgb.blueComponent()
    def _set_blue(self, val):
        val = self._normalize(val)
        r, g, b, a = self._rgb.getRed_green_blue_alpha_(None, None, None, None)
        self._rgb = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, val, a)
        self._updateCmyk()
    b = blue = property(_get_blue, _set_blue, doc="the blue component of the color")

    def _get_alpha(self):
        return self._rgb.alphaComponent()
    def _set_alpha(self, val):
        val = self._normalize(val)
        r, g, b, a = self._rgb.getRed_green_blue_alpha_(None, None, None, None)
        self._rgb = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, val)
        self._updateCmyk()
    a = alpha = property(_get_alpha, _set_alpha, doc="the alpha component of the color")

    def _get_rgba(self):
        return self._rgb.getRed_green_blue_alpha_(None, None, None, None)

    def _set_rgba(self, val):
        val = self._normalizeList(val)
        r, g, b, a = val
        self._rgb = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, a)
        self._updateCmyk()
    rgba = property(_get_rgba,
                    _set_rgba,
                    doc="the red, green, blue and alpha values of the color")

    def _get_cyan(self):
        return self._cmyk.cyanComponent()

    def _set_cyan(self, val):
        val = self._normalize(val)
        c, m, y, k, a = self.cmyka
        self._cmyk = NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(val, m, y, k, a)
        self._updateRgb()
    c = cyan = property(_get_cyan, _set_cyan, doc="the cyan component of the color")

    def _get_magenta(self):
        return self._cmyk.magentaComponent()

    def _set_magenta(self, val):
        val = self._normalize(val)
        c, m, y, k, a = self.cmyka
        self._cmyk = NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(c, val, y, k, a)
        self._updateRgb()
    m = magenta = property(_get_magenta,
                           _set_magenta,
                           doc="the magenta component of the color")

    def _get_yellow(self):
        return self._cmyk.yellowComponent()

    def _set_yellow(self, val):
        val = self._normalize(val)
        c, m, y, k, a = self.cmyka
        self._cmyk = NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(
                                                                c, m, val, k, a)
        self._updateRgb()
    y = yellow = property(_get_yellow,
                          _set_yellow,
                          doc="the yellow component of the color")

    def _get_black(self):
        return self._cmyk.blackComponent()

    def _set_black(self, val):
        val = self._normalize(val)
        c, m, y, k, a = self.cmyka
        self._cmyk = NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(
                                                                c, m, y, val, a)
        self._updateRgb()
    k = black = property(_get_black,
                         _set_black,
                         doc="the black component of the color")

    def _get_cmyka(self):
        return (self._cmyk.cyanComponent(),
                self._cmyk.magentaComponent(),
                self._cmyk.yellowComponent(),
                self._cmyk.blackComponent(),
                self._cmyk.alphaComponent())
    cmyka = property(_get_cmyka, doc="a tuple containing the CMYKA values for this color")

    def blend(self, otherColor, factor):
        """Blend the color with otherColor with a factor; return the new color. Factor
        is a float between 0.0 and 1.0.
        """
        if hasattr(otherColor, "color"):
            otherColor = otherColor._rgb
        return self.__class__(color=self._rgb.blendedColorWithFraction_ofColor_(
                factor, otherColor))

    def _normalize(self, v):
        """Bring the color into the 0-1 scale for the current colorrange"""
        if self._ctx._colorrange == 1.0:
            return v
        return v / self._ctx._colorrange

    def _normalizeList(self, lst):
        """Bring the color into the 0-1 scale for the current colorrange"""
        r = self._ctx._colorrange
        if r == 1.0:
            return lst
        return [v / r for v in lst]
color = Color


class Transform(object):

    def __init__(self, transform=None):
        if transform is None:
            transform = NSAffineTransform.transform()
        elif isinstance(transform, Transform):
            matrix = transform._nsAffineTransform.transformStruct()
            transform = NSAffineTransform.transform()
            transform.setTransformStruct_(matrix)
        elif isinstance(transform, (list, tuple, NSAffineTransformStruct)):
            matrix = tuple(transform)
            transform = NSAffineTransform.transform()
            transform.setTransformStruct_(matrix)
        elif isinstance(transform, NSAffineTransform):
            pass
        else:
            raise NodeBoxError("Don't know how to handle transform %s." % transform)
        self._nsAffineTransform = transform
        
    def _get_transform(self):
        s = ("The 'transform' attribute is deprecated. "
             "Please use _nsAffineTransform instead.")
        warnings.warn(s, DeprecationWarning, stacklevel=2)
        return self._nsAffineTransform
    transform = property(_get_transform)

    def set(self):
        self._nsAffineTransform.set()

    def concat(self):
        self._nsAffineTransform.concat()

    def copy(self):
        return self.__class__(self._nsAffineTransform.copy())

    def __repr__(self):
        return "<%s [%.3f %.3f %.3f %.3f %.3f %.3f]>" % ((self.__class__.__name__,)
                                                          + tuple(self))

    def __iter__(self):
        for value in self._nsAffineTransform.transformStruct():
            yield value

    def _get_matrix(self):
        return self._nsAffineTransform.transformStruct()

    def _set_matrix(self, value):
        self._nsAffineTransform.setTransformStruct_(value)
    matrix = property(_get_matrix, _set_matrix)

    def rotate(self, degrees=0, radians=0):
        if degrees:
            self._nsAffineTransform.rotateByDegrees_(degrees)
        else:
            self._nsAffineTransform.rotateByRadians_(radians)

    def translate(self, x=0, y=0):
        self._nsAffineTransform.translateXBy_yBy_(x, y)

    def scale(self, x=1, y=None):
        if y is None:
            y = x
        self._nsAffineTransform.scaleXBy_yBy_(x, y)

    def skew(self, x=0, y=0):
        import math
        x = math.pi * x / 180
        y = math.pi * y / 180
        t = Transform()
        t.matrix = 1, math.tan(y), -math.tan(x), 1, 0, 0
        self.prepend(t)

    def invert(self):
        self._nsAffineTransform.invert()

    def append(self, other):
        if isinstance(other, Transform):
            other = other._nsAffineTransform
        self._nsAffineTransform.appendTransform_(other)

    def prepend(self, other):
        if isinstance(other, Transform):
            other = other._nsAffineTransform
        self._nsAffineTransform.prependTransform_(other)

    def transformPoint(self, point):
        return self._nsAffineTransform.transformPoint_(point)

    def transformBezierPath(self, path):
        if isinstance(path, BezierPath):
            path = BezierPath(path._ctx, path)
        else:
            raise NodeBoxError("Can only transform BezierPaths")
        path._nsBezierPath = self._nsAffineTransform.transformBezierPath_(path._nsBezierPath)
        return path


class Image(Grob, TransformMixin):

    stateAttributes = ('_transform', '_transformmode')
    kwargs = ()

    def __init__(self, ctx, path=None, x=0, y=0,
                       width=None, height=None, alpha=1.0, image=None, data=None):
        """
        Parameters:
         - path: A path to a certain image on the local filesystem.
         - x: Horizontal position.
         - y: Vertical position.
         - width: Maximum width. Images get scaled according to this factor.
         - height: Maximum height. Images get scaled according to this factor.
              If a width and height are both given, the smallest 
              of the two is chosen.
         - alpha: transparency factor
         - image: optionally, an Image or NSImage object.
         - data: a stream of bytes of image data.
        """
        super(Image, self).__init__(ctx)
        TransformMixin.__init__(self)

        # pdb.set_trace()

        if data is not None:
            if not isinstance(data, NSData):
                data = NSData.dataWithBytes_length_(data, len(data))
            self._nsImage = NSImage.alloc().initWithData_(data)
            if self._nsImage is None:
                raise NodeBoxError("can't read image %r" % path)
            self._nsImage.setFlipped_(True)
            self._nsImage.setCacheMode_(NSImageCacheNever)

        elif image is not None:
            if isinstance(image, NSImage):
                self._nsImage = image
                self._nsImage.setFlipped_(True)
            else:
                raise NodeBoxError("Don't know what to do with %s." % image)

        elif path is not None:
            if not os.path.exists(path):
                raise NodeBoxError('Image "%s" not found.' % path)
            curtime = os.path.getmtime(path)
            try:
                image, lasttime = self._ctx._imagecache[path]
                if lasttime != curtime:
                    image = None
            except KeyError:
                pass
            if image is None:
                image = NSImage.alloc().initWithContentsOfFile_(path)
                if image is None:
                    raise NodeBoxError("Can't read image %r" % path)
                image.setFlipped_(True)
                image.setCacheMode_(NSImageCacheNever)
                self._ctx._imagecache[path] = (image, curtime)
            self._nsImage = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alpha = alpha
        self.debugImage = False

    def _get_image(self):
        w = "The 'image' attribute is deprecated. Please use _nsImage instead."
        warnings.warn(w, DeprecationWarning, stacklevel=2)
        return self._nsImage
    image = property(_get_image)

    def copy(self):
        new = self.__class__(self._ctx)
        _copy_attrs(self, new, ('image', 'x', 'y', 'width', 'height',
                                '_transform', '_transformmode', 'alpha', 'debugImage'))
        return new

    def getSize(self):
        return self._nsImage.size()

    size = property(getSize)

    def _draw(self):
        """Draw an image on the given coordinates."""

        srcW, srcH = self._nsImage.size()
        srcRect = ((0, 0), (srcW, srcH))

        # Width or height given
        if self.width is not None or self.height is not None:
            if self.width is not None and self.height is not None:
                factor = min(self.width / srcW, self.height / srcH)
            elif self.width is not None:
                factor = self.width / srcW
            elif self.height is not None:
                factor = self.height / srcH
            _save()

            # Center-mode transforms: translate to image center
            if self._transformmode == CENTER:
                # This is the hardest case: center-mode transformations with given
                # width or height.
                # Order is very important in this code.

                # Set the position first, before any of the scaling or transformations
                # are done.
                # Context transformations might change the translation, and we don't
                # want that.
                t = Transform()
                t.translate(self.x, self.y)
                t.concat()

                # Set new width and height factors. Note that no scaling is done yet:
                # they're just here to set the new center of the image according to
                # the scaling factors.
                srcW = srcW * factor
                srcH = srcH * factor

                # Move image to newly calculated center.
                dX = srcW / 2
                dY = srcH / 2
                t = Transform()
                t.translate(dX, dY)
                t.concat()

                # Do current transformation.
                self._transform.concat()

                # Move back to the previous position.
                t = Transform()
                t.translate(-dX, -dY)
                t.concat()

                # Finally, scale the image according to the factors.
                t = Transform()
                t.scale(factor)
                t.concat()
            else:
                # Do current transformation
                self._transform.concat()
                # Scale according to width or height factor
                t = Transform()
                t.translate(self.x, self.y) # Here we add the positioning of the image.
                t.scale(factor)
                t.concat()

            # A debugImage draws a black rectangle instead of an image.
            if self.debugImage:
                Color(self._ctx).set()
                pt = BezierPath()
                pt.rect(0, 0, srcW / factor, srcH / factor)
                pt.fill()
            else:
                self._nsImage.drawAtPoint_fromRect_operation_fraction_((0, 0),
                                            srcRect, NSCompositeSourceOver, self.alpha)
            _restore()
        # No width or height given
        else:
            _save()
            x,y = self.x, self.y
            # Center-mode transforms: translate to image center
            if self._transformmode == CENTER:
                deltaX = srcW / 2
                deltaY = srcH / 2
                t = Transform()
                t.translate(x+deltaX, y+deltaY)
                t.concat()
                x = -deltaX
                y = -deltaY
            # Do current transformation
            self._transform.concat()
            # A debugImage draws a black rectangle instead of an image.
            if self.debugImage:
                Color(self._ctx).set()
                pt = BezierPath()
                pt.rect(x, y, srcW, srcH)
                pt.fill()
            else:
                # The following code avoids a nasty bug in Cocoa/PyObjC.
                # Apparently, EPS files are put on a different position when drawn
                # with a certain position.
                # However, this only happens when the alpha value is set to 1.0: set
                # it to something lower and the positioning is the same as a bitmap
                # file.
                # I could of course make every EPS image have an alpha value of
                # 0.9999, but this solution is better: always use zero coordinates for
                # drawAtPoint and use a transform to set the final position.
                t = Transform()
                t.translate(x,y)
                t.concat()
                self._nsImage.drawAtPoint_fromRect_operation_fraction_(
                                (0,0), srcRect, NSCompositeSourceOver, self.alpha)
            _restore()


class Text(Grob, TransformMixin, ColorMixin):

    stateAttributes = ('_transform', '_transformmode', '_fillcolor', '_fontname',
                       '_fontsize', '_align', '_lineheight')
    kwargs = ('fill', 'font', 'fontsize', 'align', 'lineheight')

    __dummy_color = NSColor.blackColor()
    
    def __init__(self, ctx, text, x=0, y=0, width=None, height=None, **kwargs):
        super(Text, self).__init__(ctx)
        TransformMixin.__init__(self)
        ColorMixin.__init__(self, **kwargs)
        self.text = makeunicode(text)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._fontname = kwargs.get('font', "Helvetica")
        self._fontsize = kwargs.get('fontsize', 24)
        self._lineheight = max(kwargs.get('lineheight', 1.2), 0.01)
        self._align = kwargs.get('align', NSLeftTextAlignment)

    def copy(self):
        new = self.__class__(self._ctx, self.text)
        _copy_attrs(self, new,
            ('x', 'y', 'width', 'height', '_transform', '_transformmode', 
            '_fillcolor', '_fontname', '_fontsize', '_align', '_lineheight'))
        return new
        
    def font_exists(cls, fontname):
        # Check if the font exists.
        f = NSFont.fontWithName_size_(fontname, 12)
        return f is not None
    font_exists = classmethod(font_exists)

    def _get_font(self):
        return NSFont.fontWithName_size_(self._fontname, self._fontsize)
    font = property(_get_font)

    def _getLayoutManagerTextContainerTextStorage(self, clr=__dummy_color):
        paraStyle = NSMutableParagraphStyle.alloc().init()
        paraStyle.setAlignment_(self._align)
        paraStyle.setLineBreakMode_(NSLineBreakByWordWrapping)
        paraStyle.setLineHeightMultiple_(self._lineheight)

        d = {
            NSParagraphStyleAttributeName:  paraStyle,
            NSForegroundColorAttributeName: clr,
            NSFontAttributeName:            self.font
        }

        t = makeunicode( self.text )
        textStorage = NSTextStorage.alloc().initWithString_attributes_(t, d)
        try:
            textStorage.setFont_(self.font)
        except ValueError:
            raise NodeBoxError("Text.draw(): font '%s' not available.\n" % self._fontname)
            return

        layoutManager = NSLayoutManager.alloc().init()
        textContainer = NSTextContainer.alloc().init()
        if self.width != None:
            textContainer.setContainerSize_((self.width,1000000))
            textContainer.setWidthTracksTextView_(False)
            textContainer.setHeightTracksTextView_(False)
        layoutManager.addTextContainer_(textContainer)
        textStorage.addLayoutManager_(layoutManager)
        return layoutManager, textContainer, textStorage

    def _draw(self):
        if self._fillcolor is None:
            return

        s = self._getLayoutManagerTextContainerTextStorage(self._fillcolor.nsColor)
        layoutManager, textContainer, textStorage = s

        x,y = self.x, self.y
        glyphRange = layoutManager.glyphRangeForTextContainer_(textContainer)
        s = layoutManager.boundingRectForGlyphRange_inTextContainer_(glyphRange,
                                                                    textContainer)
        (dx, dy), (w, h) = s
        preferredWidth, preferredHeight = textContainer.containerSize()
        if self.width is not None:
            if self._align == RIGHT:
                x += preferredWidth - w
            elif self._align == CENTER:
                x += preferredWidth/2 - w/2

        _save()
        # Center-mode transforms: translate to image center
        if self._transformmode == CENTER:
            deltaX = w / 2
            deltaY = h / 2
            t = Transform()
            t.translate(x+deltaX, y-self.font.defaultLineHeightForFont()+deltaY)
            t.concat()
            self._transform.concat()
            layoutManager.drawGlyphsForGlyphRange_atPoint_(glyphRange,
                                                           (-deltaX-dx,-deltaY-dy))
        else:
            self._transform.concat()
            layoutManager.drawGlyphsForGlyphRange_atPoint_(glyphRange,
                                    (x-dx, y-dy-self.font.defaultLineHeightForFont()))
        _restore()
        return (w, h)

    def _get_allmetrics(self):
        items = self._getLayoutManagerTextContainerTextStorage()
        layoutManager, textContainer, textStorage = items
        glyphRange = layoutManager.glyphRangeForTextContainer_(textContainer)
        (dx, dy), (w, h) = layoutManager.boundingRectForGlyphRange_inTextContainer_(
                                                            glyphRange, textContainer)
        # print "metrics (dx,dy):", (dx,dy)
        return dx,dy,w,h
    allmetrics = property(_get_allmetrics)

    def _get_metrics(self):
        dx,dy,w,h = self._get_allmetrics()
        return w,h
    metrics = property(_get_metrics)

    def _get_path(self):
        items = self._getLayoutManagerTextContainerTextStorage()
        layoutManager, textContainer, textStorage = items
        x, y = self.x, self.y
        glyphRange = layoutManager.glyphRangeForTextContainer_(textContainer)
        (dx, dy), (w, h) = layoutManager.boundingRectForGlyphRange_inTextContainer_(
                                                            glyphRange, textContainer)
        preferredWidth, preferredHeight = textContainer.containerSize()
        if self.width is not None:
           if self._align == RIGHT:
               x += preferredWidth - w
           elif self._align == CENTER:
               x += preferredWidth/2 - w/2
        length = layoutManager.numberOfGlyphs()
        path = NSBezierPath.bezierPath()
        for glyphIndex in range(length):
            lineFragmentRect = layoutManager.lineFragmentRectForGlyphAtIndex_effectiveRange_(
                                                                    glyphIndex, None)
            # HACK: PyObjc 2.0 and 2.2 are subtly different:
            #  - 2.0 (bundled with OS X 10.5) returns one argument: the rectangle.
            #  - 2.2 (bundled with OS X 10.6) returns two arguments: the rectangle and the range.
            # So we check if we got one or two arguments back (in a tuple) and unpack them.
            if isinstance(lineFragmentRect, tuple):
                lineFragmentRect = lineFragmentRect[0]
            layoutPoint = layoutManager.locationForGlyphAtIndex_(glyphIndex)

            # Here layoutLocation is the location (in container coordinates)
            # where the glyph was laid out. 
            finalPoint = [lineFragmentRect[0][0],lineFragmentRect[0][1]]
            finalPoint[0] += layoutPoint[0] - dx
            finalPoint[1] += layoutPoint[1] - dy
            g = layoutManager.glyphAtIndex_(glyphIndex)
            if g == 0:
                continue
            path.moveToPoint_((finalPoint[0], -finalPoint[1]))
            path.appendBezierPathWithGlyph_inFont_(g, self.font)
            path.closePath()
        path = BezierPath(self._ctx, path)
        trans = Transform()
        trans.translate(x,y-self.font.defaultLineHeightForFont())
        trans.scale(1.0,-1.0)
        path = trans.transformBezierPath(path)
        path.inheritFromContext()
        return path
    path = property(_get_path)


class Variable(object):
    def __init__(self, name, typ,
                       default=None, minV=0, maxV=100, value=None,
                       handler=None, menuitems=None):
        self.name = makeunicode(name)
        self.type = typ or NUMBER
        self.default = default
        self.min = minV
        self.max = maxV

        self.handler = None
        if handler is not None:
            self.handler = handler

        self.menuitems = None
        if menuitems is not None:
            if type(menuitems) in (list, tuple):
                self.menuitems = [makeunicode(i) for i in menuitems]
        
        if self.type == NUMBER:
            if default is None:
                self.default = 50
            self.min = minV
            self.max = maxV

        elif self.type == TEXT:
            if default is None:
                self.default = makeunicode("hello")
            else:
                self.default = makeunicode(default)

        elif self.type == BOOLEAN:
            if default is None:
                self.default = True
            else:
                self.default = bool(default)

        elif self.type == BUTTON:
            self.default = makeunicode(self.name)

        elif self.type == MENU:
            # value is list of menuitems
            # default is name of function to call with selected menu item name

            # old interface
            if type(value) in (list, tuple): # and type(default) in (function,):
                # print "type(default)", type(default)
                if default is not None:
                    self.handler = default
                self.menuitems = [makeunicode(i) for i in value]
                default = None
                value = ""
                

            if default is None:
                if self.menuitems is not None:
                    if len(self.menuitems) > 0:
                        default = self.menuitems[0]
                else:
                    default = u""
            self.default = default
        self.value = value or self.default
        self.control = None


    def sanitize(self, val):
        """Given a Variable and a value, cleans it out"""
        if self.type == NUMBER:
            try:
                return float(val)
            except ValueError:
                return 0.0
        elif self.type == TEXT:
            # return unicode(str(val), "utf_8", "replace")
            return makeunicode( val )
            try:
                # return unicode(str(val), "utf_8", "replace")
                return makeunicode( val )
            except:
                return ""
        elif self.type == BOOLEAN:
            v = makeunicode( val )
            if v.lower() in (u"true", u"1", u"yes"):
                return True
            else:
                return False

    def compliesTo(self, v):
        """Return whether I am compatible with the given var:
             - Type should be the same
             - My value should be inside the given vars' min/max range.
        """
        if self.type == v.type:
            if self.type == NUMBER:
                if self.value < self.min or self.value > self.max:
                    return False
            return True
        return False

    def __repr__(self):
        s = ("Variable(name=%s, typ=%s, default=%s, min=%s, max=%s, value=%s, "
             "handler=%s, menuitems=%s)")
        return s % (self.name, self.type, self.default, self.min, self.max, self.value,
                    repr(self.handler), repr(self.menuitems))


class _PDFRenderView(NSView):
    
    # This view was created to provide PDF data.
    # Strangely enough, the only way to get PDF data from Cocoa is by asking
    # dataWithPDFInsideRect_ from a NSView. So, we create one just to get to
    # the PDF data.

    def initWithCanvas_(self, canvas):

        # for some unknown reason the following line stopped working
        # Solution: use objc.super -- see import
        super(_PDFRenderView, self).initWithFrame_( ((0, 0), (canvas.width, canvas.height)) )
        # for some unknown reason this is the solution for the preceding problem
        # self.initWithFrame_( ((0, 0), (canvas.width, canvas.height)) )
        # it is the only super in this file, having a NS* superclass

        self.canvas = canvas
        return self
        
    def drawRect_(self, rect):
        self.canvas.draw()
        
    def isOpaque(self):
        return False

    def isFlipped(self):
        return True


class Canvas(Grob):

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        self.width = width
        self.height = height
        self.speed = None
        self.mousedown = False
        self.clear()

    def clear(self):
        self._grobs = self._container = []
        self._grobstack = [self._grobs]
        
    def _get_size(self):
        return self.width, self.height
    size = property(_get_size)

    def append(self, el):
        self._container.append(el)
        
    def __iter__(self):
        for grob in self._grobs:
            yield grob
            
    def __len__(self):
        return len(self._grobs)
        
    def __getitem__(self, index):
        return self._grobs[index]
        
    def push(self, containerGrob):
        self._grobstack.insert(0, containerGrob)
        self._container.append(containerGrob)
        self._container = containerGrob
        
    def pop(self):
        try:
            del self._grobstack[0]
            self._container = self._grobstack[0]
        except IndexError as e:
            raise NodeBoxError("pop: too many canvas pops!")

    def draw(self):
        if self.background is not None:
            self.background.set()
            NSRectFillUsingOperation(((0,0), (self.width, self.height)),
                                     NSCompositeSourceOver)
        for grob in self._grobs:
            grob._draw()
            
    def _get_nsImage(self):
        img = NSImage.alloc().initWithSize_((self.width, self.height))
        img.setFlipped_(True)
        img.lockFocus()
        self.draw()
        img.unlockFocus()
        return img
    _nsImage = property(_get_nsImage)

    def _getImageData(self, format):
        if format == 'pdf':
            view = _PDFRenderView.alloc().initWithCanvas_(self)
            return view.dataWithPDFInsideRect_(view.bounds())
        elif format == 'eps':
            view = _PDFRenderView.alloc().initWithCanvas_(self)
            return view.dataWithEPSInsideRect_(view.bounds())
        else:
            imgTypes = {"gif":  NSGIFFileType,
                        "jpg":  NSJPEGFileType,
                        "jpeg": NSJPEGFileType,
                        "png":  NSPNGFileType,
                        "tiff": NSTIFFFileType}
            if format not in imgTypes:
                e = "Filename should end in .pdf, .eps, .tiff, .gif, .jpg or .png"
                raise NodeBoxError(e)
            data = self._nsImage.TIFFRepresentation()
            if format != 'tiff':
                imgType = imgTypes[format]
                rep = NSBitmapImageRep.imageRepWithData_(data)
                return rep.representationUsingType_properties_(imgType, None)
            else:
                return data

    def save(self, fname, format=None):
        if format is None:
            basename, ext = os.path.splitext(fname)
            format = ext[1:].lower() # Skip the dot
        data = self._getImageData(format)
        fname = NSString.stringByExpandingTildeInPath(fname)
        data.writeToFile_atomically_(fname, False)

def _test():
    import doctest, cocoa
    return doctest.testmod(cocoa)

if __name__=='__main__':
    _test()
