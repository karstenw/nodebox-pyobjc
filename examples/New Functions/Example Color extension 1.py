# Colors can now be defined as hex strings:
#
# Either
#
#   #RRGGBB
#   #RRGGBBAA
#   #RGB
#   #RGBA
#
# or
#   RRGGBB
#   RRGGBBA
#   RGB
#   RGBA

# 3 RRGGBB 
fill( "#ff0000" )
rect(10, 10, 100, 100)

fill( "00ff00" )
rect(110, 10, 100, 100)

fill( "#0000ff" )
rect(210, 10, 100, 100)


# 3 RRGGBBAA
fill( "#ff000080" )
rect(320, 10, 100, 100)

fill( "#00ff0080" )
rect(420, 10, 100, 100)

fill( "0000ff80" )
rect(520, 10, 100, 100)


# 3 RGB
fill( "f00" )
rect(10, 120, 100, 100)

fill( "#0f0" )
rect(110, 120, 100, 100)

fill( "#00f" )
rect(210, 120, 100, 100)


# 3 RGBA
fill( "#f004" )
rect(320, 120, 100, 100)

fill( "0f04" )
rect(420, 120, 100, 100)

fill( "00f4" )
rect(520, 120, 100, 100)


# some text with orange outline in a random font
stroke( "#f80" )
strokewidth( 5 )
fill( "#08f" )
f = choice(fontnames())
print f
font( f, 120 )
text("Hello World!", 10, 520, outline=True)