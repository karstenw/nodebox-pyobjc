# Startup file for the NodeBox OS X application
# PyObjC requires the startup file to be in the root folder.
# This just imports everything from the nodebox.gui.mac module
# and works from there

# for the libraries
import sgmllib
import bs4
import numpy
import sqlite3
import zipfile

import hashlib
import base64
import re
import pickle
import UserList


# PIL / Pillow support
import PIL
import PIL.Image
import PIL.ImageFilter
import PIL.ImageChops
import PIL.ImageEnhance
import PIL.ImageOps
import PIL.ImageDraw
import PIL.ImageStat


import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

import nodebox
import nodebox.geo
#import nodebox.geo.pathmatics
import nodebox.graphics
#import nodebox.graphics.bezier
#import nodebox.graphics.cocoa

import nodebox.gui
import nodebox.gui.mac

#import matplotlib

#import sys
#import pprint
#pprint.pprint(sys.path)


#import PyObjCTools.Debugging
#PyObjCTools.Debugging.installVerboseExceptionHandler()


AppHelper.runEventLoop()
