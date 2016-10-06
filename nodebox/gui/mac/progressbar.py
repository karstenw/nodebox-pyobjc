import objc
import AppKit
NSDefaultRunLoopMode = AppKit.NSDefaultRunLoopMode


class ProgressBarController(AppKit.NSWindowController):
    messageField = objc.IBOutlet()
    progressBar = objc.IBOutlet()
    
    def init(self):
        AppKit.NSBundle.loadNibNamed_owner_("ProgressBarSheet", self)
        return self

    def begin_maxval_(self, message, maxval):
        self.value = 0
        self.message = message
        self.maxval = maxval
        self.progressBar.setMaxValue_(self.maxval)
        self.messageField.cell().setTitle_(self.message)
        parentWindow = AppKit.NSApp().keyWindow()
        AppKit.NSApp().beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(self.window(), parentWindow, self, None, 0)
        
    def inc(self):
        self.value += 1
        self.progressBar.setDoubleValue_(self.value)
        date = AppKit.NSDate.dateWithTimeIntervalSinceNow_(0.01)
        AppKit.NSRunLoop.currentRunLoop().acceptInputForMode_beforeDate_(NSDefaultRunLoopMode, date)
        
    def end(self):
        AppKit.NSApp().endSheet_(self.window())
        self.window().orderOut_(self)
        