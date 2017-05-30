print "The Documents folder with paths:"

mydocs = filelist( "~/Documents")

for f in mydocs:
    print f

print 
print '-' * 40
print 

print "The Documents folder with file tuples:"

mydocs = filelist( "~/Documents", pathonly=False)

for f in mydocs:
    print f
