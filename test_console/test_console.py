import sys,os,pdb

import nodebox
import nodebox.console
import nodebox.util


examples = os.path.abspath( "../examples" )

alldemos = nodebox.util.filelist( examples, pathonly=False, extensions=[".py",] )

total = errors = 0

for rec in alldemos:
    filepath, size, lastmodified, mode, islink = rec
    if islink:
        continue

    folder, filename = os.path.split( filepath )
    basename, ext = os.path.splitext( filename )
    
    # you don't want that - trust me
    if 'voice' in filename:
        continue
    if 'speech' in filename:
        continue
    
    total += 1
    imgname = basename + '.png'
    imgname = basename + '.jpg'
    
    try:
        s = nodebox.console.make_image( filepath, imgname )
    except Exception as err:
        errors += 1
        print(filepath)
        print(err)
        #pdb.set_trace()
        print()
        print()

print()
print("total:", total)
print("errors:", errors)
