



def buttonhandler(val, name):
    print 'Oh, the button was pressed...', repr(val), name

def menuhandler( menuitem, name ):
    print 'A menu was selected:', menuitem, name
    
def numberHandler( n, name ):
    print "And the number is:", n, name

def textHandler( s, name ):
    print "And the text is: '%s'" % s, name
    

fonts = fontnames()
default = choice(fonts)

# new style menu var - defaults can now be set
var('Fonts', MENU, default=default, handler=menuhandler, menuitems=fonts)

var('Ein Button', BUTTON, handler=buttonhandler )


# old tsyle menu var - still works if only for compatibility
var('À la carte', MENU, default=menuhandler, value=['Un', 'Deux', 'Trois', 'Eins', 'Zwei', 'Drei'])



# number var old style
var("number1", NUMBER, 0, -200, 200)

# var number new style
var("number2", NUMBER, 0, -200, 200, handler=numberHandler)

var("text1", TEXT, "A text - Old style")
var("text2", TEXT, "A text - Old style", handler=textHandler)



print "number1", number1
print "text1", text1