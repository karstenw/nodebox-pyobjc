print "The Documents folder with paths:"

mydocs = filelist( "~/Documents")

for f in mydocs:
    print f

print 
print '-' * 40
print 

print "The Documents folder with file tuples:"

mydocs = filelist( "~/Documents", pathonly=False)


f = open("documents.txt", 'w')
s = u"%s\t%s\t%s\t%s\t%s\n"
for fle in mydocs:
    t = s % fle
    f.write( t.encode("utf-8") )
    
f.close()

