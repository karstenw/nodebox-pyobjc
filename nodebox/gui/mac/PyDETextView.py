from bisect import bisect
import re
import objc
super = objc.super

import AppKit

NSBackgroundColorAttributeName = AppKit.NSBackgroundColorAttributeName
NSBeep = AppKit.NSBeep
NSColor = AppKit.NSColor
NSCommandKeyMask = AppKit.NSCommandKeyMask
NSDictionary = AppKit.NSDictionary
NSEvent = AppKit.NSEvent
NSFont = AppKit.NSFont
NSFontAttributeName = AppKit.NSFontAttributeName
NSForegroundColorAttributeName = AppKit.NSForegroundColorAttributeName
NSLigatureAttributeName = AppKit.NSLigatureAttributeName
NSLiteralSearch = AppKit.NSLiteralSearch
NSNotificationCenter = AppKit.NSNotificationCenter
NSObject = AppKit.NSObject
NSStringPboardType = AppKit.NSStringPboardType
NSTextStorage = AppKit.NSTextStorage
NSTextStorageEditedCharacters = AppKit.NSTextStorageEditedCharacters
NSTextView = AppKit.NSTextView
NSURL = AppKit.NSURL
NSURLPboardType = AppKit.NSURLPboardType
NSViewWidthSizable = AppKit.NSViewWidthSizable

NSCalibratedRGBColorSpace = AppKit.NSCalibratedRGBColorSpace
NSUserDefaults = AppKit.NSUserDefaults


import nodebox.PyFontify
fontify = nodebox.PyFontify.fontify


import pdb
from nodebox.gui.mac.ValueLadder import ValueLadder
from nodebox.gui.mac.AskStringWindowController import AskStringWindowController

from nodebox.util import _copy_attr, _copy_attrs, makeunicode


whiteRE = re.compile(r"[ \t]+")
commentRE = re.compile(r"[ \t]*(#)")


def AskString(question, resultCallback, default="", parentWindow=None):
    AskStringWindowController(question, resultCallback, default, parentWindow)

def findWhitespace(s, pos=0):
    m = whiteRE.match(s, pos)
    if m is None:
        return pos
    return m.end()


stringPat = r"q[^\\q\n]*(\\[\000-\377][^\\q\n]*)*q"
stringOrCommentPat = stringPat.replace("q", "'") + "|" + stringPat.replace('q', '"') + "|#.*"
stringOrCommentRE = re.compile(stringOrCommentPat)


def removeStringsAndComments(s):
    items = []
    while 1:
        m = stringOrCommentRE.search(s)
        if m:
            start = m.start()
            end = m.end()
            items.append(s[:start])
            if s[start] != "#":
                items.append("X" * (end - start))  # X-out strings
            s = s[end:]
        else:
            items.append(s)
            break
    return "".join(items)



