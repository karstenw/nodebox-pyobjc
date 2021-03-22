import sys
import os
import traceback, linecache
import re
import objc
import time
import random
import signal
import atexit

import pprint
pp = pprint.pprint

import pdb

kwdbg = False

# set to true to have stdio on the terminal for pdb
debugging = True

# if true print out some debug info on stdout
kwlog = False

import Foundation
import AppKit
NSObject = AppKit.NSObject
NSColor = AppKit.NSColor
NSScriptCommand = AppKit.NSScriptCommand

NSDocument = AppKit.NSDocument
NSDocumentController = AppKit.NSDocumentController

NSNotificationCenter = AppKit.NSNotificationCenter

NSFontAttributeName = AppKit.NSFontAttributeName
NSScreen = AppKit.NSScreen
NSMenu = AppKit.NSMenu
NSCursor = AppKit.NSCursor
NSTimer = AppKit.NSTimer
NSForegroundColorAttributeName = AppKit.NSForegroundColorAttributeName

NSPasteboard = AppKit.NSPasteboard
NSPDFPboardType = AppKit.NSPDFPboardType
NSPostScriptPboardType = AppKit.NSPostScriptPboardType
NSTIFFPboardType = AppKit.NSTIFFPboardType

NSBundle = AppKit.NSBundle
NSSavePanel = AppKit.NSSavePanel
NSLog = AppKit.NSLog
NSApp = AppKit.NSApp
NSPrintOperation = AppKit.NSPrintOperation
NSWindow = AppKit.NSWindow
NSBorderlessWindowMask = AppKit.NSBorderlessWindowMask
NSBackingStoreBuffered = AppKit.NSBackingStoreBuffered
NSView = AppKit.NSView
NSGraphicsContext = AppKit.NSGraphicsContext
NSRectFill = AppKit.NSRectFill
NSAffineTransform = AppKit.NSAffineTransform
NSFocusRingTypeExterior = AppKit.NSFocusRingTypeExterior
NSResponder = AppKit.NSResponder

NSURL = AppKit.NSURL
NSWorkspace = AppKit.NSWorkspace
NSBezierPath = AppKit.NSBezierPath


import threading
Thread = threading.Thread

from . import ValueLadder
MAGICVAR = ValueLadder.MAGICVAR

from . import PyDETextView

from . import preferences
NodeBoxPreferencesController = preferences.NodeBoxPreferencesController
LibraryFolder = preferences.LibraryFolder

from . import util
errorAlert = util.errorAlert


# from nodebox import util
import nodebox.util
util = nodebox.util
makeunicode = nodebox.util.makeunicode

import nodebox.util.ottobot
genProgram = nodebox.util.ottobot.genProgram


import nodebox.util.QTSupport
QTSupport = nodebox.util.QTSupport

# from nodebox import graphics
import nodebox.graphics
graphics = nodebox.graphics

# AppleScript enumerator codes for PDF and Quicktime export
PDF = 0x70646678 # 'pdfx'
QUICKTIME = 0x71747878 # 'qt  '


black = NSColor.blackColor()
VERY_LIGHT_GRAY = black.blendedColorWithFraction_ofColor_(0.95,
                                                          NSColor.whiteColor())
DARKER_GRAY = black.blendedColorWithFraction_ofColor_(0.8,
                                                      NSColor.whiteColor())

# from nodebox.gui.mac.dashboard import *
# from nodebox.gui.mac.progressbar import ProgressBarController
from . import dashboard
DashboardController = dashboard.DashboardController

from . import progressbar
ProgressBarController = progressbar.ProgressBarController

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

class ExportCommand(NSScriptCommand):
    pass    

class OutputFile(object):

    def __init__(self, data, isErr=False):
        self.data = data
        self.isErr = isErr

    def write(self, data):
        if isinstance(data, pstr):
            try:
                # data = unicode(data, "utf_8", "replace")
                data = makeunicode( data )
            except UnicodeDecodeError:
                data = "XXX " + repr(data)
        self.data.append( (self.isErr, data) )




