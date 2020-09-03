

def params(val, name):
    global x, y,r1,r2
    # global scope needs updating.
    val = int(round(val,0))
    if name == "x":
        x = round(val,1)
    elif name == "y":
        y = round(val,1)
    elif name == "r1":
        r1 = round(val,1)
    elif name == "r2":
        r2 = round(val,1)
    paintcircle(x,y,r1,r2)


def paintcircle(cx, cy, rw, rh):
    stroke(0.2)
    fill(0,0.5,0,0.5)
    strokewidth(2)
    circle(cx, cy, rw, rh)
    # print(cx, cy, rw, rh)

var("x", NUMBER, default=50, min=10, max=301, handler=params)
var("y", NUMBER, default=50, min=10, max=301, handler=params)
var("r1", NUMBER, default=50, min=10, max=300, handler=params)
var("r2", NUMBER, default=50, min=10, max=300, handler=params)

paintcircle(x,y,r1,r2)
