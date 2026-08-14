sl = ximport("strokelib")

FLAT    = sl.linecap_flat
ROUNDED = sl.linecap_rounded
 
UNIFORM  = sl.transform_uniform
EXPAND   = sl.transform_expand
CONTRACT = sl.transform_contract
SMOOTH   = sl.transform_smooth

ang = 0

nofill()
stroke(0)
strokewidth(1)

path = sl.makepath( 95, 164, 318, 49, 188, 400, 400, 290)
 
strokewidth(30)
path = BezierPath()
path.moveto( 154, 457 )
path.lineto( 228, 300 )
path.lineto( 618, 223 )
path.lineto( 751, 546 )


path1 = sl.outline_stroke(path.copy(),
                        linecap=ROUNDED, transform=UNIFORM,
                        precision=37,
                        debug=1, fixedangle=ang)
 
#strokewidth(1)
#fill(0.4, 0, 0.4, 0.25)

strokewidth( 1 )
fill(0.4,0,0.4,0.25)
drawpath(path1)

strokewidth(30)
path2 = sl.outline_stroke(path.copy(),
                        linecap=FLAT, transform=SMOOTH,
                        precision=37,
                        debug=1, fixedangle=ang)
strokewidth( 1 )
fill(0.4,0,0.4,0.25)
drawpath(path2)
