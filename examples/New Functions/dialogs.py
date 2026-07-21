
import pprint
pp = pprint.pprint

# download a url and display headers and content
if 0:
    print("\nreadURL():")
    r = readURL("http://support.nodebox.net/discussions/nodebox-1")
    
    pp( r['headers'], width=300)
    print( makeunicode(r['content']))

# get a single python file
print("\ngetFileDialog( multiple=False, types=('py',), asURLs=False ):")
pp( getFileDialog( multiple=False, types=('py',), asURLs=False  ), width=300)


# get a folder
print("\ngetFolderDialog( multiple=False, asURLs=False ):")
pp( getFolderDialog( multiple=False, asURLs=False ), width=300)

# get anything
print("\ngetAnyDialog(multiple=True, types=None, asURLs=True):")
pp( getAnyDialog( multiple=True, types=None, asURLs=True ), width=300)

# show error dialog
print()
pp( errorDialog("GET", "OUT!") )


