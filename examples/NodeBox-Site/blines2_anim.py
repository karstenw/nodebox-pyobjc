# set this to your screen size and watch it fullscreen
size(1280, 1024)

boids = ximport("boids")
cornu = ximport("cornu")

flock = boids.flock(10, 0, 0, WIDTH, HEIGHT)

def setup():
    pass

speed(12)

n = 9

def draw():
    background(0.1, 0.1, 0.0)
    nofill()

    for i in range(n):
        flock.update(shuffled=False)

        # Each flying boid is a point.
        points = []
        for boid in flock:
            points.append((boid.x, boid.y))

        # Relativise points for Cornu.
        for j in range(len(points)):
            x, y = points[j]
            x /= 1.0 * WIDTH
            y /= 1.0 * HEIGHT
            points[j] = (x,y)
        # points = [ (x,y) for ]


        t = float(i) / n
        stroke(0.9, 0.9, 4*t, 0.6*t)
        cornu.drawpath(points, tweaks=0)
