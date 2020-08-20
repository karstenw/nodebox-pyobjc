


def circles(x, y,cnt, dist):
    for i in range(cnt):
        r = i * dist
        circle(x, y, r)


var("c2x", NUMBER, 300, 0, 600)
var("d", NUMBER, 1.0, 0.1, 5.0)

nofill()
strokewidth( d )
stroke(0,0,0, 1)

circles(200,250, 40, 5)
circles(c2x,250, 40, 5)

