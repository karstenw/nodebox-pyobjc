This is a personal fork of NodeBox1.

Download the compiled app from my dropbox: [http://goo.gl/vkuBeV](http://goo.gl/vkuBeV)
Versions for 32 and 64-bit are available.


Differences from the official version:

1. Additional Commands (they were already in the original source but not active)
  1.  angle(x0, y0, x1, y1)
  1.  distance(x0, y0, x1, y1)
  1.  coordinates(x0, y0, distance, angle)
  1.  reflect(x0, y0, x1, y1, d=1.0, a=180)

1. Different behaviour:
  1.  `size(0,0)`  sets size to size of main screen

1.  Uses Python 2.7.12 and PyObjC 3.2a1

1.  Is self containend so it does not depend on an installed Python

1.  Builds without Xcode (python setup.py py2app)

1.  Uses a different and bigger icon (512px)

1.  Has some additional examples. See folders `Escher` and `geometry/Convex Hull`.

1.  Additional 64-bit app which runs on OSX 10.6 & 10.10 (10.7, 10.8 and 10.9 due to lack of installation not tested)



The adapted Nodebox library is available here: [Library](https://github.com/karstenw/Library). Download as zip and unpack the contents into ~/Library/Application Support/NodeBox.


Latest changes
--------------
2016-10-06 Version 1.9.14. Upgraded to Python 2.7.12 and PyobjC 3.2a1.


![](art/nodeboxlogo_big.png?raw=true)




The original README:
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
