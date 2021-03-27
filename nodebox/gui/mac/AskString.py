__all__ = ["AskStringWindowController", "AskString"]

import objc

import Foundation

#import AppKit
#NSApp = AppKit.NSApplication

# class defined in AskString.xib
class AskStringWindowController(AppKit.NSWindowController):
    questionLabel = objc.IBOutlet()
    textField = objc.IBOutlet()

    def __new__(cls, question, resultCallback, default="", parentWindow=None):
        self = cls.alloc().initWithWindowNibName_("AskString")
        self.question = question
        self.resultCallback = resultCallback
        self.default = default
        self.parentWindow = parentWindow
        if self.parentWindow is None:
            self.window().setFrameUsingName_("AskStringPanel")
            self.setWindowFrameAutosaveName_("AskStringPanel")
            self.showWindow_(self)
        else:
            #NSApp().beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_( self.window(), self.parentWindow, None, None, 0)
            self.parentWindow().beginSheet_completionHandler_( self.window(), None )
            # (void)beginSheet_completionHandler_(NSWindow *)sheetWindow  completionHandler:(void (^)(NSModalResponse returnCode))handler;
        self.retain()
        return self

    def windowWillClose_(self, notification):
        self.autorelease()

    def awakeFromNib(self):
        self.questionLabel.setStringValue_(self.question)
        self.textField.setStringValue_(self.default)

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


def AskString(question, resultCallback, default="", parentWindow=None):
    AskStringWindowController(question, resultCallback, default, parentWindow)
