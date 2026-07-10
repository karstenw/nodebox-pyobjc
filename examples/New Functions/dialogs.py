
import pprint
pp = pprint.pprint


print("readURL_():")
r = readURL("https://www.danisch.de/blog/")

pp( r['headers'], width=300)
print( makeunicode(r['content']))

print("getOpenDialog():")
pp( getOpenDialog(), width=300)

print("getFileDialog():")
pp( getFileDialog( multiple=False ), width=300)

print("getFolderDialog():")
pp( getFolderDialog( multiple=False ), width=300)

pp( errorDialog("GET", "OUT!") )


