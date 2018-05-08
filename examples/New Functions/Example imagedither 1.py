import os
import random as rnd
import time
import PIL


# choose a desktop image
filetuples = imagefiles( "/Library/Desktop Pictures", False )

# filter for images ≥ 50000 bytes size.
images = []
for t in filetuples:
    path, filesize, lastmodified, mode, islink = t
    if filesize < 50000:
        continue
    images.append( path )
    
# aktivieren für wiederholbare zufalls folge
# rnd.seed(2)

img = choice( images )

def handletype(val, name):
    global Dithertype
    Dithertype = val
    convert(img, Dithertype, Threshhold)

def handlethreshhold(val, name):
    global Threshhold
    Threshhold = int(round(val, 0))
    convert(img, Dithertype, Threshhold)

var('Dithertype', MENU, default=handletype, value=dithertypes())

var('Threshhold', NUMBER, 127, 0, 255, handler=handlethreshhold)


def convert(img, dithtype, threshhold):
    # convert to dithered 
    starttime = time.time()
    path = ditherimage( img, dithtype, threshhold )
    stoptime = time.time()
    # canvas der Bildgrösse anpassen
    w,h = imagesize( path )
    size(w,h)
    image(path, 0,0)
    print "IN:", img
    print "OUT:", path
    print "Dithertype:", Dithertype
    print "Threshhold:", Threshhold
    w,h = imagesize( img )
    print "SIZE:", w, h
    print "TIME: %.4f" % ( round(stoptime-starttime, 4) )
    print
    os.remove(path)

convert(img, Dithertype, Threshhold)
