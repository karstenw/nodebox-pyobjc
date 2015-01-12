background( None )
size(1100,900)

"""Create a Escher squarelimit drawing."""


import math


# scale factor for next smaller picture
smaller = 1 / math.sqrt(2)


# global counter
no_of_pictures = 0

# unused
types = {
    1: "line",
    2: "linesegments",
    3: "curvesegments"}

# debug options
# draw a rectangle around picture
dbg_frame = False

# draw a circle around points
dbg_points = False

# draw a circle around startpoints
dbg_starts = False

# switch off content rendering
dbg_NOCONTENT = False

# scales content to 85%
dbg_smallerscale = False

# guess what, gives pictures a twist
dbg_randomtwist = False

# set pictures apart by self.size / offsetpart
dbg_offset = False

# 1/25.0 -> 4% offset
offsetpart = 25.0

dbg_any = (   dbg_offset
           or dbg_smallerscale
           or dbg_NOCONTENT
           or dbg_starts
           or dbg_points
           or dbg_frame
           or dbg_randomtwist)

# color for debug marks
mark_color = color(1.0, 0.0, 0.0, 1.0)

# std line color
line_color = color(0.0, 0.0, 0.0, 1.0)

pictlinewidth = 1.0
framelinewidth = 0.3


class Segment(object):
    """
    Hold a line or polygon.

    type - what to draw with point list
        1: a line
        2: a polygon
        3: a curvesegment

    points - list of x,y tuples


    Currently only polygons are drawn
    """

    def __init__(self, type_, points):
        self.type = type_
        self.points = points

    def draw(self, context):
        if self.type == 1:
            """
            A single line.
            """
            pass

        elif self.type == 2:
            """
            a list of points drawn as a polygon. If first and last point are the
            same, last point is popped and autoclosepath is called.
            """
            push()

            # stupid experiment... funny results
            # seems like it was the wrong place...
            if False: # dbg_smallerscale:
                transform(CENTER)
                scale(0.85)

            L = list(self.points) # [:]
            n = len(self.points)

            # check for a closed polygon
            if L[0] == L[-1]:
                close = True
                L.pop()
            else:
                close = False
            autoclosepath( close )

            beginpath()

            if dbg_frame or dbg_points or dbg_starts:
                # draw a circle at my origin
                strokewidth(framelinewidth)
                stroke( mark_color )
                oval(-2, -2, 4, 4)
                stroke( line_color )
                strokewidth(pictlinewidth)

            for i,p in enumerate(L):
                if i == 0:
                    # first point
                    moveto( p[0], p[1] )
                    # last = p
                else:
                    lineto(p[0], p[1])
                    if dbg_points:
                        strokewidth(framelinewidth)
                        oval(p[0]-1, p[1]-1, 2, 2)
                        strokewidth(pictlinewidth)
                    # last = p

            if not dbg_NOCONTENT:
                path = endpath(draw=True)
                #drawpath( path )

            if False: #dbg_smallerscale:
                transform(CORNER)
                scale(1.15)

            pop()
        elif self.type == 3:
            pass


class Picture(object):
    """A list of Segments make a Picture.
    """

    def __init__(self, size_, segments):
        # extent
        self.size = size_

        # segmentlist
        self.segments = segments

    def draw_NBContext(self, c=None):
        if dbg_frame:
            push()
            strokewidth(framelinewidth)
            x = self.size[0]
            y = self.size[1]
            if True:
                rect(0,0,self.size[0], self.size[1])
            else:
                line(0,0, x,0)
                line(x,0, 0,y)
                line(0,y, 0,0)
            strokewidth(pictlinewidth)
            pop()

        if dbg_randomtwist:
            r = random(-15.0, 15.0)
            rotate(r)

        if dbg_smallerscale:
            #transform(CENTER)
            scale(0.85)

        for i, s in enumerate(self.segments):
            if dbg_frame:
                # mark origin of picture
                if i == 0:
                    # rect(-2,-2,4,4)
                    pass
            push()
            s.draw(None)
            pop()
    draw = draw_NBContext


    def draw_FrameContext(self, frame):
        """
        Draw in the context of a Henderson style frame

        TBD
        """
        pass


# a list of Segments making up the squarelimit fish
# uncolored

