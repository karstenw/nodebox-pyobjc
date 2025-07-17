
from __future__ import print_function

import pprint


fontFamilies = fontfamilies(flat=False)
# pprint.pprint(fontFamilies)

keys = list(fontFamilies.keys())

keys.sort()

fontfamiliesCount = 0
fontMembersCount = 0

for fmname in keys:
    fontfamiliesCount += 1
    print( fmname )
    famMembers = fontFamilies[fmname]
    for member in famMembers:
        fontMembersCount += 1
        print( "    ", member )
        # print "        ", fontFamilies[fmname][member]
    print()

print( "fontfamiliesCount:", fontfamiliesCount )
print( "fontMembersCount:", fontMembersCount )