class PyDETextView(NSTextView):

    document = objc.IBOutlet()

    def awakeFromNib(self):
        # Can't use a subclass of NSTextView as an NSTextView in IB,
        # so we need to set some attributes programmatically
        scrollView = self.superview().superview()
        self.setFrame_(((0, 0), scrollView.contentSize()))
        self.setAutoresizingMask_(NSViewWidthSizable)
        self.textContainer().setWidthTracksTextView_(True)
        self.setAllowsUndo_(True)
        self.setRichText_(False)
        self.setTypingAttributes_(getBasicTextAttributes())
        self.setUsesFindPanel_(True)
        self.usesTabs = 0
        self.indentSize = 4
        self._string = self.textStorage().mutableString().nsstring()
        self._storageDelegate = PyDETextStorageDelegate(self.textStorage())
        
        # FDB: no wrapping
        # Thanks to http://cocoa.mamasam.com/COCOADEV/2003/12/2/80304.php
        scrollView = self.enclosingScrollView()
        scrollView.setHasHorizontalScroller_(True)
        self.setHorizontallyResizable_(True)
        layoutSize = self.maxSize()
        layoutSize = (layoutSize[1], layoutSize[1])
        self.setMaxSize_(layoutSize)
        self.textContainer().setWidthTracksTextView_(False)
        self.textContainer().setContainerSize_(layoutSize)

        # FDB: value ladder
        self.valueLadder = None
        
        nc = NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(self, "textFontChanged:",
                                                   "PyDETextFontChanged", None)

    def drawRect_(self, rect):
        NSTextView.drawRect_(self, rect)
        if self.valueLadder is not None and self.valueLadder.visible:
            self.valueLadder.draw()
            
    def hideValueLadder(self):
        if self.valueLadder is not None:            
            self.valueLadder.hide()
            if self.valueLadder.dirty:
                self.document.updateChangeCount_(True)
        self.valueLadder = None

    def mouseUp_(self, event):
        self.hideValueLadder()
        NSTextView.mouseUp_(self, event)
            
    def mouseDragged_(self,event):
        if self.valueLadder is not None:
            self.valueLadder.mouseDragged_(event)
        else:
            NSTextView.mouseDragged_(self, event)

    def mouseDown_(self, event):
        if event.modifierFlags() & NSCommandKeyMask:
            screenPoint = NSEvent.mouseLocation()
            viewPoint =   self.superview().convertPoint_fromView_(event.locationInWindow(),
                                                        self.window().contentView())

            c = self.characterIndexForPoint_(screenPoint)

            txt = self.string()
            # XXX move code into ValueLadder
            try:
                if txt[c] in "1234567890.":
                    # Find full number
                    begin = c
                    end = c
                    try:
                        while txt[begin-1] in "1234567890.":
                            begin-=1
                    except IndexError as err:
                        print( "PyDETextView.mouseDown_() failed to scan number 1." )
                        print( err )
                        # pass
                    try:
                        while txt[end+1] in "1234567890.":
                            end+=1
                    except IndexError as err:
                        print( "PyDETextView.mouseDown_() failed to scan number 2." )
                        print( err )
                        # pass
                    end+=1
                    self.valueLadder = ValueLadder(self,
                                                   eval(txt[begin:end]),
                                                   (begin,end),
                                                   screenPoint, viewPoint)
            except IndexError:
                print( "PyDETextView.mouseDown_() failed to scan number 3." )
                print( err )
                # pass
        else:
            NSTextView.mouseDown_(self,event)

    def acceptableDragTypes(self):
        return list(super(PyDETextView, self).acceptableDragTypes()) + [NSURLPboardType]

    def draggingEntered_(self, dragInfo):
        pboard = dragInfo.draggingPasteboard()
        types = pboard.types()
        if NSURLPboardType in pboard.types():
            # Convert URL to string, replace pboard entry, let NSTextView
            # handle the drop as if it were a plain text drop.
            url = NSURL.URLFromPasteboard_(pboard)
            if url.isFileURL():
                s = url.path()
            else:
                s = url.absoluteString()
            s = 'u"%s"' % s.replace('"', '\\"')
            pboard.declareTypes_owner_([NSStringPboardType], self)
            pboard.setString_forType_(s, NSStringPboardType)
        return super(PyDETextView, self).draggingEntered_(dragInfo)

    def _cleanup(self):
        # delete two circular references
        del self._string
        del self._storageDelegate

    def __del__(self):
        nc = NSNotificationCenter.defaultCenter()
        nc.removeObserver_name_object_(self, "PyDETextFontChanged", None)

    @objc.IBAction
    def jumpToLine_(self, sender):
        # from nodebox.gui.mac.AskString import AskString
        AskString("Jump to line number:", self.jumpToLineCallback_,
                  parentWindow=self.window())

    def jumpToLineCallback_(self, value):
        if value is None:
            return  # user cancelled
        try:
            lineNo = int(value.strip())
        except ValueError:
            NSBeep()
        else:
            self.jumpToLineNr_(lineNo)

    def jumpToLineNr_(self, lineNo):
        lines = self.textStorage().string().splitlines()
        lineNo = min(max(0, lineNo - 1), len(lines))
        length_of_prevs = sum([len(line)+1 for line in lines[:lineNo]])
        curlen = len(lines[lineNo])
        rng = (length_of_prevs, curlen)
        self.setSelectedRange_(rng)
        self.scrollRangeToVisible_(rng)
        self.setNeedsDisplay_(True)

    def textFontChanged_(self, notification):
        basicAttrs = getBasicTextAttributes()
        self.setTypingAttributes_(basicAttrs)
        # Somehow the next line is needed, we crash otherwise :(
        self.layoutManager().invalidateDisplayForCharacterRange_(
                                                        (0, self._string.length()))
        self._storageDelegate.textFontChanged_(notification)

    def setTextStorage_str_tabs_(self, storage, string, usesTabs):
        storage.addLayoutManager_(self.layoutManager())
        self._string = string
        self.usesTabs = usesTabs

    @objc.IBAction
    def changeFont_(self, sender):
        # Change the font through the user prefs API, we'll get notified
        # through textFontChanged_
        font = getBasicTextAttributes()[NSFontAttributeName]
        font = sender.convertFont_(font)
        setTextFont(font)

    def getLinesForRange_(self, rng):
        rng = self._string.lineRangeForRange_(rng)
        return self._string.substringWithRange_(rng), rng

    def getIndent(self):
        if self.usesTabs:
            return "\t"
        else:
            return self.indentSize * " "

    def drawInsertionPointInRect_color_turnedOn_(self, pt, color, on):
        self.insertionPoint = pt
        super(PyDETextView, self).drawInsertionPointInRect_color_turnedOn_(pt, color, on)

    def keyDown_(self, event):
        super(PyDETextView, self).keyDown_(event)
        char = event.characters()[:1]
        if char in ")]}":
            selRng = self.selectedRange()
            line, lineRng, pos = self.findMatchingIndex_paren_(selRng[0] - 1, char)
            if pos is not None:
                self.balanceParens_(lineRng[0] + pos)

    def balanceParens_(self, index):
        rng = (index, 1)
        oldAttrs, effRng = self.textStorage().attributesAtIndex_effectiveRange_(index,
                                                                                None)
        balancingAttrs = {
            NSBackgroundColorAttributeName: NSColor.selectedTextBackgroundColor()
        }
        # Must use temp attrs otherwise the attrs get reset right away due to colorizing.
        self.layoutManager().setTemporaryAttributes_forCharacterRange_(balancingAttrs,
                                                                                rng)
        self.performSelector_withObject_afterDelay_("resetBalanceParens:",
                (oldAttrs, effRng), 0.2)

    def resetBalanceParens_(self, params):
        attrs, rng = params
        self.layoutManager().setTemporaryAttributes_forCharacterRange_(attrs, rng)

    def iterLinesBackwards_maxChars_(self, end, maxChars):
        begin = max(0, end - maxChars)
        if end > 0:
            prevChar = self._string.characterAtIndex_(end - 1)
            if prevChar == "\n":
                end += 1
        lines, linesRng = self.getLinesForRange_((begin, end - begin))
        lines = lines[:end - linesRng[0]]
        linesRng = (linesRng[0], len(lines))
        lines = lines.splitlines(True)
        lines.reverse()
        for line in lines:
            nChars = len(line)
            yield line, (end - nChars, nChars)
            end -= nChars
        assert end == linesRng[0]

    def findMatchingIndex_paren_(self, index, paren):
        openToCloseMap = {"(": ")", "[": "]", "{": "}"}
        if paren:
            stack = [paren]
        else:
            stack = []
        line, lineRng, pos = None, None, None
        for line, lineRng in self.iterLinesBackwards_maxChars_(index, 8192):
            line = removeStringsAndComments(line)
            pos = None
            for i in range(len(line)-1, -1, -1):
                c = line[i]
                if c in ")]}":
                    stack.append(c)
                elif c in "([{":
                    if not stack:
                        if not paren:
                            pos = i
                        break
                    elif stack[-1] != openToCloseMap[c]:
                        # mismatch
                        stack = []
                        break
                    else:
                        stack.pop()
                        if paren and not stack:
                            pos = i
                            break
            if not stack:
                break
        return line, lineRng, pos

    def insertNewline_(self, sender):
        selRng = self.selectedRange()
        super(PyDETextView, self).insertNewline_(sender)
        line, lineRng, pos = self.findMatchingIndex_paren_(selRng[0], None)
        if line is None:
            return
        leadingSpace = ""
        if pos is None:
            m = whiteRE.match(line)
            if m is not None:
                leadingSpace = m.group()
        else:
            leadingSpace = re.sub(r"[^\t]", " ", line[:pos + 1])
        line, lineRng = self.getLinesForRange_((selRng[0], 0))
        line = removeStringsAndComments(line).strip()
        if line and line[-1] == ":":
            leadingSpace += self.getIndent()

        if leadingSpace:
            self.insertText_(leadingSpace)

    def insertTab_(self, sender):
        if self.usesTabs:
            return super(PyDETextView, self).insertTab_(sender)
        self.insertText_("")
        selRng = self.selectedRange()
        assert selRng[1] == 0
        lines, linesRng = self.getLinesForRange_(selRng)
        sel = selRng[0] - linesRng[0]
        whiteEnd = findWhitespace(lines, sel)
        nSpaces = self.indentSize - (whiteEnd % self.indentSize)
        self.insertText_(nSpaces * " ")
        sel += nSpaces
        whiteEnd += nSpaces
        sel = min(whiteEnd, sel + (sel % self.indentSize))
        self.setSelectedRange_((sel + linesRng[0], 0))

    def deleteBackward_(self, sender):
        self.delete_fwd_superf_(sender, False, super(PyDETextView, self).deleteBackward_)

    def deleteForward_(self, sender):
        self.delete_fwd_superf_(sender, True, super(PyDETextView, self).deleteForward_)

    def delete_fwd_superf_(self, sender, isForward, superFunc):
        selRng = self.selectedRange()
        if self.usesTabs or selRng[1]:
            return superFunc(sender)
        lines, linesRng = self.getLinesForRange_(selRng)
        sel = selRng[0] - linesRng[0]
        whiteEnd = findWhitespace(lines, sel)
        whiteBegin = sel
        while whiteBegin and lines[whiteBegin-1] == " ":
            whiteBegin -= 1
        if not isForward:
            white = whiteBegin
        else:
            white = whiteEnd
        if white == sel or (whiteEnd - whiteBegin) <= 1:
            return superFunc(sender)
        nSpaces = (whiteEnd % self.indentSize)
        if nSpaces == 0:
            nSpaces = self.indentSize
        offset = sel % self.indentSize
        if not isForward and offset == 0:
            offset = nSpaces
        delBegin = sel - offset
        delEnd = delBegin + nSpaces
        delBegin = max(delBegin, whiteBegin)
        delEnd = min(delEnd, whiteEnd)
        self.setSelectedRange_((linesRng[0] + delBegin, delEnd - delBegin))
        self.insertText_("")

    @objc.IBAction
    def indent_(self, sender):
        def indentFilter(lines):
            indent = self.getIndent()
            indentedLines = []
            for line in lines:
                if line.strip():
                    indentedLines.append(indent + line)
                else:
                    indentedLines.append(line)
            [indent + line for line in lines[:-1]]
            return indentedLines
        self.filterLines_(indentFilter)

    @objc.IBAction
    def dedent_(self, sender):
        def dedentFilter(lines):
            indent = self.getIndent()
            dedentedLines = []
            indentSize = len(indent)
            for line in lines:
                if line.startswith(indent):
                    line = line[indentSize:]
                dedentedLines.append(line)
            return dedentedLines
        self.filterLines_(dedentFilter)

    @objc.IBAction
    def comment_(self, sender):
        def commentFilter(lines):
            commentedLines = []
            indent = self.getIndent()
            pos = 100
            for line in lines:
                if not line.strip():
                    continue
                pos = min(pos, findWhitespace(line))
            for line in lines:
                if line.strip():
                    commentedLines.append(line[:pos] + "#" + line[pos:])
                else:
                    commentedLines.append(line)
            return commentedLines
        self.filterLines_(commentFilter)

    @objc.IBAction
    def uncomment_(self, sender):
        def uncommentFilter(lines):
            commentedLines = []
            commentMatch = commentRE.match
            for line in lines:
                m = commentMatch(line)
                if m is not None:
                    pos = m.start(1)
                    line = line[:pos] + line[pos+1:]
                commentedLines.append(line)
            return commentedLines
        self.filterLines_(uncommentFilter)

    def filterLines_(self, filterFunc):
        selRng = self.selectedRange()
        lines, linesRng = self.getLinesForRange_(selRng)

        filteredLines = filterFunc(lines.splitlines(True))

        filteredLines = "".join(filteredLines)
        if lines == filteredLines:
            return
        self.setSelectedRange_(linesRng)
        self.insertText_(filteredLines)
        newSelRng = linesRng[0], len(filteredLines)
        self.setSelectedRange_(newSelRng)

