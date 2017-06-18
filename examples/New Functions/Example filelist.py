print "The Documents folder with paths:"

mydocs = filelist( "~/Documents")

# using a list and print only once speeds up massively
s = []
for f in mydocs:
    s.append(f)

s = u"\n".join(s)
print s