fish = [
    # torso outline
    Segment(2,( (0,0), (20,20), (30,16), (38,12), (44,4),
                (50,4), (60,4), (72,2), (80,0), (75,3),
                (68,8), (63,13), (60,16), (53,15), (46,17),
                (40,20), (32,32), (40,40), (40,60), (33,63),
                (27,65), (20,64), (17,67), (12,72), (5,77),
                (0,80), (-2,72), (-4,60), (-4,50), (-4,44),
                (-12,38), (-16,30), (-20,20), (0,0) )),

    # outer eye
    Segment(2, ( (0,64), (0,54), (4,58), (0,64) )),

    # inner eye
    Segment(2, ( (8,68), (8,58), (12,60), (8,68) )),

    # fin line
    Segment(2, ( (8,54), (16,42), (28,26), (40,16), (58,10) )),

    # flossenrand torso aussen
    Segment(2, ( (-4,44), (6,28), (20,20) )),

    # fl 1
    Segment(2, ( (-2,36), (-8,30), (-12,22) )),

    # fl 2
    Segment(2, ( (2,30), (-6,22), (-8,16) )),

    # fl 3
    Segment(2, ( (8,24), (-2,16), (-4,10) )),

    # fl 4
    Segment(2, ( (10,18), (2,10), (0,6) )),

    # flossenrand torso innen
    Segment(2, ( (20,64), (24,56), (26,44), (32,32) )),

    # fl 1
    Segment(2, ( (26,56), (30,58), (34,58), (40,54) )),

    # fl 2
    Segment(2, ( (28,50), (32,52), (36,52), (40,50) )),

    # fl 3
    Segment(2, ( (30,42), (34,46), (40,46) )),

    # shadow line 1
    Segment(2, ( (38,36), (40,34) )),

    # shadow line 2
    Segment(2, ( (38,32), (40,30) )),

    # shadow line 3
    Segment(2, ( (36,30), (40,26) ))
]

insettriangle = [
    # inset triangle
    Segment(2, ( (10, 10), (70, 10), (10,70), (10,10) ))
            ]

triangle = [
    # triangle
    Segment(2, ( (0, 0), (80, 0), (0, 80), (0, 0) ))
            ]


def build_up_module(picture, doleft, doright, level):
    """
    Squarelimit layout engine.

    Assumes a current point and orientation.

    The "up_module" in ascii speak:

    ------+----------+------
    \     |    /\    |     /
     \    |   /  \   |    /
      \   |  /    \  |   /
       \  | /      \ |  /
        \ |/        \| /
         \|----------|/

    The left and right triangles are drawn if doleft/doright are True respectively.
    """
    pict_size_x = picture.size[0]
    pict_size_y = picture.size[1]

    # function scope push
    push()

    translate(pict_size_x / 2, pict_size_y / 2)

    if dbg_offset:
        translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

    # pict 1
    rotate(135)
    scale(-smaller, smaller)
    draw_squarellimit_quarter(picture, level, False)

    if True:
        # right quarter sized pictures
        push()
        translate(pict_size_x / 2, pict_size_y / 2)

        if dbg_offset:
            translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

        rotate(135)
        scale(-smaller, smaller)
        draw_squarellimit_quarter(picture, level, True, doleft=False, doright=False)
        rotate(90)
        draw_squarellimit_quarter(picture, level, False)

        # right edge
        if doright:
            push()
            translate(pict_size_x, pict_size_y)

            if dbg_offset:
                translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

            rotate(180)
            draw_squarellimit_quarter(picture, level, False)
            rotate(90)

            # this is right outmost
            draw_squarellimit_quarter(picture, level, True, doleft=False, doright=True)
            pop()
        pop()

    rotate(90)
    draw_squarellimit_quarter(picture, level, False)

    if True:
        # left quarter sized pictures
        push()
        translate(pict_size_x / 2, pict_size_y / 2)

        if dbg_offset:
            translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

        rotate(135)
        scale(-smaller, smaller)
        draw_squarellimit_quarter(picture, level, False)

        # left edge
        if doleft:
            push()
            translate(pict_size_x, pict_size_y)

            if dbg_offset:
                translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

            rotate(180)
            draw_squarellimit_quarter(picture, level, False)
            rotate(-90)

            # this is left outmost
            draw_squarellimit_quarter(picture, level, True, doleft=True, doright=False)
            pop()
        rotate(90)
        draw_squarellimit_quarter(picture, level, True)
        pop()
    pop()