class PyDETextStorageDelegate(NSObject):

    def __new__(cls, *args, **kwargs):
        return cls.alloc().init()

    def __init__(self, textStorage=None):
        self._syntaxColors = getSyntaxTextAttributes()
        self._haveScheduledColorize = False
        self._source = None  # XXX
        self._dirty = []
        if textStorage is None:
            textStorage = NSTextStorage.alloc().init()
        self._storage = textStorage
        self._storage.setAttributes_range_(getBasicTextAttributes(),
                (0, textStorage.length()))
        self._string = self._storage.mutableString().nsstring()
        self._lineTracker = LineTracker(self._string)
        self._storage.setDelegate_(self)

    def textFontChanged_(self, notification):
        self._storage.setAttributes_range_(getBasicTextAttributes(),
                (0, self._storage.length()))
        self._syntaxColors = getSyntaxTextAttributes()
        self._dirty = [0]
        self.scheduleColorize()

    def textStorage(self):
        return self._storage

    def string(self):
        return self._string

    def lineIndexFromCharIndex_(self, charIndex):
        return self._lineTracker.lineIndexFromCharIndex_(charIndex)

    def charIndexFromLineIndex_(self, lineIndex):
        return self._lineTracker.charIndexFromLineIndex_(lineIndex)

    def numberOfLines(self):
        return self._lineTracker.numberOfLines()

    def getSource(self):
        if self._source is None:
            # self._source = makeunicode(self._string)
            self._source = self._string
        return self._source

    def textStorageWillProcessEditing_(self, notification):
        if not self._storage.editedMask() & NSTextStorageEditedCharacters:
            return
        rng = self._storage.editedRange()
        # make darn sure we don't get infected with return chars
        s = self._string
        s.replaceOccurrencesOfString_withString_options_range_("\r", "\n",
                                                            NSLiteralSearch , rng)

    def textStorageDidProcessEditing_(self, notification):
        if not self._storage.editedMask() & NSTextStorageEditedCharacters:
            return
        self._source = None
        rng = self._storage.editedRange()
        try:
            self._lineTracker._update(rng, self._storage.changeInLength())
        except:
            import traceback
            traceback.print_exc()
        start = rng[0]
        rng = (0, 0)
        count = 0
        while start > 0:
            # find the last colorized token and start from there.
            start -= 1
            attrs, rng = self._storage.attributesAtIndex_effectiveRange_(start, None)
            value = attrs.objectForKey_(NSForegroundColorAttributeName)
            if value != None:
                count += 1
                if count > 1:
                    break
            # uncolorized section, track back
            start = rng[0] - 1
        rng = self._string.lineRangeForRange_((rng[0], 0))
        self._dirty.append(rng[0])
        self.scheduleColorize()

    def scheduleColorize(self):
        if not self._haveScheduledColorize:
            self.performSelector_withObject_afterDelay_("colorize", None, 0.0)
            self._haveScheduledColorize = True

    def colorize(self):
        self._haveScheduledColorize = False
        self._storage.beginEditing()
        try:
            try:
                self._colorize()
            except:
                import traceback
                traceback.print_exc()
        finally:
            self._storage.endEditing()

    def _colorize(self):
        if not self._dirty:
            return
        storage = self._storage
        source = self.getSource()
        source = source.copy()
        sourceLen = len(source)
        dirtyStart = self._dirty.pop()

        getColor = self._syntaxColors.get
        setAttrs = storage.setAttributes_range_
        getAttrs = storage.attributesAtIndex_effectiveRange_
        basicAttrs = getBasicTextAttributes()

        lastEnd = end = dirtyStart
        count = 0
        sameCount = 0
        
        #plainlength = source.length
        #(void)getCharacters:(unsigned short*)arg1 range:(NSRange)arg2
        #plaintext = source.mutableAttributedString.mutableString
        #for tag, start, end, sublist in fontify(plaintext, dirtyStart):
        for tag, start, end, sublist in fontify(source, dirtyStart):
            end = min(end, sourceLen)
            rng = (start, end - start)
            attrs = getColor(tag)
            oldAttrs, oldRng = getAttrs(rng[0], None)
            if attrs is not None:
                clearRng = (lastEnd, start - lastEnd)
                if clearRng[1]:
                    setAttrs(basicAttrs, clearRng)
                setAttrs(attrs, rng)
                if rng == oldRng and attrs == oldAttrs:
                    sameCount += 1
                    if sameCount > 4:
                        # due to backtracking we have to account for a few more
                        # tokens, but if we've seen a few tokens that were already
                        # colorized the way we want, we're done
                        return
                else:
                    sameCount = 0
            else:
                rng = (lastEnd, end - lastEnd)
                if rng[1]:
                    setAttrs(basicAttrs, rng)
            count += 1
            if count > 200:
                # enough for now, schedule a new chunk
                self._dirty.append(end)
                self.scheduleColorize()
                break
            lastEnd = end
        else:
            # reset coloring at the end
            end = min(sourceLen, end)
            rng = (end, sourceLen - end)
            if rng[1]:
                setAttrs(basicAttrs, rng)


