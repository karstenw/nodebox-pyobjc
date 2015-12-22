This is a personal fork of NodeBox1.

Download the app from my dropbox: [http://goo.gl/vkuBeV](http://goo.gl/vkuBeV)


Differences from the official version:

1. Additional Commands
  1.  angle(x0, y0, x1, y1)
  1.  distance(x0, y0, x1, y1)
  1.  coordinates(x0, y0, distance, angle)
  1.  reflect(x0, y0, x1, y1, d=1.0, a=180)

2. Different behaviour:
  1.  size(0,0) sets to main screen size

3. Uses Python 2.7.9 and PyObjC 3.1b1

4. is self containend

5. Builds without Xcode (python setup.py py2app)

6. Uses a different and bigger icon (512px)

7. Has some additional Escher examples

8. Additional 64-bit app which runs on OSX 10.6 & 10.10 (10.7, 10.8 and 10.9 due to lack of installment not tested)

![Image](art/nodeboxlogo_big.png?raw=true)


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