def build_down_module(picture, doleft, doright, level):
    """
    Squarelimit layout engine.

    Assumes a current point and orientation.

    The "up_module" in ascii speak:

    ------+----------+------
    \     |    /\    |     /
     \    |   /  \   |    /
      \   |  /    \  |   /
       \  | /      \ |  /
        \ |/        \| /
         \|----------|/

    The left and right triangles are drawn if doleft/doright are True respectively.
    """
    pict_size_x = picture.size[0]
    pict_size_y = picture.size[1]

    # function scope push
    push()

    translate(pict_size_x / 2, pict_size_y / 2)

    if dbg_offset:
        translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

    # pict 1
    rotate(135)
    scale(-smaller, smaller)
    draw_squarellimit_quarter(picture, level, False)

    if True:
        # right quarter sized pictures
        push()
        translate(pict_size_x / 2, pict_size_y / 2)

        if dbg_offset:
            translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

        rotate(135)
        scale(-smaller, smaller)
        draw_squarellimit_quarter(picture, level, True, doleft=False, doright=False)
        rotate(90)
        draw_squarellimit_quarter(picture, level, False)

        # right edge
        if doright:
            push()
            translate(pict_size_x, pict_size_y)

            if dbg_offset:
                translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

            rotate(180)
            draw_squarellimit_quarter(picture, level, False)
            rotate(90)

            # this is right outmost
            draw_squarellimit_quarter(picture, level, True, doleft=False, doright=True)
            pop()
        pop()

    rotate(90)
    draw_squarellimit_quarter(picture, level, False)

    if True:
        # left quarter sized pictures
        push()
        translate(pict_size_x / 2, pict_size_y / 2)

        if dbg_offset:
            translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

        rotate(135)
        scale(-smaller, smaller)
        draw_squarellimit_quarter(picture, level, False)

        # left edge
        if doleft:
            push()
            translate(pict_size_x, pict_size_y)

            if dbg_offset:
                translate(pict_size_x / offsetpart, pict_size_y / offsetpart)

            rotate(180)
            draw_squarellimit_quarter(picture, level, False)
            rotate(-90)

            # this is left outmost
            draw_squarellimit_quarter(picture, level, True, doleft=True, doright=False)
            pop()
        rotate(90)
        draw_squarellimit_quarter(picture, level, True)
        pop()
    pop()


def draw_squarellimit_quarter(picture, level, buildup, doleft=False, doright=False):
    """
    """
    global no_of_pictures
    # dbg_frame = True
    if level >= 0:
        push()
        # this global is just for picture counting
        no_of_pictures += 1
        picture.draw()

        if buildup:
            build_up_module(picture, doleft, doright, level - 1)
        pop()


def inversesquarelimit( picture, depth ):
    """Squarelimit is drawn in a triangular style. For the whole picture, 4 triangles forming
    a square are drawn.
    """

    # no of triangles
    n = 4

    # advance in degrees
    q = 90

    transform(CORNER)
    scale(1, 1)

    for i in range(n):
        push()
        rotate( i * q )

        if dbg_offset:
            translate(picture.size[0] / offsetpart, picture.size[1] / offsetpart)

        draw_squarellimit_quarter(picture, depth, True, True, True)
        pop()

    
    

def squarelimit(picture, depth, qstart=1, qstop=4):
    """Squarelimit is drawn in a triangular style. For the whole picture, 4 triangles forming
    a square are drawn.
    """

    # no of quarters
    n = 4

    # advance in degrees
    q = 90

    transform(CORNER)
    scale(1, 1)

    for i in range(n):
        push()
        rotate( i * q )

        if dbg_offset:
            translate(picture.size[0] / offsetpart, picture.size[1] / offsetpart)

        draw_squarellimit_quarter(picture, depth, True, True, True)
        pop()


if __name__ == '__builtin__':

    #starting point
    px = py = 350

    if dbg_offset:
        parts = 1 + 1 / offsetpart
        px *= parts
        py *= parts

    # correct version:
    fishpicture = Picture( (80, 80), fish)
    insettrianglepicture = Picture( (80, 80), insettriangle)
    trianglepicture = Picture( (80, 80), triangle)
    reset()
    # scale(2)
    strokewidth(1)
    stroke( line_color )

    translate(px, py)
    rotate(135)

    nofill()
    scale(2)

    # The actual call:
    squarelimit(fishpicture, 3)
    # squarelimit(insettrianglepicture, 8)

    print "#pictures rendered:", no_of_pictures