class LineTracker(object):

    def __init__(self, string):
        self.string = string
        self.lines, self.lineStarts, self.lineLengths = self._makeLines()

    def _makeLines(self, start=0, end=None):
        lines = []
        lineStarts = []
        lineLengths = []
        string = self.string
        if end is None:
            end = string.length()
        else:
            end = min(end, string.length())
        rng = string.lineRangeForRange_((start, end - start))
        pos = rng[0]
        end = pos + rng[1]
        while pos < end:
            lineRng = string.lineRangeForRange_((pos, 0))
            line = makeunicode(string.substringWithRange_(lineRng))
            assert len(line) == lineRng[1]
            lines.append(line)
            lineStarts.append(lineRng[0])
            lineLengths.append(lineRng[1])
            if not lineRng[1]:
                break
            pos += lineRng[1]
        return lines, lineStarts, lineLengths

    def _update(self, editedRange, changeInLength):
        oldRange = editedRange[0], editedRange[1] - changeInLength
        start = self.lineIndexFromCharIndex_(oldRange[0])
        if oldRange[1]:
            end = self.lineIndexFromCharIndex_(oldRange[0] + oldRange[1])
        else:
            end = start

        lines, lineStarts, lineLengths = self._makeLines(
            editedRange[0], editedRange[0] + editedRange[1] + 1)
        self.lines[start:end + 1] = lines
        self.lineStarts[start:] = lineStarts  # drop invalid tail
        self.lineLengths[start:end + 1] = lineLengths
        # XXX: This assertion doesn't actually assert
        # assert "".join(self.lines) == unicode(self.string)

    def lineIndexFromCharIndex_(self, charIndex):
        lineIndex = bisect(self.lineStarts, charIndex)
        if lineIndex == 0:
            return 0
        nLines = len(self.lines)
        nLineStarts = len(self.lineStarts)
        if lineIndex == nLineStarts and nLineStarts != nLines:
            # update line starts
            i = nLineStarts - 1
            assert i >= 0
            pos = self.lineStarts[i]
            while pos <= charIndex and i < nLines:
                pos = pos + self.lineLengths[i]
                self.lineStarts.append(pos)
                i += 1
            lineIndex = i

        lineIndex -= 1
        start = self.lineStarts[lineIndex]
        line = self.lines[lineIndex]
        if (    line[-1:] == "\n"
            and not (start <= charIndex < start + self.lineLengths[lineIndex])):
            lineIndex += 1
        return lineIndex

    def charIndexFromLineIndex_(self, lineIndex):
        if not self.lines:
            return 0
        if lineIndex == len(self.lines):
            return self.lineStarts[-1] + self.lineLengths[-1]
        try:
            return self.lineStarts[lineIndex]
        except IndexError:
            # update lineStarts
            for i in range(min(len(self.lines), lineIndex + 1) - len(self.lineStarts)):
                self.lineStarts.append(self.lineStarts[-1] + self.lineLengths[-1])
            # XXX: Assertion doesn't actually assert.
            #assert len(self.lineStarts) == len(self.lineLengths) == len(self.lines)
            if lineIndex == len(self.lineStarts):
                return self.lineStarts[-1] + self.lineLengths[-1]
            return self.lineStarts[lineIndex]

    def numberOfLines(self):
        return len(self.lines)

