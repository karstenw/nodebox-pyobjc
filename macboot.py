# Startup file for the NodeBox OS X application
# PyObjC requires the startup file to be in the root folder.
# This just imports everything from the nodebox.gui.mac module
# and works from there

import os
#import operator
#import warnings

# for the libraries
import sgmllib
import bs4

# moved to Lubrary
# import numpy

import sqlite3
import zipfile

import hashlib
import base64
import re
import pickle
#import UserList

# needed by matplotlib et al.
# import six
# import pyparsing
# import cycler
# import requests
# import pymongo
# import dateutil
# import copy
# import csv
# import functools
# import itertools
# import gzip
# import io
# import httplib
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


#import PyObjCTools.Debugging
#PyObjCTools.Debugging.installVerboseExceptionHandler()


AppHelper.runEventLoop()
