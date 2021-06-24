import pdb
import AppKit

NSObject = AppKit.NSObject
NSFont = AppKit.NSFont
NSMiniControlSize = AppKit.NSMiniControlSize
NSOnState = AppKit.NSOnState
NSOffState = AppKit.NSOffState
NSTextField = AppKit.NSTextField
NSRightTextAlignment = AppKit.NSRightTextAlignment
NSSlider = AppKit.NSSlider
NSMiniControlSize = AppKit.NSMiniControlSize
NSGraphiteControlTint = AppKit.NSGraphiteControlTint
NSButton = AppKit.NSButton
NSSwitchButton = AppKit.NSSwitchButton
NSSmallControlSize = AppKit.NSSmallControlSize
NSPopUpButton = AppKit.NSPopUpButton


import objc

from nodebox import graphics

# just to make the next lines print better
smfontsize = NSFont.smallSystemFontSize()
smctrlsize = NSFont.systemFontSizeForControlSize_(NSMiniControlSize)

SMALL_FONT = NSFont.systemFontOfSize_(smfontsize)
MINI_FONT = NSFont.systemFontOfSize_(smctrlsize)

# class defined in NodeBoxDocument.xib
class DashboardController(NSObject):
    document = objc.IBOutlet()
    documentWindow = objc.IBOutlet()
    panel = objc.IBOutlet()

    def clearInterface(self):
        for s in list(self.panel.contentView().subviews()):
            s.removeFromSuperview()

    def numberChanged_(self, sender):
        var = self.document.vars[sender.tag()]
        var.value = sender.floatValue()
        if var.handler is not None:
            args = [var.value,var.name]
            if var.handler.func_code.co_argcount < 2:
                args = [var.value]
            self.document.fastRun_newSeed_args_(var.handler, False, args)
        else:
            self.document.runScript(compile=False, newSeed=False)

    def textChanged_(self, sender):
        var = self.document.vars[sender.tag()]
        var.value = sender.stringValue()
        if var.handler is not None:
            args = [var.value,var.name]
            if var.handler.func_code.co_argcount < 2:
                args = [var.value]
            self.document.fastRun_newSeed_args_(var.handler, False, args)
        else:
            self.document.runScript(compile=False, newSeed=False)

    def booleanChanged_(self, sender):
        var = self.document.vars[sender.tag()]
        if sender.state() == NSOnState:
            var.value = True
        else:
            var.value = False
        if var.handler is not None:
            args = [var.value,var.name]
            if var.handler.func_code.co_argcount < 2:
                args = [var.value]
            self.document.fastRun_newSeed_args_(var.handler, False, args)
        else:
            self.document.runScript(compile=False, newSeed=False)

    def buttonClicked_(self, sender):
        var = self.document.vars[sender.tag()]
        # self.document.fastRun_newSeed_(self.document.namespace[var.name], True)
        #self.document.runFunction_(var.name)
        if var.handler is not None:
            args = ["",var.name]
            if var.handler.func_code.co_argcount < 2:
                args = [var.value]
            self.document.fastRun_newSeed_args_(var.handler, False, args)
        else:
            self.document.runScript(compile=False, newSeed=False)

    def menuSelected_(self, sender):
        var = self.document.vars[sender.tag()]
        sel = sender.titleOfSelectedItem()
        var.value = sel
        fn = var.handler
        if var.handler:
            args = [sel,var.name]
            if var.handler.func_code.co_argcount < 2:
                args = [sel]
            self.document.fastRun_newSeed_args_(fn, False, args)
        #self.document.runFunction_(var.name)

    def buildInterface_(self, variables):
        self.vars = variables
        self.clearInterface()
        if len(self.vars) > 0:
            self.panel.orderFront_(None)
        else:
            self.panel.orderOut_(None)
            return

        # Set the title of the parameter panel to the title of the window
        self.panel.setTitle_(self.documentWindow.title())

        (px,py),(pw,ph) = self.panel.frame()
        # Height of the window. Each element has a height of 21.
        # The extra "fluff" is 38 pixels.
        ph = len(self.vars) * 21 + 54
        # Start of first element
        # First element is the height minus the fluff.
        y = ph - 49
        cnt = 0
        for v in self.vars:
            if v.type == graphics.NUMBER:
                self.addLabel_y_c_(v, y, cnt)
                self.addSlider_y_c_(v, y, cnt)

            elif v.type == graphics.TEXT:
                self.addLabel_y_c_(v, y, cnt)
                self.addTextField_y_c_(v, y, cnt)

            elif v.type == graphics.BOOLEAN:
                self.addSwitch_y_c_(v, y, cnt)

            elif v.type == graphics.BUTTON:
                self.addButton_y_c_(v, y, cnt)

            elif v.type == graphics.MENU:
                self.addLabel_y_c_(v, y, cnt)
                self.addMenu_y_c_(v, y, cnt)
            y -= 21
            cnt += 1
        self.panel.setFrame_display_animate_( ((px,py),(pw,ph)), True, True )

    def addLabel_y_c_(self, v, y, cnt):
        control = NSTextField.alloc().init()
        control.setFrame_( ((0,y),(100,13)) )
        control.setStringValue_(v.name + ":")
        control.setAlignment_(NSRightTextAlignment)
        control.setEditable_(False)
        control.setBordered_(False)
        control.setDrawsBackground_(False)
        control.setFont_(SMALL_FONT)
        self.panel.contentView().addSubview_(control)

    def addSlider_y_c_(self, v, y, cnt):
        control = NSSlider.alloc().init()
        control.setMaxValue_(v.max)
        control.setMinValue_(v.min)
        control.setFloatValue_(v.value)
        control.setFrame_(((108,y-1),(172,13)))
        control.cell().setControlSize_(NSMiniControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setContinuous_(True)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.numberChanged_, signature="v@:@@"))
        self.panel.contentView().addSubview_(control)

    def addTextField_y_c_(self, v, y, cnt):
        control = NSTextField.alloc().init()
        control.setStringValue_(v.value)
        control.setFrame_(((108,y-2),(172,15)))
        control.cell().setControlSize_(NSMiniControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setFont_(MINI_FONT)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.textChanged_, signature="v@:@@"))
        self.panel.contentView().addSubview_(control)

    def addSwitch_y_c_(self, v, y, cnt):
        control = NSButton.alloc().init()
        control.setButtonType_(NSSwitchButton)
        if v.value:
            control.setState_(NSOnState)
        else:
            control.setState_(NSOffState)
        control.setFrame_(((108,y-2),(172,16)))
        control.setTitle_(v.name)
        control.setFont_(SMALL_FONT)
        control.cell().setControlSize_(NSSmallControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.booleanChanged_, signature="v@:@@"))
        self.panel.contentView().addSubview_(control)
        
    def addButton_y_c_(self, v, y, cnt):
        control = NSButton.alloc().init()
        control.setFrame_(((108, y-2),(172,16)))
        control.setTitle_(v.name)
        control.setBezelStyle_(1)
        control.setFont_(SMALL_FONT)
        control.cell().setControlSize_(NSMiniControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.buttonClicked_, signature="v@:@@"))
        self.panel.contentView().addSubview_(control)

    def addMenu_y_c_(self, v, y, cnt):
        control = NSPopUpButton.alloc().init()
        control.setFrame_( ((108, y-2),(172,16)) )
        control.setPullsDown_( False )
        control.removeAllItems()
        if v.menuitems is not None:
            for title in v.menuitems:
                control.addItemWithTitle_( title )
        control.setTitle_(v.value)
        control.synchronizeTitleAndSelectedItem()
        control.setBezelStyle_(1)
        control.setFont_(SMALL_FONT)
        control.cell().setControlSize_(NSMiniControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.menuSelected_, signature="v@:@@"))
        self.panel.contentView().addSubview_(control)

