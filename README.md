<!-- $theme: default -->

![](art/nodeboxlogo_big.png?raw=true)


This is a fork of [NodeBox 1](https://github.com/nodebox/nodebox-pyobjc).

The current version is 1.9.32

Download the compiled app from my [dropbox](http://goo.gl/dZDic5).

As of 2018-05-05 and version 1.9.31 OS X 10.9 is the minimum OS version needed to run NodeBox. Prior Versions should run on 10.6 and above.

As of 2017-05-17 the 32-bit version has been dropped. Please write up an issue if you need one.

Attention!
==========

### The download includes the NodeBox-Library. When first starting NodeBox, go to the preferences and set the Library folder to the included folder.

####Differences from the official version:

1. Additional Commands (they were already in the original source but not active)
	1.  `angle(x0, y0, x1, y1)`
		The angle of line (y0,y0,x1,y1) 
	1.  `distance(x0, y0, x1, y1)`
		The distance between points (x0,y0) and (x1,y1).
	1.  `coordinates(x0, y0, distance, angle)`
		The point at dintance and angle from point(x0,y0)
	1.  `reflect(x0, y0, x1, y1, d=1.0, a=180)
		Too complicated. Watch the example file _Example coordinates 1.py_
	1.  `isqrt(n)` = 1 / sqrt(n)

1. Different behaviour:
	1.  `size(0,0)`  sets size to size of main screen
	1.  Can open shoebot ('.bot') files.  Runs many of the shoebot examples. Incompatibilities exist.
	1.  Colors can be hex strings. 
		-  '#f00' or 'f00' for red
		-  '#f008' or 'f008' for red with alpha=0.5
		-  '#00ff00' or '00ff00'for green
		-  '#00ff001a' or '00ff001a' for green with ca. 10% alpha

	1.  Variables
		-  New var type: `MENU`
		-  The `var` keyword has 2 new parameters: `handler=None` and `menuitems=None`
		-  All var types now can have a handler: `NUMBER`, `TEXT`, `BUTTON`, `BOOLEAN`and `MENU`.
		-  The difference is: When a handler is set, only that function is re-run. The whole script otherwise.
		-  The `MENU` var needs a handler.
		-  The handler=one or two argument-function to be called. If 1-arg: (value,). If 2-arg: (value, name).
		-  menuitems = list or tuple of strings.
		-  See example file `"examples/New Functions/Example var menu 2.py"`


1.  Uses Python 2.7.15 and PyObjC 4.2

1.  Is self containend so it does not depend on an installed Python and therefore runs on different OS versions.

1.  Builds without Xcode ( `python setup.py py2app` )

1.  Uses a different and bigger icon (512px)

1.  Has many additional examples. See folders `Escher`, `geometry/Convex Hull` and `New Functions` .

1.  New function `filelist( folder or list of folders, pathonly=True )` (v1.9.19)
	- Returns a path generator
	- If pathonly is False, it returns a (path, size, lastmodifieddatetime, oct(mode)) generator
	- The Following filenames are ignored: any name starting with '.', any name containing any of: '\r\n\t'.


1.  New function `imagefiles( folder or list of folders, pathonly=True )` (v1.9.19)
	-  Same parameters and restrictions as filelist plus:
	-  filters file extensions for ".pdf .eps .tif .tiff .gif .jpg .jpeg .png"


1.  New function `fontnames()` (v1.9.20)
	-  Returns a list of names from NSFontManager.sharedFontManager().availableFonts().
		Fontnames starting with '.' are ignored.


1.  New function `fontfamilies(flat=False)` (v1.9.20)
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


1.  New graphics primitive `arc(x, y, r, startAngle, endAngle)`
	-  Draws an arc between startAngle and endAngle with center at (x,y) and radius=r.


1.  New function `say(txt, voice=None, outfile=None, wait=True)` (1.9.26).
		Say txt in voice. If voice is None, the default voice is used.
		If outfile is a valid path, the text will be saved as an AIFF file (1.9.27).


1.  New function `voices()`(1.9.26).
		List all voices in a format that can be used by `say()`.


1.  New function `voiceattributes( voice )` (1.9.26).
		return a dict with all attributes about that voice.


1.  New Examples subfolder "New Functions" which contains examples for the new functions.



Since 1.9.21 the adapted Nodebox library is now included in the [download](http://goo.gl/vkuBeV). Open Nodebox, go to preferences and set the Library folder to the included one "NodeBox-Library". The repository is here: [Library](https://github.com/karstenw/Library). 


Latest changes
--------------

2020-07-20 Version 1.9.32 Added circle() for shoebot compatibility. Fractal C extension. See example code.

2018-05-05 Version 1.9.31 First Version built on 10.12. Minimum OS is now 10.9. Fixed some bugs in ditherimage(). Added example for ditherimage().

2017-12-23 Version 1.9.30 New experimental commands `imagepalette()`  `ditherimage()`, `aspectRatio()` 

2017-11-05 Version 1.9.29 say() has now a wait=True optional parameter to make it wait untill the other voices have spoken. Many more adapted examples for the extended app.

2017-09-20 Version 1.9.28 Another Repackaging. Now by making 2 apps. One standart, one with many extra libs. Python is now 2.7.14, PyObjc 3.3a0.

2017-08-14 Version 1.9.27 Repackaging: scipy, matplotlib, sklearn, sympy, pattern moved to a separate archive file which can be downloaded. The folders were removed from the `Library` repository. These are compiled packages. numpy has made it back into the app. I hope this configuration tango is over...

2017-08-05 Version 1.9.26 New functions: `say(txt, voice)`, `voices()` and `voiceattributes( voice )`. Extended var behaviour (handler) for `NUMBER`, `TEXT`, `BOOLEAN` and `BUTTON`. Added scikit-learn and pattern to Library.

2017-07-15 Version 1.9.25 Lots of example updates. No new functionality.

2017-07-13 Version 1.9.24 Bugfix in imports.

2017-07-10 Version 1.9.23 Included [Twyg](http://www.johnnovak.net/twyg/) into the Library. Example files in examples/New Functions/twyg.

2017-07-09 Version 1.9.22 New Variable type MENU. See example file. Included scipy and matplotlib in imports.

2017-06-18 Version 1.9.21 Added shoebot files to document types ('.bot'), color definitions can be hex strings. 

2017-06-12 Version 1.9.20 Added License from origin, isqrt(), fontnames() and fontfamilies()

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
