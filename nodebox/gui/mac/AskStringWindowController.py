import sys, os, pdb

import objc

import Foundation

import AppKit
NSApp = AppKit.NSApplication

def AskString(question, resultCallback, default="", parentWindow=None):
    p = AskStringWindowController.alloc().init()
    p.setup_cb_default_parent_(question, resultCallback, default, parentWindow)


# class defined in AskString.xib
class AskStringWindowController(AppKit.NSWindowController):
    questionLabel = objc.IBOutlet()
    textField = objc.IBOutlet()

    def init(self):

        self = self.initWithWindowNibName_( "AskString" )
        self.question = u"" #question
        self.resultCallback = None # resultCallback
        self.default = u"" #default
        self.parentWindow = None #parentWindow
        self.retain()
        return self

    def setup_cb_default_parent_( self, question, resultCallback, default, parentWindow):
        self.question = question
        self.resultCallback = resultCallback
        self.default = default
        self.parentWindow = parentWindow
        self.window().setFrameUsingName_( u"AskStringPanel" )
        self.setWindowFrameAutosaveName_( u"AskStringPanel" )
        self.showWindow_( self.window() )

    def windowWillClose_(self, notification):
        self.autorelease()
        return objc.super(AskStringWindowController, self).windowWillClose_(
                                                    self, notification)

    def awakeFromNib(self):
        self.questionLabel.setStringValue_( self.question )
        self.textField.setStringValue_( self.default )
        return objc.super(AskStringWindowController, self).awakeFromNib()

    def done(self):
        if self.parentWindow is None:
            self.close()
        else:
            sheet = self.window()
            # NSApp().endSheet_(sheet)
            sheet.endSheet_(self)
            sheet.orderOut_(self)

    @objc.IBAction
    def ok_(self, sender):
        value = self.textField.stringValue()
        self.done()
        self.resultCallback(value)

    @objc.IBAction
    def cancel_(self, sender):
        self.done()
        self.resultCallback(None)


    def windowDidLoad( self ):
        print("AskStringWindowController.windowDidLoad()")
        print( "self.window()", self.window() )
        return objc.super(AskStringWindowController, self).windowDidLoad()


    def windowWillLoad( self ):
        # pdb.set_trace()
        print("AskStringWindowController.windowWillLoad()")
        return objc.super(AskStringWindowController, self).windowWillLoad()