_basicFont = NSFont.userFixedPitchFontOfSize_(11)

_BASICATTRS = {NSFontAttributeName: _basicFont,
               NSLigatureAttributeName: 0}
_SYNTAXCOLORS = {
    "keyword": {NSForegroundColorAttributeName: NSColor.blueColor()},
    "identifier": {
        NSForegroundColorAttributeName: NSColor.redColor().shadowWithLevel_(0.2)},
    "string": {NSForegroundColorAttributeName: NSColor.magentaColor()},
    "comment": {NSForegroundColorAttributeName: NSColor.grayColor()},
}
for key, value in _SYNTAXCOLORS.items():
    newVal = _BASICATTRS.copy()
    newVal.update(value)
    _SYNTAXCOLORS[key] = NSDictionary.dictionaryWithDictionary_(newVal)
_BASICATTRS = NSDictionary.dictionaryWithDictionary_(_BASICATTRS)


def unpackAttrs(d):
    unpacked = {}
    for key, value in d.items():
        if key == NSFontAttributeName:
            name = value["name"]
            size = value["size"]
            value = NSFont.fontWithName_size_(name, size)
        elif key in (NSForegroundColorAttributeName, NSBackgroundColorAttributeName):
            r, g, b, a = map(float, value.split())
            value = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)
        elif isinstance(value, (dict, NSDictionary)):
            value = unpackAttrs(value)
        unpacked[key] = value
    return unpacked

