
from __future__ import print_function


fonts = fontnames()

fonts.sort()
s = u"\n".join( fonts )

print( s )
print( "\nFonts:", len(fonts) )
