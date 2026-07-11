
import pprint
pp = pprint.pprint

# download a url and display headers and content
if 0:
    print("readURL_():")
    r = readURL("http://support.nodebox.net/discussions/nodebox-1")
    
    pp( r['headers'], width=300)
    print( makeunicode(r['content']))

# get a single python file
print("getFileDialog():")
pp( getFileDialog( multiple=False, types=('py',)  ), width=300)


# get a folder
print("getFolderDialog():")
pp( getFolderDialog( multiple=False ), width=300)

# show error dialog
pp( errorDialog("GET", "OUT!") )


