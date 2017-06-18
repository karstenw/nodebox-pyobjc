![](art/nodeboxlogo_big.png?raw=true)


This is a personal fork of NodeBox 1.


Download the compiled app from my dropbox: [http://goo.gl/vkuBeV](http://goo.gl/vkuBeV).


As of 2017-05-17 the 32-bit version has been dropped. Please write up an issue if you need one.


Differences from the official version:

1. Additional Commands (they were already in the original source but not active)
	1.  angle(x0, y0, x1, y1)
	1.  distance(x0, y0, x1, y1)
	1.  coordinates(x0, y0, distance, angle)
	1.  reflect(x0, y0, x1, y1, d=1.0, a=180)

1. Different behaviour:
	1.  `size(0,0)`  sets size to size of main screen
	1.  Can open shoebot ('.bot') files.  Runs ca. 80% of the shoebot examples.
	1.  Colors can be hex strings. 
		-  '#f00' or 'f00' for red
		-  '#f008' or 'f008' for red with alpha=0.5
		-  '#00ff00' or '00ff00'for green
		-  '#00ff001a' or '00ff001a' for green with ca. 10% alpha

1.  Uses Python 2.7.13 and PyObjC 3.2a1

1.  Is self containend so it does not depend on an installed Python and therefore runs on different OS versions.

1.  Builds without Xcode (python setup.py py2app)

1.  Uses a different and bigger icon (512px)

1.  Has some additional examples. See folders `Escher`, `geometry/Convex Hull` and `New Functions` .

1.  New function filelist( folder or list of folders, pathonly=True )
	- Returns a path generator
	- If pathonly is False, it returns a (path, size, lastmodifieddatetime, oct(mode)) generator
	- The Following filenames are ignored: any name starting with '.', any name containing any of: '\r\n\t'.

1.  New function imagefiles( folder or list of folders, pathonly=True )
	-  Same parameters and restrictions as filelist plus:
	-  filters file extensions for ".pdf .eps .tif .tiff .gif .jpg .jpeg .png"

1.  New function fontnames()
	-  Returns a unfiltered list of names from NSFontManager.sharedFontManager().availableFonts()

1.  New function fontfamilies(flat=False)
	-  Return a dict with [FontFamily][STYLE]-> FontRecord
	-  if parameter flat=True returns a list of FontRecord
	-  A FontRecord has the following attributes:
		-  psname - the postscript name, which can be used for font()
		-  familyname - the font family name
		-  style - the style name
		-  weight - the font weight
		-  traits - an int that represents the fonts traits
		-  traitnames - the traits converted to a list of names: (italic, bold, unbold,
			nonstandardcharacterset", narrow, expanded, condensed, smallcaps,
			poster, compressed, fixedpitch, unitalic)

1.  New graphics primitive `arc(self, x, y, r, startAngle, endAngle)`
	-  Draws an arc between startAngle and endAngle with center at (x,y) and radius=r.

1.  New Examples subfolder "New Functions" which contains examples for the new functions.



The adapted Nodebox library is available here: [Library](https://github.com/karstenw/Library). Download as zip, unpack, rename to 'NodeBox' and move it to ~/Library/Application Support/.



Latest changes
--------------

2017-05-28 Version 1.9.19. Added setup_console.py. If all needed libraries are installed, NodeBox can be installed as a standard Python lib. Scripts can be executed without the app.

2017-05-22 Version 1.9.18. Added filelist and imagefiles generators.

2017-05-20 Version 1.9.17. Added zipfile for support of patched color library. [Shoebot zipped color library patch](https://github.com/shoebot/shoebot/commit/b2b9c43b28acb9312ca2a0557cc8728fc49a47bb).

2017-05-20 Version 1.9.16. Added preference for Library Path. It can be anywhere now. Added help menu item to open the Library path.

2017-05-17 Version 1.9.15. Upgraded to Python 2.7.13. Dropped the 32-bit version.

2016-10-06 Version 1.9.14. Upgraded to Python 2.7.12 and PyobjC 3.2a1.






The original README:
--------------------


NodeBox
=======
NodeBox is an application used in graphic design research. It provides
an interactive Python environment where you can create two-dimensional
graphics. NodeBox scripts can create PDFs or QuickTime movies that can 
contain anything from simple geometrical shapes to fully-fledged bitmaps,
vector images and text.

NodeBox is mostly meant to design and explore generative design and
animation. It features several ways to manipulate parameters inside 
of a program: it contains an interface builder and an on-the-fly value 
changing gizmo called the throttle.

  http://nodebox.net/

Credits
-------
NodeBox itself is written by Frederik De Bleser. (frederik@burocrazy.com)
The NodeBox manual is written by Tom De Smedt. (tomdesmedt@organisms.be)

NodeBox is a fork of DrawBot (http://drawbot.com) by Just van Rossum (just@letterror.com),
which is released under a MIT-style license.

Contributing
------------
The NodeBox source is available on GitHub:

  http://github.com/nodebox/nodebox-pyobjc
