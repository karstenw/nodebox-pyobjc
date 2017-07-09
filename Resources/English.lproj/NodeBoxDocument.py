#
#   NodeBoxDocument.py
#
#   Created by Karsten E. Wolf on 30.06.17.
#   Copyright 2017 __MyCompanyName__. All rights reserved.
#

from Foundation import *
from AppKit import *
import objc
class NodeBoxDocument (NSDocument):
    animationSpinner = objc.IBOutlet()

    dashboardController = objc.IBOutlet()

    exportImageAccessory = objc.IBOutlet()

    exportImageFormat = objc.IBOutlet()

    exportImagePageCount = objc.IBOutlet()

    exportMovieAccessory = objc.IBOutlet()

    exportMovieFps = objc.IBOutlet()

    exportMovieFrames = objc.IBOutlet()

    exportSheet = objc.IBOutlet()

    exportSheetIndicator = objc.IBOutlet()

    graphicsView = objc.IBOutlet()

    outputView = objc.IBOutlet()

    pageCount = objc.IBOutlet()

    pageCountAccessory = objc.IBOutlet()

    textView = objc.IBOutlet()

    variablesController = objc.IBOutlet()

    window = objc.IBOutlet()

    @objc.IBAction
    def buildInterface_(self, sender):

    @objc.IBAction
    def copyImageAsPDF_(self, sender):

    @objc.IBAction
    def exportAsImage_(self, sender):

    @objc.IBAction
    def exportAsMovie_(self, sender):

    @objc.IBAction
    def exportImageFormatChanged_(self, sender):

    @objc.IBAction
    def printDocument_(self, sender):

    @objc.IBAction
    def runFullscreen_(self, sender):

    @objc.IBAction
    def runScript_(self, sender):

    @objc.IBAction
    def stopScript_(self, sender):

    @objc.IBAction
    def zoomIn_(self, sender):

    @objc.IBAction
    def zoomOut_(self, sender):

    @objc.IBAction
    def zoomToFit_(self, sender):

    @objc.IBAction
    def zoomToTag_(self, sender):

