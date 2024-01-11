
nofill()
stroke(0)

radius = 250
startangle = 270
endangle = 0

x, y = 300, 400

arc( x, y, radius, startangle, endangle)

line(x, y, x, y-radius)
line(x, y, x+radius, y)

arc( x, y, radius, startangle-180, endangle-180)
