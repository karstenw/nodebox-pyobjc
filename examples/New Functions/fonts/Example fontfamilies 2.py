
from __future__ import print_function

import pprint


# flat == True gives a list of FontRecords

# flat == False gives dict fontname -> fontstyle -> list of FontRecord

flatFonts = fontfamilies(flat=True)

# filter all fixed width fonts
fixed = []

for fontRec in flatFonts:
    if u'fixedpitch' in fontRec.traitnames:
        fixed.append( fontRec )

print()
print( "All fixed width fonts:" )
print()
pprint.pprint( fixed )

print()
print( "font families:", len(fontFamilies) )
print( "fonts:", len(flatFonts) )
print( "fixed width fonts:", len(fixed) )