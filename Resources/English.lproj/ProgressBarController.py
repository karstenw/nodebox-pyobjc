#
#   ProgressBarController.py
#
#   Created by Karsten E. Wolf on 30.06.17.
#   Copyright 2017 __MyCompanyName__. All rights reserved.
#

from Foundation import *
from AppKit import *
import objc
class ProgressBarController (NSWindowController):
    messageField = objc.IBOutlet()

    progressBar = objc.IBOutlet()



