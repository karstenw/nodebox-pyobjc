import pprint


fontFamilies = fontfamilies(flat=True)
# pprint.pprint(fontFamilies)

fontFamilies.sort()

for fontRec in fontFamilies:
    print fontRec
