import sys,os,pdb

import nodebox
import nodebox.console
import nodebox.util



def uniquename(folder, basename, ext='',
               noofdigits=3, startindex=1, separator='_',
               alwaysenumerate=False):
    #
    folder = os.path.abspath( folder )
    if not alwaysenumerate:
        filename = basename + ext
        path = os.path.join(folder, filename )
        if not os.path.exists( path ):
            return path
    i = startindex
    while True:
        serialstring = str(i).rjust(noofdigits, "0")
        filename = basename + separator + serialstring + ext
        fullpath = os.path.join(folder, filename)
        if not os.path.exists(fullpath):
            return fullpath
        i += 1
        if i >= 10**noofdigits:
            nfill = noofdigits + 1


def uniquepath(folder,  filenamebase, ext, nfill=1,
                        startindex=1, sep="_",
                        always=False):
    # old version. compatibility 
    return uniquename(folder, filenamebase, ext=ext, noofdigits=nfill,
                              startindex=1,
                              separator=sep,
                              alwaysenumerate=always)



examples = os.path.abspath( "../examples" )
imgfolder = os.path.abspath( "./temp" )
if not os.path.exists( imgfolder ):
    os.makedirs( imgfolder )

# examples = os.path.abspath( "../examples/Third party examples/shoebot" )

print("examples:", examples)

alldemos = nodebox.util.filelist( examples,
                                  pathonly=False,
                                  extensions=['.py','.bot', '.pv'] )

total = errors = 0

ignorefiles = ("Example speech 3 allvoices.py", "Example speech 4 allvoicefiles.py", "Example filelist.py")

pdb.set_trace()

for rec in alldemos:
    filepath, size, lastmodified, mode, islink = rec
    if islink:
        continue
    
    folder, filename = os.path.split( filepath )
    basename, ext = os.path.splitext( filename )
    
    # you don't want that - trust me
    if filename in ignorefiles:
        continue
    
    
    total += 1
    imgname = basename + '.png'
    imgname = basename + '.jpg'
    
    imgpath = uniquepath(imgfolder, basename, ".jpg")
    # imgpath = os.path.join( imgfolder, imgname )
    
    try:
        s = nodebox.console.make_image( filepath, imgpath )
    except Exception as err:
        errors += 1
        print(filepath)
        print(err)
        # pdb.set_trace()
        print()
        print()
    

print()
print("total:", total)
print("errors:", errors)
