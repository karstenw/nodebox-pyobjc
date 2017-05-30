print "The Pictures folder with paths:"

myimages = filelist( "~/Pictures")

for f in myimages:
    print f

print 
print '-' * 40
print 

print "The Pictures folder with file tuples:"

myimages = filelist( "~/Pictures", pathonly=False)

for f in myimages:
    print f
