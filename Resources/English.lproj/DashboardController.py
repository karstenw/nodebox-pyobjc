#
#   DashboardController.py
#
#   Created by Karsten E. Wolf on 30.06.17.
#   Copyright 2017 __MyCompanyName__. All rights reserved.
#

from Foundation import *
from AppKit import *
import objc
class DashboardController (NSObject):
    document = objc.IBOutlet()

    documentWindow = objc.IBOutlet()

    panel = objc.IBOutlet()