def packAttrs(d):
    packed = {}
    for key, value in d.items():
        if key == NSFontAttributeName:
            value = {"name": value.fontName(), "size": value.pointSize()}
        elif key in (NSForegroundColorAttributeName, NSBackgroundColorAttributeName):
            col = value.colorUsingColorSpaceName_(NSCalibratedRGBColorSpace)
            channels = col.getRed_green_blue_alpha_(None, None, None, None)
            value = " ".join(map(str, channels))
        elif isinstance(value, (dict, NSDictionary)):
            value = packAttrs(value)
        packed[key] = value
    return packed


def getBasicTextAttributes():
    attrs = NSUserDefaults.standardUserDefaults().objectForKey_(
            "PyDEDefaultTextAttributes")
    return unpackAttrs(attrs)

def getSyntaxTextAttributes():
    attrs = NSUserDefaults.standardUserDefaults().objectForKey_(
            "PyDESyntaxTextAttributes")
    return unpackAttrs(attrs)

def setBasicTextAttributes(basicAttrs):
    if basicAttrs != getBasicTextAttributes():
        NSUserDefaults.standardUserDefaults().setObject_forKey_(
                packAttrs(basicAttrs), "PyDEDefaultTextAttributes")
        nc = NSNotificationCenter.defaultCenter()
        nc.postNotificationName_object_("PyDETextFontChanged", None)

def setSyntaxTextAttributes(syntaxAttrs):
    if syntaxAttrs != getSyntaxTextAttributes():
        NSUserDefaults.standardUserDefaults().setObject_forKey_(
                packAttrs(syntaxAttrs), "PyDESyntaxTextAttributes")
        nc = NSNotificationCenter.defaultCenter()
        nc.postNotificationName_object_("PyDETextFontChanged", None)

def setTextFont(font):
    basicAttrs = getBasicTextAttributes()
    syntaxAttrs = getSyntaxTextAttributes()
    basicAttrs[NSFontAttributeName] = font
    for v in syntaxAttrs.values():
        v[NSFontAttributeName] = font
    setBasicTextAttributes(basicAttrs)
    setSyntaxTextAttributes(syntaxAttrs)

_defaultUserDefaults = {
    "PyDEDefaultTextAttributes": packAttrs(_BASICATTRS),
    "PyDESyntaxTextAttributes": packAttrs(_SYNTAXCOLORS),
}

NSUserDefaults.standardUserDefaults().registerDefaults_(_defaultUserDefaults)
