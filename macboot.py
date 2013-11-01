# Startup file for the NodeBox OS X application
# PyObjC requires the startup file to be in the root folder.
# This just imports everything from the nodebox.gui.mac module
# and works from there

import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

import nodebox
import nodebox.geo
import nodebox.geo.pathmatics
import nodebox.graphics
import nodebox.graphics.bezier
import nodebox.graphics.cocoa
import nodebox.gui

import nodebox.gui.mac

import sgmllib
#import numeric


import PyObjCTools.Debugging
PyObjCTools.Debugging.installVerboseExceptionHandler()


AppHelper.runEventLoop()
