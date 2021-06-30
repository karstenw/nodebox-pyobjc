

from __future__ import print_function

import pdb
kwdbg = False


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

# py3 stuff
py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int
    xrange = range

def getFunctionArgCount( function ):
    # pdb.set_trace()
    if py3:
        return function.__code__.co_argcount
    else:
        return function.func_code.co_argcount


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
            argcount = getFunctionArgCount( var.handler )
            if argcount < 2:
                args = [var.value]
            self.document.fastRun_newSeed_args_(var.handler, False, args)
        else:
            self.document.runScript(compile=False, newSeed=False)

    def textChanged_(self, sender):
        var = self.document.vars[sender.tag()]
        var.value = sender.stringValue()
        if var.handler is not None:
            args = [var.value,var.name]
            argcount = getFunctionArgCount( var.handler )
            if argcount < 2:
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
            argcount = getFunctionArgCount( var.handler )
            if argcount < 2:
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
            argcount = getFunctionArgCount( var.handler )
            if argcount < 2:
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
            argcount = getFunctionArgCount( var.handler )
            if argcount < 2:
                args = [sel]
            self.document.fastRun_newSeed_args_(fn, False, args)
        #self.document.runFunction_(var.name)

    def buildInterface_(self, variables):
        panelwidth = 300

        label_x = 0
        label_w = 100
        ctrl_x = 108
        ctrl_w = 172
        ctrlheight = 26 # 21
        ctrltop = 5
        ctrlheader = 11
        ctrlfooter = 38
        ctrlheaderfooter = ctrlheader + ctrlfooter
        ncontrols = len( variables )
        varsheight = ncontrols * ctrlheight
        
        sizes = {
            'label': 13,
            graphics.NUMBER: 13,
            graphics.TEXT: 15,
            graphics.BOOLEAN: 16,
            graphics.BUTTON: 16,
            graphics.MENU: 16 }

        ctrlfluff = ctrltop + ctrlheader + ctrlfooter

        self.vars = variables
        self.clearInterface()
        if len(self.vars) > 0:
            self.panel.orderFront_(None)
        else:
            self.panel.orderOut_(None)
            return


        # Set the title of the parameter panel to the title of the window
        self.panel.setTitle_(self.documentWindow.title())

        # pdb.set_trace()

        # reset panel
        self.panel.setContentSize_( (panelwidth, 97) )
        (panelx,panely),(panelwidth,panelheight) = self.panel.frame()

        # Height of the window. Each element has a height of ctrlheight.
        # The extra "fluff" is 38 pixels.
        # panelheight = len(self.vars) * 21 + 54
        panelheight = varsheight + ctrlfluff
        # print("panelheight: ", panelheight )
        self.panel.setMinSize_( (panelwidth, panelheight) )

        # Start of first element
        # First element is the height minus the fluff.
        # y = panelheight - 49
        y = panelheight - ( ctrlheader + ctrlfooter )
        
        cnt = 0
        widthlabel = 0
        widthctrl = 0
        y = panelheight - (ctrltop + ctrlheight + 20)
        for v in self.vars:
            leftheight = sizes.get('label', ctrlheight)
            rightheight = sizes.get(v.type, ctrlheight)
            left_coord = (label_x, y)
            right_coord = (ctrl_x, y)
            leftframe =  ( ( label_x, y), (label_w, leftheight) )
            rightframe = ( ( ctrl_x, y), (ctrl_w, rightheight) )

            if v.type == graphics.NUMBER:
                l = self.addLabel_idx_frame_(v, cnt, leftframe)
                c = self.addSlider_idx_frame_(v, cnt, rightframe)
                v.control = (l,c)

            elif v.type == graphics.TEXT:
                l = self.addLabel_idx_frame_(v, cnt, leftframe)
                c = self.addTextField_idx_frame_(v, cnt, rightframe)
                v.control = (l,c)

            elif v.type == graphics.BOOLEAN:
                c = self.addSwitch_idx_frame_(v, cnt, rightframe)
                v.control = (None,c)

            elif v.type == graphics.BUTTON:
                c = self.addButton_idx_frame_(v, cnt, rightframe)
                v.control = (None,c)

            elif v.type == graphics.MENU:
                l = self.addLabel_idx_frame_(v, cnt, leftframe)
                c = self.addMenu_idx_frame_(v, cnt, rightframe)
                v.control = (l,c)
            # print("cnt/y  %i   %i" % (cnt, y) )
            y -= ctrlheight
            cnt += 1

        self.panel.setFrame_display_animate_( ((panelx,panely),(panelwidth,panelheight)), True, 0 )


    def addLabel_idx_frame_(self, v, cnt, frame):
        (x,y),(w,h) = frame
        y += 3
        frame = ((x,y),(w,h))
        control = NSTextField.alloc().init()
        control.setFrame_( frame ) #((0,y),(100,16)) )
        control.setStringValue_(v.name + ":")
        control.setAlignment_(NSRightTextAlignment)
        control.setEditable_(False)
        control.setBordered_(False)
        control.setDrawsBackground_(False)
        control.setFont_(SMALL_FONT)
        # control.setAutoresizingMask_( AppKit.NSViewMinYMargin )
        self.panel.contentView().addSubview_(control)
        return control

    def addSlider_idx_frame_(self, v, cnt, frame):
        (x,y),(w,h) = frame
        control = NSSlider.alloc().init()
        control.setMaxValue_(v.max)
        control.setMinValue_(v.min)
        control.setFloatValue_(v.value)
        control.setFrame_( frame ) #((108,y-1),(172,16)))
        control.cell().setControlSize_(NSMiniControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setContinuous_(True)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.numberChanged_, signature=b"v@:@@"))
        control.setAutoresizingMask_( AppKit.NSViewWidthSizable ) #+ AppKit.NSViewMinYMargin )
        self.panel.contentView().addSubview_(control)
        return control

    def addTextField_idx_frame_(self, v, cnt, frame):
        (x,y),(w,h) = frame
        control = NSTextField.alloc().init()
        control.setStringValue_(v.value)
        control.setFrame_( frame ) #((108,y-2),(172,16)))
        control.cell().setControlSize_(NSMiniControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setFont_(MINI_FONT)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.textChanged_, signature=b"v@:@@"))
        control.setAutoresizingMask_( AppKit.NSViewWidthSizable ) #+ AppKit.NSViewMinYMargin )
        self.panel.contentView().addSubview_(control)
        return control

    def addSwitch_idx_frame_(self, v, cnt, frame):
        (x,y),(w,h) = frame
        control = NSButton.alloc().init()
        control.setButtonType_(NSSwitchButton)
        if v.value:
            control.setState_(NSOnState)
        else:
            control.setState_(NSOffState)
        control.setFrame_( frame ) #((108,y-2),(172,16)))
        control.setTitle_(v.name)
        control.setFont_(SMALL_FONT)
        control.cell().setControlSize_(NSSmallControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.booleanChanged_, signature=b"v@:@@"))
        control.setAutoresizingMask_( AppKit.NSViewWidthSizable ) # + AppKit.NSViewMinYMargin )
        self.panel.contentView().addSubview_(control)
        return control
        
    def addButton_idx_frame_(self, v, cnt, frame):
        (x,y),(w,h) = frame
        control = NSButton.alloc().init()
        control.setFrame_( frame ) #((108, y-2),(172,16)))
        control.setTitle_(v.name)
        control.setBezelStyle_(1)
        control.setFont_(SMALL_FONT)
        control.cell().setControlSize_(NSMiniControlSize)
        control.cell().setControlTint_(NSGraphiteControlTint)
        control.setTarget_(self)
        control.setTag_(cnt)
        control.setAction_(objc.selector(self.buttonClicked_, signature=b"v@:@@"))
        control.setAutoresizingMask_( AppKit.NSViewWidthSizable ) # + AppKit.NSViewMinYMargin )
        self.panel.contentView().addSubview_(control)
        return control

    def addMenu_idx_frame_(self, v, cnt, frame):
        (x,y),(w,h) = frame
        
        control = NSPopUpButton.alloc().init()
        control.setFrame_( frame ) #((108, y-2),(172,16)) )
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
        control.setAction_(objc.selector(self.menuSelected_, signature=b"v@:@@"))
        control.setAutoresizingMask_( AppKit.NSViewWidthSizable ) # + AppKit.NSViewMinYMargin )
        self.panel.contentView().addSubview_(control)
        return control

