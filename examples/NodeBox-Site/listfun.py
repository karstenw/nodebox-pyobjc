size(500, 500)
background(0.2)

words = "Lists are fun and even much faster that frontier".split()

colors = [color(1,0,0), color(1,1,1), color(0,0,0), color(0,1,0), color(0,0,1), color(0,1,1), color(1,1,0)]
 
for i in range(400):
 
    x = random(WIDTH)
    y = random(HEIGHT)
    rotate(random(360))
    fontsize(random(12,72))
 
    fill(choice(colors))
    text(choice(words), x, y)