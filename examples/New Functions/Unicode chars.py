


size(1200, 800)

frames = True

fonts = fontnames()
f = choice( fonts )
fsize = 72
print( "Font:", f )

font( f )
fontsize(fsize)
stroke(0)
strokewidth(1)

transform(CORNER)

# unicode from http://leancrew.com/all-this/2017/06/live-and-let-diaeresis/
t1 = "This is Sp\u0131n\u0308al Tap!"

t2 = "This is Spın̈al Tap!"

# you dont want this
t3 = "This is Sp\u0131n\u0308al Pap!"

x, y = 10, 100
fill(0)
dx, dy, t1w, t1h = alltextmetrics(t1, fontsize=fsize, font=f)
text(t1, x+dx, y+dy)

nofill()
if frames:
    rect(x, y-fsize, t1w+dx, t1h+dy)


y = 200
fill(0)
dx, dy, t2w, t2h = alltextmetrics(t2, fontsize=fsize, font=f)
text(t2, x+dx, y+dy)

nofill()
if frames:
    rect(x, y-fsize, t2w+dx, t2h+dy)

y = 300
fill(0)
dx, dy, t3w, t3h = alltextmetrics(t3, fontsize=fsize, font=f)
text(t3, x+dx, y+dy)

nofill()
if frames:
    rect(x, y-fsize, t3w+dx, t3h+dy)


# This script documents an error in unicode text display.
#
# The first and second line align only by manually correcting the x-offset with
# the new and undocumented function alltextmetrics