class NodeBoxDocument(NSDocument):
    # class defined in NodeBoxDocument.xib

    graphicsView = objc.IBOutlet()
    outputView = objc.IBOutlet() 
    textView = objc.IBOutlet()
    window = objc.IBOutlet()
    variablesController = objc.IBOutlet()
    dashboardController = objc.IBOutlet()
    animationSpinner = objc.IBOutlet()

    # The ExportImageAccessory adds:
    exportImageAccessory = objc.IBOutlet()
    exportImageFormat = objc.IBOutlet()
    exportImagePageCount = objc.IBOutlet()

    # The ExportMovieAccessory adds:
    exportMovieAccessory = objc.IBOutlet()
    exportMovieFrames = objc.IBOutlet()
    exportMovieFps = objc.IBOutlet()

    # When the PageCount accessory is loaded, we also add:
    pageCount = objc.IBOutlet()
    pageCountAccessory = objc.IBOutlet()

    # When the ExportSheet is loaded, we also add:
    exportSheet = objc.IBOutlet()
    exportSheetIndicator = objc.IBOutlet()

    path = None
    exportDir = None
    magicvar = None # Used for value ladders.
    _code = None
    vars = []
    movie = None

    def windowNibName(self):
        return "NodeBoxDocument"

    def init(self):
        self = super(NodeBoxDocument, self).init()
        nc = NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(self,
                                             "textFontChanged:",
                                             "PyDETextFontChanged",
                                             None)
        self.namespace = {}
        self.canvas = graphics.Canvas()
        self.context = graphics.Context(self.canvas, self.namespace)
        self.animationTimer = None
        self.__doc__ = {}
        self._pageNumber = 1
        self._frame = 150
        self.fullScreen = None
        self._seed = time.time()

        # this is None
        self.currentView = self.graphicsView
        return self

    def autosavesInPlace(self):
        return True

    def close(self):
        self.stopScript()
        super(NodeBoxDocument, self).close()

    def __del__(self):
        nc = NSNotificationCenter.defaultCenter()
        nc.removeObserver_name_object_(self, "PyDETextFontChanged", None)
        # text view has a couple of circular refs, it can let go of them now
        self.textView._cleanup()

    def textFontChanged_(self, notification):
        font = PyDETextView.getBasicTextAttributes()[NSFontAttributeName]
        self.outputView.setFont_(font)

    def readFromFile_ofType_(self, path, tp):
        if self.textView is None:
            # we're not yet fully loaded
            self.path = path
        else:
            # "revert"
            self.readFromUTF8_(path)
        return True

    def writeToFile_ofType_(self, path, tp):
        f = file(path, "w")
        text = self.textView.string()
        f.write(text.encode("utf8"))
        f.close()
        return True

    def windowControllerDidLoadNib_(self, controller):
        if self.path:
            self.readFromUTF8_(self.path)
        font = PyDETextView.getBasicTextAttributes()[NSFontAttributeName]
        self.outputView.setFont_(font)
        self.textView.window().makeFirstResponder_(self.textView)
        self.windowControllers()[0].setWindowFrameAutosaveName_("NodeBoxDocumentWindow")

        # switch off automatic substitutions
        try:
            self.textView.setAutomaticQuoteSubstitutionEnabled_( False )
            self.textView.setAutomaticDashSubstitutionEnabled_( False )

            # This does not work well with syntax coloring
            #self.textView.setAutomaticLinkDetectionEnabled_( True )
            #self.textView.setDisplaysLinkToolTips_( True )

            self.outputView.setAutomaticQuoteSubstitutionEnabled_( False )
            self.outputView.setAutomaticDashSubstitutionEnabled_( False )
            #self.outputView.setAutomaticLinkDetectionEnabled_( True )
            #self.outputView.setDisplaysLinkToolTips_( True )
        except Exception as err:
            pass

    def readFromUTF8_(self, path):
        f = open(path)
        s = f.read()
        f.close()
        text = makeunicode( s )
        f.close()
        self.textView.setString_(text)
        self.textView.usesTabs = "\t" in text
        
    def cleanRun_newSeed_buildInterface_(self, fn, newSeed, buildInterface):
        self.animationSpinner.startAnimation_(None)

        # Prepare everything for running the script
        self.prepareRun()

        # Run the actual script
        success = self.fastRun_newSeed_(fn, newSeed)
        self.animationSpinner.stopAnimation_(None)

        if success and buildInterface:

            # Build the interface
            self.vars = self.namespace["_ctx"]._vars
            if len(self.vars) > 0:
                self.buildInterface_(None)

        return success

    def prepareRun(self):

        # Compile the script
        success, output = self.boxedRun_args_(self._compileScript, [])
        self.flushOutput_(output)
        if not success:
            return False

        # Initialize the namespace
        self._initNamespace()
        
        # Reset the pagenum
        self._pageNum = 1
        
        # Reset the frame
        self._frame = 1

        self.speed = self.canvas.speed = None

    def fastRun_newSeed_(self, fn, newSeed = False):
        """This is the old signature. Dispatching to the new with args"""
        return self.fastRun_newSeed_args_( fn, newSeed, [])


    def fastRun_newSeed_args_(self, fn, newSeed = False, args=[]):
        # Check if there is code to run
        if self._code is None:
            return False

        # Clear the canvas
        self.canvas.clear()

        # Generate a new seed, if needed
        if newSeed:
            self._seed = time.time()
        random.seed(self._seed)

        # Set the mouse position
        
        # kw fix
        if not self.currentView:
            self.currentView = self.graphicsView

        window = self.currentView.window()
        pt = window.mouseLocationOutsideOfEventStream()
        mx, my = window.contentView().convertPoint_toView_(pt, self.currentView)
        # Hack: mouse coordinates are flipped vertically in FullscreenView.
        # This flips them back.
        if isinstance(self.currentView, FullscreenView):
            my = self.currentView.bounds()[1][1] - my
        if self.fullScreen is None:
            mx /= self.currentView.zoom
            my /= self.currentView.zoom
        self.namespace["MOUSEX"], self.namespace["MOUSEY"] = mx, my
        self.namespace["mousedown"] = self.currentView.mousedown
        self.namespace["keydown"] = self.currentView.keydown
        self.namespace["key"] = self.currentView.key
        self.namespace["keycode"] = self.currentView.keycode
        self.namespace["scrollwheel"] = self.currentView.scrollwheel
        self.namespace["wheeldelta"] = self.currentView.wheeldelta

        # Reset the context
        self.context._resetContext()

        # Initalize the magicvar
        self.namespace[MAGICVAR] = self.magicvar

        # Set the pagenum
        self.namespace['PAGENUM'] = self._pageNumber
        
        # Set the frame
        self.namespace['FRAME'] = self._frame

        # Run the script
        success, output = self.boxedRun_args_(fn, args)
        self.flushOutput_(output)
        if not success:
            return False

        # Display the output of the script
        self.currentView.setCanvas_(self.canvas)

        return True
        

    @objc.IBAction
    def clearMessageArea_(self, sender):
        # pp( dir(self.outputView.textStorage()))
        self.outputView.textStorage().mutableString().setString_(u"")

    @objc.IBAction
    def runFullscreen_(self, sender):
        if self.fullScreen is not None:
            return
        # self.clearMessageArea_( None )
        self.stopScript()
        self.currentView = FullscreenView.alloc().init()
        self.currentView.canvas = None
        fullRect = NSScreen.mainScreen().frame()
        self.fullScreen = FullscreenWindow.alloc().initWithRect_(fullRect)
        # self.fullScreen.oneShot = True
        self.fullScreen.setContentView_(self.currentView)
        self.fullScreen.makeKeyAndOrderFront_(self)
        self.fullScreen.makeFirstResponder_(self.currentView)
        NSMenu.setMenuBarVisible_(False)
        NSCursor.hide()
        self._runScript()

    @objc.IBAction
    def runScript_(self, sender):
        # self.clearMessageArea_( None )
        self.runScript()
        
    def runScript(self, compile=True, newSeed=True):
        if self.fullScreen is not None: return
        self.currentView = self.graphicsView
        self._runScript(compile, newSeed)

    def _runScript(self, compile=True, newSeed=True):
        if not self.cleanRun_newSeed_buildInterface_(self._execScript, True, True):
            pass

        # Check whether we are dealing with animation
        if self.canvas.speed is not None:
            if not self.namespace.has_key("draw"):
                errorAlert("Not a proper NodeBox animation",
                    "NodeBox animations should have at least a draw() method.")
                return

            # Check if animationTimer is already running
            if self.animationTimer is not None:
                self.stopScript()

            self.speed = self.canvas.speed

            # Run setup routine
            if self.namespace.has_key("setup"):
                self.fastRun_newSeed_(self.namespace["setup"], False)
            window = self.currentView.window()
            window.makeFirstResponder_(self.currentView)

            # Start the timer
            timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_
            self.animationTimer = timer(1.0 / self.speed,
                                        self,
                                        objc.selector(self.doFrame, signature="v@:@"),
                                        None,
                                        True)

            # Start the spinner
            self.animationSpinner.startAnimation_(None)

    def runScriptFast(self):        
        if self.animationTimer is None:
            self.fastRun_newSeed_(self._execScript, False)
        else:
            # XXX: This can be sped up. We just run _execScript to get the
            # method with __MAGICVAR__ into the namespace, and execute
            # that, so it should only be called once for animations.
            self.fastRun_newSeed_(self._execScript, False)
            self.fastRun_newSeed_(self.namespace["draw"], False)

    def doFrame(self):
        self.fastRun_newSeed_(self.namespace["draw"], True)
        self._frame += 1
        
    def source(self):
        return self.textView.string()

    def setSource_(self, source):
        self.textView.setString_(source)

    @objc.IBAction
    def stopScript_(self, sender=None):
        self.stopScript()
        
    def stopScript(self):
        if self.namespace.has_key("stop"):
            success, output = self.boxedRun_args_(self.namespace["stop"], [])
            self.flushOutput_(output)
        self.animationSpinner.stopAnimation_(None)

        if self.animationTimer is not None:
            self.animationTimer.invalidate()
            self.animationTimer = None

        if self.fullScreen is not None:
            self.currentView = self.graphicsView
            self.fullScreen.orderOut_(None)
            self.fullScreen = None
            
        NSMenu.setMenuBarVisible_(True)
        NSCursor.unhide()
        self.textView.hideValueLadder()
        window = self.textView.window()
        window.makeFirstResponder_(self.textView)

    def _compileScript(self, source=None):
        if source is None:
            source = self.textView.string()

        # if this is activated, all unicode carrying scripts NEED a "encoding"
        # line
        # OTOH if this is on, NB accepts scripts with an encoding line.
        # currently an error
        # source = source.encode("utf-8")
        self._code = None
        self._code = compile(source + "\n\n",
                             self.scriptName.encode('ascii', 'ignore'),
                             "exec")

    def _initNamespace(self):

        self.namespace.clear()
        # Add everything from the namespace
        for name in graphics.__all__:
            self.namespace[name] = getattr(graphics, name)
        for name in util.__all__:
            self.namespace[name] = getattr(util, name)

        # debug print all collected keywords
        if kwlog:
            #print "util.__all__:"
            #pp(util.__all__)
            #print "graphics.__all__:"
            #pp(graphics.__all__)
            print("namespace.keys():")
            # pp(namespace.keys())

        # Add everything from the context object
        self.namespace["_ctx"] = self.context
        for attrName in dir(self.context):
            self.namespace[attrName] = getattr(self.context, attrName)
        # Add the document global
        self.namespace["__doc__"] = self.__doc__
        # Add the page number
        self.namespace["PAGENUM"] = self._pageNumber
        # Add the frame number
        self.namespace["FRAME"] = self._frame
        # Add the magic var
        self.namespace[MAGICVAR] = self.magicvar
        # XXX: will be empty after reset.
        #for var in self.vars:
        #    self.namespace[var.name] = var.value

    def _execScript(self):
        exec(self._code, self.namespace)
        self.__doc__ = self.namespace.get("__doc__", self.__doc__)

    def boxedRun_args_(self, method, args):
        """
        Runs the given method in a boxed environment.
        Boxed environments:
         - Have their current directory set to the directory of the file
         - Have their argument set to the filename
         - Have their outputs redirect to an output stream.
        Returns:
           A tuple containing:
             - A boolean indicating whether the run was successful
             - The OutputFile
        """

        self.scriptName = self.fileName()
        libpath = LibraryFolder()
        libDir = libpath.libDir

        if not self.scriptName:
            curDir = os.getenv("HOME")
            self.scriptName = "<untitled>"
        else:
            curDir = os.path.dirname(self.scriptName)

        save = sys.stdout, sys.stderr
        saveDir = os.getcwd()
        saveArgv = sys.argv
        sys.argv = [self.scriptName]
        if os.path.exists(libDir):
            sys.path.insert(0, libDir)
        os.chdir(curDir)
        sys.path.insert(0, curDir)
        output = []
        
        # for pdb debugging in terminal this needs to be switched off
        if not debugging:
            sys.stdout = OutputFile(output, False)
            sys.stderr = OutputFile(output, True)
        self._scriptDone = False
        try:
            if self.animationTimer is None:
                pass
                # Creating a thread is a heavy operation,
                # don't install it when animating, where speed is crucial
                #t = Thread(target=self._userCancelledMonitor,
                #           name="UserCancelledMonitor")
                #t.start()
            try:
                method(*args)
            except KeyboardInterrupt:
                self.stopScript()
            except:
                etype, value, tb = sys.exc_info()
                if tb.tb_next is not None:
                    tb = tb.tb_next  # skip the frame doing the exec
                traceback.print_exception(etype, value, tb)
                etype = value = tb = None
                return False, output
        finally:
            self._scriptDone = True
            sys.stdout, sys.stderr = save
            os.chdir(saveDir)
            sys.path.remove(curDir)
            try:
                sys.path.remove(libDir)
            except ValueError:
                pass
            sys.argv = saveArgv
            #self.flushOutput_()
        return True, output

    # UNUSED - Referenced in commented out Thread section of boxedRun_args_
    # Should be removed since Carbon is not available anymore

    # from Mac/Tools/IDE/PyEdit.py
    def _userCancelledMonitor(self):
        from Carbon import Evt
        while not self._scriptDone:
            if Evt.CheckEventQueueForUserCancel():
                # Send a SIGINT signal to ourselves.
                # This gets delivered to the main thread,
                # cancelling the running script.
                os.kill(os.getpid(), signal.SIGINT)
                break
            time.sleep(0.25)

    def flushOutput_(self, output):
        outAttrs = PyDETextView.getBasicTextAttributes()
        errAttrs = outAttrs.copy()
        # XXX err color from user defaults...
        errAttrs[NSForegroundColorAttributeName] = NSColor.redColor()

        outputView = self.outputView
        outputView.setSelectedRange_((outputView.textStorage().length(), 0))
        lastErr = None
        for isErr, data in output:
            if isErr != lastErr:
                attrs = [outAttrs, errAttrs][isErr]
                outputView.setTypingAttributes_(attrs)
                lastErr = isErr
            outputView.insertText_(data)
        # del self.output

    @objc.IBAction
    def copyImageAsPDF_(self, sender):
        pboard = NSPasteboard.generalPasteboard()
        # graphicsView implements the pboard delegate method to provide the data
        pboard.declareTypes_owner_( [NSPDFPboardType,
                                     NSPostScriptPboardType,
                                     NSTIFFPboardType],
                                    self.graphicsView)

    @objc.IBAction
    def exportAsImage_(self, sender):
        exportPanel = NSSavePanel.savePanel()
        exportPanel.setRequiredFileType_("pdf")
        exportPanel.setNameFieldLabel_("Export To:")
        exportPanel.setPrompt_("Export")
        exportPanel.setCanSelectHiddenExtension_(True)
        if not NSBundle.loadNibNamed_owner_("ExportImageAccessory", self):
            NSLog("Error -- could not load ExportImageAccessory.")
        self.exportImagePageCount.setIntValue_(1)
        exportPanel.setAccessoryView_(self.exportImageAccessory)
        path = self.fileName()
        if path:
            dirName, fileName = os.path.split(path)
            fileName, ext = os.path.splitext(fileName)
            fileName += ".pdf"
        else:
            dirName, fileName = None, "Untitled.pdf"
        # If a file was already exported, use that folder as the default.
        if self.exportDir is not None:
            dirName = self.exportDir
        exportPanel.beginSheetForDirectory_file_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            dirName,
            fileName,
            NSApp().mainWindow(),
            self,
            "exportPanelDidEnd:returnCode:contextInfo:", 0)

    def exportPanelDidEnd_returnCode_contextInfo_(self, panel, returnCode, context):
        if returnCode:
            fname = panel.filename()
            self.exportDir = os.path.split(fname)[0] # Save the directory we exported to.
            pages = self.exportImagePageCount.intValue()
            format = panel.requiredFileType()
            panel.close()
            self.doExportAsImage_fmt_pages_(fname, format, pages)
    exportPanelDidEnd_returnCode_contextInfo_ = objc.selector( exportPanelDidEnd_returnCode_contextInfo_, signature=b"v@:@ii")
            
    @objc.IBAction
    def exportImageFormatChanged_(self, sender):
        image_formats = ('pdf', 'eps', 'png', 'tiff', 'jpg', 'gif')
        panel = sender.window()
        panel.setRequiredFileType_(image_formats[sender.indexOfSelectedItem()])

    def doExportAsImage_fmt_pages_(self, fname, format, pages):
        basename, ext = os.path.splitext(fname)
        # When saving one page (the default), just save the current graphics
        # context. When generating multiple pages, we run the script again 
        # (so we don't use the current displayed view) for the first page,
        # and then for every next page.
        if pages == 1:
            if self.graphicsView.canvas is None:
                self.runScript()
            self.canvas.save(fname, format)
        elif pages > 1:
            pb = ProgressBarController.alloc().init()
            pb.begin_maxval_("Generating %s images..." % pages, pages)
            try:
                if not self.cleanRun_newSeed_buildInterface_(self._execScript,
                                                                        True, True):
                    return
                self._pageNumber = 1
                self._frame = 1

                # If the speed is set, we are dealing with animation
                if self.canvas.speed is None:
                    for i in range(pages):
                        if i > 0: # Run has already happened first time
                            self.fastRun_newSeed_(self._execScript, True)
                        counterAsString = "-%5d" % self._pageNumber
                        counterAsString = counterAsString.replace(' ', '0')
                        exportName = basename + counterAsString + ext

                        self.canvas.save(exportName, format)
                        self.graphicsView.setNeedsDisplay_(True)
                        self._pageNumber += 1
                        self._frame += 1
                        pb.inc()
                else:
                    if self.namespace.has_key("setup"):
                        self.fastRun_newSeed_(self.namespace["setup"], False)
                    for i in range(pages):
                        self.fastRun_newSeed_(self.namespace["draw"], True)
                        # 1-based
                        counterAsString = "-%5d" % self._pageNumber
                        # 0-based
                        # counterAsString = "-%5d" % i 
                        counterAsString = counterAsString.replace(' ', '0')
                        exportName = basename + counterAsString + ext
                        self.canvas.save(exportName, format)
                        self.graphicsView.setNeedsDisplay_(True)
                        self._pageNumber += 1
                        self._frame += 1
                        pb.inc()
                    if self.namespace.has_key("stop"):
                        success, output = self.boxedRun_args_(self.namespace["stop"],
                                                              [])
                        self.flushOutput_(output)
            except KeyboardInterrupt:
                pass
            pb.end()
            del pb
        self._pageNumber = 1
        self._frame = 1

    @objc.IBAction
    def exportAsMovie_(self, sender):
        exportPanel = NSSavePanel.savePanel()
        exportPanel.setRequiredFileType_("pdf")
        exportPanel.setNameFieldLabel_("Export To:")
        exportPanel.setPrompt_("Export")
        exportPanel.setCanSelectHiddenExtension_(True)
        exportPanel.setAllowedFileTypes_(["mov"])
        if not NSBundle.loadNibNamed_owner_("ExportMovieAccessory", self):
            NSLog("Error -- could not load ExportMovieAccessory.")
        self.exportMovieFrames.setIntValue_(150)
        self.exportMovieFps.setIntValue_(30)
        exportPanel.setAccessoryView_(self.exportMovieAccessory)
        path = self.fileName()
        if path:
            dirName, fileName = os.path.split(path)
            fileName, ext = os.path.splitext(fileName)
            fileName += ".mov"
        else:
            dirName, fileName = None, "Untitled.mov"
        # If a file was already exported, use that folder as the default.
        if self.exportDir is not None:
            dirName = self.exportDir
        exportPanel.beginSheetForDirectory_file_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            dirName,
            fileName,
            NSApp().mainWindow(),
            self,
            "qtPanelDidEnd:returnCode:contextInfo:", 0)
                
    def qtPanelDidEnd_returnCode_contextInfo_(self, panel, returnCode, context):
        if returnCode:
            fname = panel.filename()
            self.exportDir = os.path.split(fname)[0] # Save the directory we exported to.
            frames = self.exportMovieFrames.intValue()
            fps = self.exportMovieFps.floatValue()
            panel.close()

            if frames <= 0 or fps <= 0: return
            self.doExportAsMovie_frames_fps_(fname, frames, fps)

    qtPanelDidEnd_returnCode_contextInfo_ = objc.selector(qtPanelDidEnd_returnCode_contextInfo_,
                                                          signature=b"v@:@ii")

    def doExportAsMovie_frames_fps_(self, fname, frames, fps):
        # Only load QTSupport when necessary. 
        # QTSupport loads QTKit, which wants to establish a connection to the window
        # server.
        # If we load QTSupport before something is on screen, the connection to the
        # window server cannot be established.

        try:
            os.unlink(fname)
        except:
            pass
        try:
            fp = open(fname, 'w')
            fp.close()
        except:
            errorAlert("File Error", ("Could not create file '%s'. "
                                      "Perhaps it is locked or busy.") % fname)
            return

        movie = None

        pb = ProgressBarController.alloc().init()
        pb.begin_maxval_("Generating %s frames..." % frames, frames)
        try:
            if not self.cleanRun_newSeed_buildInterface_(self._execScript, True, True):
                return
            self._pageNumber = 1
            self._frame = 1

            movie = QTSupport.Movie(fname, fps)
            # If the speed is set, we are dealing with animation
            if self.canvas.speed is None:
                for i in range(frames):
                    if i > 0: # Run has already happened first time
                        self.fastRun_newSeed_(self._execScript, True)
                    movie.add(self.canvas)
                    self.graphicsView.setNeedsDisplay_(True)
                    pb.inc()
                    self._pageNumber += 1
                    self._frame += 1
            else:
                if self.namespace.has_key("setup"):
                    self.fastRun_newSeed_(self.namespace["setup"], False)
                for i in range(frames):
                    self.fastRun_newSeed_(self.namespace["draw"], True)
                    movie.add(self.canvas)
                    self.graphicsView.setNeedsDisplay_(True)
                    pb.inc()
                    self._pageNumber += 1
                    self._frame += 1
                if self.namespace.has_key("stop"):
                    success, output = self.boxedRun_args_(self.namespace["stop"], [])
                    self.flushOutput_(output)
        except KeyboardInterrupt:
            pass
        pb.end()
        del pb
        movie.save()
        self._pageNumber = 1
        self._frame = 1

    @objc.IBAction
    def printDocument_(self, sender):
        op = NSPrintOperation.printOperationWithView_printInfo_(self.graphicsView,
                                                                self.printInfo())
        op.runOperationModalForWindow_delegate_didRunSelector_contextInfo_(
            NSApp().mainWindow(), self, "printOperationDidRun:success:contextInfo:",
            0)

    def printOperationDidRun_success_contextInfo_(self, op, success, info):
        if success:
            self.setPrintInfo_(op.printInfo())

    printOperationDidRun_success_contextInfo_ = objc.selector(
                                            printOperationDidRun_success_contextInfo_,
                                            signature=b"v@:@ci")

    @objc.IBAction
    def buildInterface_(self, sender):
        self.dashboardController.buildInterface_(self.vars)

    def validateMenuItem_(self, menuItem):
        if menuItem.action() in ("exportAsImage:", "exportAsMovie:"):
            return self.canvas is not None
        return True
        

    # Zoom commands, forwarding to the graphics view.
    @objc.IBAction
    def zoomIn_(self, sender):
        if self.fullScreen is not None: return
        self.graphicsView.zoomIn_(sender)

    @objc.IBAction
    def zoomOut_(self, sender):
        if self.fullScreen is not None: return
        self.graphicsView.zoomOut_(sender)
        
    @objc.IBAction
    def zoomToTag_(self, sender):
        if self.fullScreen is not None: return
        self.graphicsView.zoomTo_(sender.tag() / 100.0)

    @objc.IBAction
    def zoomToFit_(self, sender):
        if self.fullScreen is not None: return
        self.graphicsView.zoomToFit_(sender)
        

