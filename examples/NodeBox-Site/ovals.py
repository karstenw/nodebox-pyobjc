# size(400, 400)

fill(0.8, 0.1, 0.1, 0.333)
stroke(1,0,1)
reset()
for i in range(1600):
    oval(random(10, 940), random(10, 940), 50, 50) #random(5, 50), random(5, 50))
    if i % 100 == 0:
        reset()
    scale(random(0.85, 1.15))
    
