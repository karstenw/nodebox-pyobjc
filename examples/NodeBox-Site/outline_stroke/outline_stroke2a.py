sl = ximport("strokelib")

FLAT    = sl.linecap_flat
ROUNDED = sl.linecap_rounded
 
UNIFORM  = sl.transform_uniform
EXPAND   = sl.transform_expand
CONTRACT = sl.transform_contract
SMOOTH   = sl.transform_smooth

nofill()
stroke(0)
strokewidth(1)

basepath = sl.makepath( 95, 164, 318, 49, 188, 400, 400, 290)
 
strokewidth(30)
path = sl.outline_stroke(basepath.copy(), linecap=ROUNDED, transform=CONTRACT, debug=True)
 
strokewidth(1)
fill(0.4, 0, 0.4, 0.25)
drawpath(path)

if 1:
    strokewidth(30)
    path = sl.outline_stroke(basepath.copy(), linecap=ROUNDED, transform=EXPAND, debug=True)
 
    strokewidth(1)
    fill(0.4, 0, 0.4, 0.25)
    drawpath(path)
