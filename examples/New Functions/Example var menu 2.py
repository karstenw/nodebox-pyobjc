



def buttonhandler():
    print 'Oh, the button was pressed...'

def menuhandler( menuitem ):
    print 'A menu was selected:', menuitem
    
    
    

fonts = fontnames()

var('Fonts', MENU, default=menuhandler, value=fonts)

var('Ein Button', BUTTON, value=buttonhandler )

var('À la carte', MENU, default=menuhandler, value=['Un', 'Deux', 'Trois', 'Eins', 'Zwei', 'Drei'])