class FullscreenWindow(NSWindow):
    def initWithRect_(self, fullRect):
        objc.super(FullscreenWindow,
                   self).initWithContentRect_styleMask_backing_defer_(
                                        fullRect,
                                        NSBorderlessWindowMask,
                                        NSBackingStoreBuffered,
                                        True)
        return self
        
    def canBecomeKeyWindow(self):
        return True

class FullscreenView(NSView):
    
    def init(self):
        super(FullscreenView, self).init()
        self.mousedown = False
        self.keydown = False
        self.key = None
        self.keycode = None
        self.scrollwheel = False
        self.wheeldelta = 0.0
        return self
        
    def setCanvas_(self, canvas):
        self.canvas = canvas
        self.setNeedsDisplay_(True)
        if not hasattr(self, "screenRect"):
            self.screenRect = NSScreen.mainScreen().frame()
            cw, ch = self.canvas.size
            sw, sh = self.screenRect[1]
            self.scalingFactor = calc_scaling_factor(cw, ch, sw, sh)
            nw, nh = cw * self.scalingFactor, ch * self.scalingFactor
            self.scaledSize = nw, nh
            self.dx = (sw - nw) / 2.0
            self.dy = (sh - nh) / 2.0

    def drawRect_(self, rect):
        NSGraphicsContext.currentContext().saveGraphicsState()
        NSColor.blackColor().set()
        NSRectFill(rect)
        if self.canvas is not None:
            t = NSAffineTransform.transform()
            t.translateXBy_yBy_(self.dx, self.dy)
            t.scaleBy_(self.scalingFactor)
            t.concat()
            clip = NSBezierPath.bezierPathWithRect_(
                                ((0, 0), (self.canvas.width, self.canvas.height)) )
            clip.addClip()
            self.canvas.draw()
        NSGraphicsContext.currentContext().restoreGraphicsState()

    def isFlipped(self):
        return True

    def mouseDown_(self, event):
        self.mousedown = True

    def mouseUp_(self, event):
        self.mousedown = False

    def keyDown_(self, event):
        self.keydown = True
        self.key = event.characters()
        self.keycode = event.keyCode()

    def keyUp_(self, event):
        self.keydown = False
        self.key = event.characters()
        self.keycode = event.keyCode()

    def scrollWheel_(self, event):
        self.scrollwheel = True
        self.wheeldelta = event.deltaY()

    def canBecomeKeyView(self):
        return True

    def acceptsFirstResponder(self):
        return True

