<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="karstenw.20260813135631.2" a="E"><vh>NewHeadlineOutline Stroke</vh>
<v t="karstenw.20260813135657.1" a="E"><vh>Library</vh>
<v t="karstenw.20260813135703.1" a="E"><vh>@clean strokelib.py</vh>
<v t="karstenw.20260813135730.1"><vh>Declarations</vh></v>
<v t="karstenw.20260813135717.1"><vh>linecap_flat</vh></v>
<v t="karstenw.20260813135717.2"><vh>linecap_rounded</vh></v>
<v t="karstenw.20260813135717.3"><vh>smoothstep</vh></v>
<v t="karstenw.20260813135717.4"><vh>transform_uniform</vh></v>
<v t="karstenw.20260813135717.5"><vh>transform_expand</vh></v>
<v t="karstenw.20260813135717.6"><vh>transform_contract</vh></v>
<v t="karstenw.20260813135717.7"><vh>transform_smooth</vh></v>
<v t="karstenw.20260813135717.8" a="E"><vh>outline_stroke</vh>
<v t="karstenw.20260813140017.1"><vh>&lt;&lt; function comment &gt;&gt;</vh></v>
</v>
<v t="karstenw.20260813135717.9"><vh>makepath</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20260813135631.2"></t>
<t tx="karstenw.20260813135657.1"></t>
<t tx="karstenw.20260813135703.1">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20260813135717.1">def linecap_flat(pt1, pt2, path):
    """Flat line ending. A line from pt1 to pt2."""
    path.lineto(pt2.x, pt2.y)


</t>
<t tx="karstenw.20260813135717.2">def linecap_rounded(pt1, pt2, path):
    """."""
    a = _ctx.angle(pt1.x, pt1.y, pt2.x, pt2.y)
    d = _ctx.distance(pt1.x, pt1.y, pt2.x, pt2.y) * 1
    dx1, dy1 = _ctx.coordinates(pt1.x, pt1.y, d, a+90)
    dx2, dy2 = _ctx.coordinates(pt2.x, pt2.y, d, a+90)
    path.curveto(dx1, dy1, dx2, dy2, pt2.x, pt2.y)    


</t>
<t tx="karstenw.20260813135717.3">def smoothstep(a, b, x):
    """ Returns a smooth transition between 0.0 and 1.0 
        using Hermite interpolation (cubic spline),
        where x is a number between a and b. 
        The return value will ease (slow down) as x nears a or b.
        For x smaller than a, returns 0.0. For x bigger than b, returns 1.0.
    """
    if x &lt; a:
        return 0.0
    if x &gt;=b:
        return 1.0
    x = float(x-a) / (b-a)
    return x*x * (3-2*x)


</t>
<t tx="karstenw.20260813135717.4">def transform_uniform(time, dist, ang):
    return dist, ang


</t>
<t tx="karstenw.20260813135717.5">def transform_expand(time, dist, ang):
    return dist * (0.2 + 0.8 * time), ang


</t>
<t tx="karstenw.20260813135717.6">def transform_contract(time, dist, ang):
    return dist * (0.2 + 0.8*(1-time)), ang


</t>
<t tx="karstenw.20260813135717.7">def transform_smooth(time, dist, ang):
    return dist * smoothstep(0.0, 1.0, time), ang


</t>
<t tx="karstenw.20260813135717.8">def outline_stroke( path,
                    linecap=linecap_flat,
                    transform=transform_uniform,
                    precision=30,
                    debug=True,
                    fixedangle=None):
    
    &lt;&lt; function comment &gt;&gt;
    
    L = [] # The stroke edge to "the left" of the path.
    R = [] # The stroke edge to "the right" of the path.
    
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
            if i &lt; precision-1:
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
        L.append( (dx1, dy1) )
        R.append( (dx2, dy2) )
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
    L = _ctx.findpath(L)
    R = _ctx.findpath(list(reversed(R)))
    
    # Join the paths in a single path and close the beginning and end.
    # The linecap function defines the style of the join.
    path = _ctx.BezierPath()
    for pt in L: 
        path.append(pt)
    
    linecap(pt, R[0], path) # Close end.
    for pt in R: 
        path.append(pt)
    
    linecap(pt, L[0], path) # Close beginning.
    return path


</t>
<t tx="karstenw.20260813135717.9">def makepath( startx, starty, ctrl1x, ctrl1y, ctrl2x, ctrl2y, endx, endy ):
    path = _ctx.BezierPath()
    path.moveto( startx, starty )
    path.curveto( ctrl1x, ctrl1y, ctrl2x, ctrl2y, endx, endy )
    return path

</t>
<t tx="karstenw.20260813135730.1">


</t>
<t tx="karstenw.20260813140017.1">"""Returns an outlined path from the given path and the current strokewidth.
This will plot vector points along the stroke edge.
Interesting effects can be achieved by modifying the thickness of the path
at each individual point. This can be done with the given transform function:
- It takes three parameters: time, distance, angle.
- It returns a new distance and angle.
The time represents the current place on the path as a number between 0.0-1.0.
The distance represents the thickness of the path."""

</t>
</tnodes>
</leo_file>
