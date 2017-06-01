print "The Desktop Pictures folder with file tuples:"
print

myimages = imagefiles( "/Library/Desktop Pictures", pathonly=False)

# for the choice later.
myimages = list(myimages)

# get a random image
imagerecord = choice(myimages)


image(imagerecord[0], 30,200)

print "Image:", imagerecord[0]
print "Size:", imagerecord[1]
print "last modified:", str(imagerecord[2])
print "Mode:", imagerecord[3]
print "Is a link:", imagerecord[4]

print imagerecord