def calc_scaling_factor(width, height, maxwidth, maxheight):
    return min(float(maxwidth) / width, float(maxheight) / height)
        
class ZoomPanel(NSView):
    pass

# class defined in NodeBoxGraphicsView.xib
class NodeBoxGraphicsView(NSView):
    document = objc.IBOutlet()
    zoomLevel = objc.IBOutlet()
    zoomField = objc.IBOutlet()
    zoomSlider = objc.IBOutlet()
    
    # The zoom levels are 10%, 25%, 50%, 75%, 100%, 200% and so on up to 2000%.
    zoomLevels = [0.1, 0.25, 0.5, 0.75]
    zoom = 1.0
    while zoom <= 20.0:
        zoomLevels.append(zoom)
        zoom += 1.0
        
    def awakeFromNib(self):
        self.canvas = None
        self._dirty = False
        self.mousedown = False
        self.keydown = False
        self.key = None
        self.keycode = None
        self.scrollwheel = False
        self.wheeldelta = 0.0
        self._zoom = 1.0
        self.setFrameSize_( (graphics.DEFAULT_WIDTH, graphics.DEFAULT_HEIGHT) )
        self.setFocusRingType_(NSFocusRingTypeExterior)
        if self.superview() is not None:
            self.superview().setBackgroundColor_(VERY_LIGHT_GRAY)

    def setCanvas_(self, canvas):
        self.canvas = canvas
        if canvas is not None:
            w, h = self.canvas.size
            self.setFrameSize_([w*self._zoom, h*self._zoom])
        self.markDirty()

    def getZoom(self):
        return self._zoom

    def setZoom_(self, zoom):
        self._zoom = zoom
        self.zoomLevel.setTitle_("%i%%" % (self._zoom * 100.0))
        self.zoomSlider.setFloatValue_(self._zoom * 100.0)
        self.setCanvas_(self.canvas)
    zoom = property(getZoom, setZoom_)
        
    @objc.IBAction
    def dragZoom_(self, sender):
        self.zoom = self.zoomSlider.floatValue() / 100.0
        self.setCanvas_(self.canvas)
        
    def findNearestZoomIndex_(self, zoom):
        """Returns the nearest zoom level, and whether we found a direct, exact
        match or a fuzzy match."""
        try: # Search for a direct hit first.
            idx = self.zoomLevels.index(zoom)
            return idx, True
        except ValueError: # Can't find the zoom level, try looking at the indexes.
            idx = 0
            try:
                while self.zoomLevels[idx] < zoom:
                    idx += 1
            except KeyError: # End of the list
                idx = len(self.zoomLevels) - 1 # Just return the last index.
            return idx, False
        
    @objc.IBAction
    def zoomIn_(self, sender):
        idx, direct = self.findNearestZoomIndex_(self.zoom)
        # Direct hits are perfect, but indirect hits require a bit of help.
        # Because of the way indirect hits are calculated, they are already 
        # rounded up to the upper zoom level; this means we don't need to add 1.
        if direct:
            idx += 1
        idx = max(min(idx, len(self.zoomLevels)-1), 0)
        self.zoom = self.zoomLevels[idx]

    @objc.IBAction
    def zoomOut_(self, sender):
        idx, direct = self.findNearestZoomIndex_(self.zoom)
        idx -= 1
        idx = max(min(idx, len(self.zoomLevels)-1), 0)
        self.zoom = self.zoomLevels[idx]
        
    @objc.IBAction
    def resetZoom_(self, sender):
        self.zoom = 1.0
        
    def zoomTo_(self, zoom):
        self.zoom = zoom
        
    @objc.IBAction
    def zoomToFit_(self, sender):
        w, h = self.canvas.size
        fw, fh = self.superview().frame()[1]
        factor = min(fw / w, fh / h)
        self.zoom = factor

    def markDirty(self, redraw=True):
        self._dirty = True
        if redraw:
            self.setNeedsDisplay_(True)

    def setFrameSize_(self, size):
        self._image = None
        NSView.setFrameSize_(self, size)

    def isOpaque(self):
        return False

    def isFlipped(self):
        return True
        
    def drawRect_(self, rect):
        if self.canvas is not None:
            NSGraphicsContext.currentContext().saveGraphicsState()
            try:
                if self.zoom != 1.0:
                    t = NSAffineTransform.transform()
                    t.scaleBy_(self.zoom)
                    t.concat()
                    clip = NSBezierPath.bezierPathWithRect_( ( (0, 0),
                                                               (self.canvas.width,
                                                                self.canvas.height)) )
                    clip.addClip()
                self.canvas.draw()
            except:
                # A lot of code just to display the error in the output view.
                etype, value, tb = sys.exc_info()
                if tb.tb_next is not None:
                    tb = tb.tb_next  # skip the frame doing the exec
                traceback.print_exception(etype, value, tb)
                data = "".join(traceback.format_exception(etype, value, tb))
                attrs = PyDETextView.getBasicTextAttributes()
                attrs[NSForegroundColorAttributeName] = NSColor.redColor()
                outputView = self.document.outputView
                outputView.setSelectedRange_((outputView.textStorage().length(), 0))
                outputView.setTypingAttributes_(attrs)
                outputView.insertText_(data)
            NSGraphicsContext.currentContext().restoreGraphicsState()

    def _updateImage(self):
        if self._dirty:
            self._image = self.canvas._nsImage
            self._dirty = False

    # pasteboard delegate method
    def pasteboard_provideDataForType_(self, pboard, type):
        if NSPDFPboardType:
            pboard.setData_forType_(self.pdfData, NSPDFPboardType)
        elif NSPostScriptPboardType:
            pboard.setData_forType_(self.epsData, NSPostScriptPboardType)
        elif NSTIFFPboardType:
            pboard.setData_forType_(self.tiffData, NSTIFFPboardType)
            
    def _get_pdfData(self):
        if self.canvas:
            return self.canvas._getImageData('pdf')
    pdfData = property(_get_pdfData)

    def _get_epsData(self):
        if self.canvas:
            return self.canvas._getImageData('eps')
    epsData = property(_get_epsData)

    def _get_tiffData(self):
        return self.canvas._getImageData('tiff')
    tiffData = property(_get_tiffData)
     
    def _get_pngData(self):
        return self.canvas._getImageData('png')
    pngData = property(_get_pngData)

    def _get_gifData(self):
        return self.canvas._getImageData('gif')
    gifData = property(_get_gifData)

    def _get_jpegData(self):
        return self.canvas._getImageData('jpeg')
    jpegData = property(_get_jpegData)

    def mouseDown_(self, event):
        self.mousedown = True
        
    def mouseUp_(self, event):
        self.mousedown = False
        
    def keyDown_(self, event):
        self.keydown = True
        self.key = event.characters()
        self.keycode = event.keyCode()
        
    def keyUp_(self, event):
        self.keydown = False
        self.key = event.characters()
        self.keycode = event.keyCode()
        
    def scrollWheel_(self, event):
        NSResponder.scrollWheel_(self, event)
        self.scrollwheel = True
        self.wheeldelta = event.deltaY()

    def canBecomeKeyView(self):
        return True

    def acceptsFirstResponder(self):
        return True

