# Startup file for the NodeBox OS X application
# PyObjC requires the startup file to be in the root folder.
# This just imports everything from the nodebox.gui.mac module
# and works from there

from __future__ import print_function


import os
import operator
import warnings
import io
import json
import optparse

import importlib
# import _multibytecodec

import sqlite3
import zipfile
import tarfile
import gzip

import hashlib
import base64
import re
import pickle
import pydoc

# pattern lib
import csv
import functools
import itertools
import codecs
import calendar
import types
import feedparser

import encodings

# import requests


# for the libraries
import bs4

# moved to Library
import numpy


try:
    import planar
except:
    pass

# wn
import httpx
import tomli
import anyio
import certifi
import httpcore
import idna
import sniffio
import h11

# nltk
import regex



# PIL / Pillow support
import PIL
import PIL.Image
import PIL.ImageFilter
import PIL.ImageChops
import PIL.ImageEnhance
import PIL.ImageOps
import PIL.ImageDraw
import PIL.ImageStat

import cairo

import objc
import Foundation
import AppKit

import Quartz
import Quartz.QuartzCore
import AVFoundation
import AVKit
import LaunchServices
import WebKit

import CoreLocation



from PyObjCTools import AppHelper

import PyObjCTools.Debugging
PyObjCTools.Debugging.installVerboseExceptionHandler()

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
