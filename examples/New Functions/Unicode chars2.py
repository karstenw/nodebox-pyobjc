size(1200, 800)

f = "Arial"
fsize = 36
x, y = 10, 100
maxwidth = 500

font( f )
fontsize(fsize)
stroke(0)
strokewidth(1)

transform(CORNER)
align(LEFT)


t1 = "äöüÄÖÜß¡“¶¢[]|{}≠¿«∑€®†Ω¨⁄øπ•±å‚∂ƒ©ªº∆\n¥≈ç√∫~µ∞…–‘’"

fill(0)
dx, dy, t1w, t1h = alltextmetrics(t1, width=maxwidth, fontsize=fsize, font=f)
print dx,dy, t1w, t1h
text(t1, x+dx, y+dy, width=maxwidth)

nofill()
rect(x, y-fsize, t1w+dx, t1h+dy)