class NodeBoxAppDelegate(NSObject):

    def awakeFromNib(self):
        self._prefsController = None
        libpath = LibraryFolder()


    @objc.IBAction
    def showPreferencesPanel_(self, sender):
        if self._prefsController is None:
            self._prefsController = NodeBoxPreferencesController.alloc().init()
        self._prefsController.showWindow_(sender)

    @objc.IBAction
    def generateCode_(self, sender):
        """Generate a piece of NodeBox code using OttoBot"""
        # from nodebox.util.ottobot import genProgram
        controller = NSDocumentController.sharedDocumentController()
        doc = controller.newDocument_(sender)
        doc = controller.currentDocument()
        doc.textView.setString_(genProgram())
        doc.runScript()

    @objc.IBAction
    def showHelp_(self, sender):
        url = NSURL.URLWithString_("http://nodebox.net/code/index.php/Reference")
        NSWorkspace.sharedWorkspace().openURL_(url)

    @objc.IBAction
    def showSite_(self, sender):
        url = NSURL.URLWithString_("http://nodebox.net/")
        NSWorkspace.sharedWorkspace().openURL_(url)

    @objc.IBAction
    def showLibrary_(self, sender):
        libpath = LibraryFolder()
        url = NSURL.fileURLWithPath_( makeunicode(libpath.libDir) )
        NSWorkspace.sharedWorkspace().openURL_(url)

    def applicationWillTerminate_(self, note):
        # import atexit
        atexit._run_exitfuncs()
