# Startup file for the NodeBox OS X application
# PyObjC requires the startup file to be in the root folder.
# This just imports everything from the nodebox.gui.mac module
# and works from there

from __future__ import print_function


import os
import operator
import warnings
import io

# for the libraries

import bs4

# moved to Library
import numpy

import sqlite3
import zipfile

import hashlib
import base64
import re
import pickle


# pattern lib
import csv
import functools
import itertools
import codecs
import calendar
import types

import encodings
import imagewells

import json
import requests

import planar

# currently not in py2
# import MySQLdb # lib/pattern
# import locale


#import UserList

# needed by matplotlib et al.
# import six
# import pyparsing
# import cycler
# import pymongo
# import dateutil
# import copy
# import gzip
# import http
# import http.client
# import http.server
# import urllib
# import urlparse
# import decimal
# import gettext


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
#import PyObjCTools.Debugging
#PyObjCTools.Debugging.installVerboseExceptionHandler()

import nodebox
import nodebox.geo
import nodebox.graphics
import nodebox.gui
import nodebox.gui.mac

# pattern
# import xml.etree
# import xml.etree.cElementTree

# Do not import these here; they are in the app and are imported by scripts
# If you import here, 10.6 breaks
# import scipy
# import matplotlib
# import cairo

# Twyg is in Library
# import twyg


# py3 stuff
py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int

if not py3:
    import new
    import httplib



AppHelper.runEventLoop()
