#
#   AskStringWindowController.py
#
#   Created by Karsten E. Wolf on 30.06.17.
#   Copyright 2017 __MyCompanyName__. All rights reserved.
#

from Foundation import *
from AppKit import *
import objc
class AskStringWindowController (NSWindowController):

    questionLabel = objc.IBOutlet()

    textField = objc.IBOutlet()

    @objc.IBAction
    def cancel_(self, sender):

    @objc.IBAction
    def ok_(self, sender):

