


def linecap_flat(pt1, pt2, path):
    """Flat line ending. A line from pt1 to pt2."""
    path.lineto(pt2.x, pt2.y)


def linecap_rounded(pt1, pt2, path):
    """."""
    a = _ctx.angle(pt1.x, pt1.y, pt2.x, pt2.y)
    d = _ctx.distance(pt1.x, pt1.y, pt2.x, pt2.y) * 1
    dx1, dy1 = _ctx.coordinates(pt1.x, pt1.y, d, a+90)
    dx2, dy2 = _ctx.coordinates(pt2.x, pt2.y, d, a+90)
    path.curveto(dx1, dy1, dx2, dy2, pt2.x, pt2.y)    


def smoothstep(a, b, x):
    """ Returns a smooth transition between 0.0 and 1.0 
        using Hermite interpolation (cubic spline),
        where x is a number between a and b. 
        The return value will ease (slow down) as x nears a or b.
        For x smaller than a, returns 0.0. For x bigger than b, returns 1.0.
    """
    if x < a:
        return 0.0
    if x >=b:
        return 1.0
    x = float(x-a) / (b-a)
    return x*x * (3-2*x)


def transform_uniform(time, dist, ang):
    return dist, ang


def transform_expand(time, dist, ang):
    return dist * (0.2 + 0.8 * time), ang


def transform_contract(time, dist, ang):
    return dist * (0.2 + 0.8*(1-time)), ang


def transform_smooth(time, dist, ang):
    return dist * smoothstep(0.0, 1.0, time), ang


def outline_stroke( path,
                    linecap=linecap_flat,
                    transform=transform_uniform,
                    precision=30,
                    debug=True,
                    fixedangle=None):
    
    """Returns an outlined path from the given path and the current strokewidth.
    This will plot vector points along the stroke edge.
    Interesting effects can be achieved by modifying the thickness of the path
    at each individual point. This can be done with the given transform function:
    - It takes three parameters: time, distance, angle.
    - It returns a new distance and angle.
    The time represents the current place on the path as a number between 0.0-1.0.
    The distance represents the thickness of the path."""
    
    
    leftBorder = [] # The stroke edge to "the left" of the path.
    rightBorder = [] # The stroke edge to "the right" of the path.
    
    # The stroke width / 2 is the distance from the path to the left and right.
    # This distance can be tweaked by the given transform function.
    r = _ctx.strokewidth() * 0.5
    
    # Take a number of sample points on the path.
    # The longer the path, the more precision is needed.
    points = list( path.points(precision) )
    
    for i, pt in enumerate(points):
        # We can calculate the angle (i.e. direction) of a point
        # from the line between this point and the next.
        # For the last point, take the line to the previous point 
        # and reverse the angle.

        if fixedangle:
            a = fixedangle
        else:
            if i < precision-1:
                next = points[i+1]
                a = _ctx.angle(pt.x, pt.y, next.x, next.y)
            else:
                previous = points[i-1]
                a = _ctx.angle(pt.x, pt.y, previous.x, previous.y) - 180
        
        d = r
        d, a = transform(float(i)/precision, d, a)
        
        # With some basic trigonometry, we can calculate the coordinates
        # of a new point at a distance from the point on the path.
        # The direction + 90 degrees is a point on the left stroke edge,
        # the direction - 90 degrees is a point on the right stroke edge.
        dx1, dy1 = _ctx.coordinates(pt.x, pt.y, d, a+90)
        dx2, dy2 = _ctx.coordinates(pt.x, pt.y, d, a-90)
        leftBorder.append( (dx1, dy1) )
        rightBorder.append( (dx2, dy2) )
        if debug == True:
            # In debug mode, show the sample points,
            # the calculated points on the stroke edge,
            # and the angles between them.
            _ctx.strokewidth(0.5)
            _ctx.oval(pt.x-1, pt.y-1, 2, 2)
            _ctx.oval(dx1-2, dy1-2, 4, 4)
            _ctx.oval(dx2-2, dy2-2, 4, 4)
            _ctx.line(dx1, dy1, pt.x, pt.y)
            _ctx.line(dx2, dy2, pt.x, pt.y)
    
    # Reset the strokewidth (we may have changed it in debug mode).
    _ctx.strokewidth(r*2)        
    
    # From the points on the stroke edges,
    # calculate new Bezier paths.
    leftBorder = _ctx.findpath(leftBorder)
    rightBorder = _ctx.findpath(list(reversed(rightBorder)))
    
    # Join the paths in a single path and close the beginning and end.
    # The linecap function defines the style of the join.
    path = _ctx.BezierPath()
    for pt in leftBorder: 
        path.append(pt)
    
    linecap(pt, rightBorder[0], path) # Close end.
    for pt in rightBorder: 
        path.append(pt)
    
    linecap(pt, leftBorder[0], path) # Close beginning.
    return path


def makepath( startx, starty, ctrl1x, ctrl1y, ctrl2x, ctrl2y, endx, endy ):
    path = _ctx.BezierPath()
    path.moveto( startx, starty )
    path.curveto( ctrl1x, ctrl1y, ctrl2x, ctrl2y, endx, endy )
    return path

