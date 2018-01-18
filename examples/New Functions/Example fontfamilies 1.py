import pprint


fontFamilies = fontfamilies(flat=False)
# pprint.pprint(fontFamilies)

keys = fontFamilies.keys()

keys.sort()

for fmname in keys:
    print fmname
    famMembers = fontFamilies[fmname]
    for member in famMembers:
        print "    ", member
        # print "        ", fontFamilies[fmname][member]
    print
