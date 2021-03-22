#
#   NodeBoxPreferencesController.py
#
#   Created by Karsten E. Wolf on 30.06.17.
#   Copyright 2017 __MyCompanyName__. All rights reserved.
#

from Foundation import *
from AppKit import *
import objc

class NodeBoxPreferencesController (NSWindowController):

    commentsColorWell = objc.IBOutlet()

    fontPreview = objc.IBOutlet()

    libraryPath = objc.IBOutlet()

    funcClassColorWell = objc.IBOutlet()

    keywordsColorWell = objc.IBOutlet()

    stringsColorWell = objc.IBOutlet()


    @objc.IBAction
    def updateColors_(self, sender):
        pass

    @objc.IBAction
    def chooseFont_(self, sender):
        pass

    @objc.IBAction
    def chooseLibrary_(self, sender):
        pass

    @objc.IBAction
    def changeFont_(self, sender):
        pass


