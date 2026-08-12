sl = ximport("strokelib")

FLAT    = sl.linecap_flat
ROUNDED = sl.linecap_rounded
 
UNIFORM  = sl.transform_uniform
EXPAND   = sl.transform_expand
CONTRACT = sl.transform_contract
SMOOTH   = sl.transform_smooth

ang = 45

nofill()
stroke(0)
strokewidth(1)

path = sl.makepath( 95, 164, 318, 49, 188, 400, 400, 290)
 
strokewidth(30)
path = sl.outline_stroke(path,
                        linecap=ROUNDED, transform=EXPAND,
                        debug=1, fixedangle=ang)
 
strokewidth(1)
fill(0.4, 0, 0.4, 0.25)
drawpath(path)