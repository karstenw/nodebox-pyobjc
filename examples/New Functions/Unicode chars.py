size(1200, 800)

fonts = fontnames()
f = "Arial" #choice( fonts )
fsize = 72
# print "Font:", f

font( f )
fontsize(fsize)
stroke(0)
strokewidth(1)


# unicode from http://leancrew.com/all-this/2017/06/live-and-let-diaeresis/

# The u"" notation is needed for unicode expansions
t1 = u"This is Sp\u0131n\u0308al Tap!"

# no expansions, u"" not needed; 
t2 = "This is Spın̈al Tap!"

# you dont want this
t3 = "This is Sp\u0131n\u0308al Pap!"
t3w = textwidth(t3, fontsize=72, font=f)
print textmetrics(t2, fontsize=72, font=f)


x, y = 50, 100
fill(0)
text(t1, x, y)

nofill()
t1w, t1h = textmetrics(t1, fontsize=fsize, font=f)
rect(x, y-fsize, t1w, t1h)


y = 200
fill(0)
text(t2, x, y)

nofill()
t2w, t2h = textmetrics(t2, fontsize=fsize, font=f)
rect(x, y-fsize, t2w, t2h)

y = 300
fill(0)
text(t3, x, y)

nofill()
t3w, t3h = textmetrics(t3, fontsize=fsize, font=f)
rect(x, y-fsize, t3w, t3h)


# This script documents an error. The first two lines should match the frames

