# Zapfun
# from
# https://siafoo.net/snippet/173
# via https://web.archive.org/web/20110203052513/https://siafoo.net/snippet/173


size( 1440, 1024)

fill(0.2)
rect(0,0,WIDTH,HEIGHT)

fill(1)
stroke(0.2)
strokewidth(1)
font('Zapfino')

for i in range(400):
    fontsize(random(30,400))
    rotate(random(360))  
    chars = 'absdefghijklmnopqrstuvwxyz'
    p = textpath(choice(chars),
                 random(-50, WIDTH  + 100),
                 random(-50, HEIGHT + 100))
    drawpath(p)

