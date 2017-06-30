import os
import datetime
import glob


import random as librandom
choice = librandom.choice

import unicodedata
import objc

import Foundation
import AppKit

import kgp


__all__ = ('grid', 'random', 'choice', 'files', 'autotext', '_copy_attr', '_copy_attrs',
           'datestring','makeunicode', 'filelist', 'imagefiles',
           'fontnames', 'fontfamilies')


### Utilities ###

def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    typ = type(s)
    # convert to str first; for number types etc.
    if typ not in (str, unicode, Foundation.NSMutableAttributedString,
        objc.pyobjc_unicode, Foundation.NSMutableStringProxyForMutableAttributedString,
        Foundation.NSString):
        # print "makeunicode() convert:", typ
        s = str(s)
    if typ not in (unicode, Foundation.NSMutableAttributedString, objc.pyobjc_unicode,
                   Foundation.NSMutableStringProxyForMutableAttributedString):
        try:
            s = unicode(s, srcencoding)
        except TypeError, err:
            print 
            print "makeunicode():", err
            print repr(s)
            print type(s)
            print
    if typ in (unicode,):
        s = unicodedata.normalize(normalizer, s)
    return s


def datestring(dt = None, dateonly=False, nospaces=True, nocolons=True):
    """Make an ISO datestring. The defaults are good for using the result of
    'datestring()' in a filename.
    """
    if not dt:
        now = str(datetime.datetime.now())
    else:
        now = str(dt)
    if not dateonly:
        now = now[:19]
    else:
        now = now[:10]
    if nospaces:
        now = now.replace(" ", "_")
    if nocolons:
        now = now.replace(":", "")
    return now


def grid(cols, rows, colSize=1, rowSize=1, shuffled=False):
    """Returns an iterator that contains coordinate tuples.
    
    The grid can be used to quickly create grid-like structures.
    A common way to use them is:
        for x, y in grid(10,10,12,12):
            rect(x,y, 10,10)
    """
    # Prefer using generators.
    rowRange = xrange(int(rows))
    colRange = xrange(int(cols))
    # Shuffled needs a real list, though.
    if (shuffled):
        rowRange = list(rowRange)
        colRange = list(colRange)
        shuffle(rowRange)
        shuffle(colRange)
    for y in rowRange:
        for x in colRange:
            yield (x*colSize,y*rowSize)

def random(v1=None, v2=None):
    """Returns a random value.
    
    This function does a lot of things depending on the parameters:
    - If one or more floats is given, the random value will be a float.
    - If all values are ints, the random value will be an integer.
    
    - If one value is given, random returns a value from 0 to the given value.
      This value is not inclusive.
    - If two values are given, random returns a value between the two; if two
      integers are given, the two boundaries are inclusive.
    """
    if v1 != None and v2 == None: # One value means 0 -> v1
        if isinstance(v1, float):
            return librandom.random() * v1
        else:
            return int(librandom.random() * v1)
    elif v1 != None and v2 != None: # v1 -> v2
        if isinstance(v1, float) or isinstance(v2, float):
            start = min(v1, v2)
            end = max(v1, v2)
            return start + librandom.random() * (end-start)
        else:
            start = min(v1, v2)
            end = max(v1, v2) + 1
            return int(start + librandom.random() * (end-start))
    else: # No values means 0.0 -> 1.0
        return librandom.random()


def files(path="*"):
    """Returns a list of files.
    
    You can use wildcards to specify which files to pick, e.g.
        f = files('*.gif')
    """
    f = glob.glob(path)
    f = [makeunicode(t) for t in f]
    return f


def filelist( folderpathorlist, pathonly=True ):
    """Walk a folder or a list of folders and return
    paths or ((filepath, size, lastmodified, mode) tuples..
    """

    folders = folderpathorlist
    if type(folderpathorlist) in (str, unicode):
        folders = [folderpathorlist]
    result = []
    for folder in folders:
        folder = os.path.expanduser( folder )
        folder = os.path.abspath( folder )
        for root, dirs, files in os.walk( folder ):
            root = makeunicode( root )

            # skip if dir starts with '.'
            _, parentfolder = os.path.split(root)
            if parentfolder[0] == u".":
                continue

            for thefile in files:
                thefile = makeunicode( thefile )
                basename, ext = os.path.splitext(thefile)

                # exclude dotfiles
                if thefile.startswith('.'):
                    continue

                # exclude the specials
                for item in (u'\r', u'\n', u'\t'):
                    if item in thefile:
                        continue

                filepath = os.path.join( root, thefile )

                record = filepath
                if not pathonly:
                    islink = os.path.islink( filepath )
                    if islink:
                        info = os.lstat( filepath )
                    else:
                        info = os.stat( filepath )
                    lastmodified = datetime.datetime.fromtimestamp( info.st_mtime )
                    record = (filepath, info.st_size, lastmodified,
                              oct(info.st_mode), islink )
                yield record


def imagefiles( folderpathorlist, pathonly=True ):
    """Use filelist to extract all imagefiles"""
    result = []
    filetuples = filelist( folderpathorlist, pathonly=pathonly )

    # 2017-06-23 - kw .eps dismissed
    extensions = tuple(".pdf .tif .tiff .gif .jpg .jpeg .png".split())
    for filetuple in filetuples:
        path = filetuple
        if not pathonly:
            path = filetuple[0]
        _, ext = os.path.splitext( path )
        if ext.lower() not in extensions:
            continue
        if pathonly:
            yield path
        else:
            yield filetuple

def fontnames():
    fm = AppKit.NSFontManager.sharedFontManager()
    l = fm.availableFonts()
    result = []
    for i in l:
        result.append( makeunicode(i) )
    return result


class FontRecord:
    def __init__(self, psname, familyname, style, weight, traits, traitnames):
        self.psname = psname
        self.familyname = familyname
        self.style = style
        self.weight = weight
        self.traits = traits
        self.traitnames = traitnames
    def __repr__(self):
        return (u'FontRecord( psname="%s", familyname="%s", style="%s", '
                u'weight=%.2f, traits="%s", traitnames=%s)') % (
                            self.psname, self.familyname, self.style,
                            self.weight, self.traits, self.traitnames)


def fontfamilies(flat=False):
    fm = AppKit.NSFontManager.sharedFontManager()
    l = fm.availableFontFamilies()

    def makeTraitsList( traits ):
        appleTraits = {
            0x00000001: u"italic",
            0x00000002: u"bold",
            0x00000004: u"unbold",
            0x00000008: u"nonstandardcharacterset",
            0x00000010: u"narrow",
            0x00000020: u"expanded",
            0x00000040: u"condensed",
            0x00000080: u"smallcaps",
            0x00000100: u"poster",
            0x00000200: u"compressed",
            0x00000400: u"fixedpitch",
            0x01000000: u"unitalic"}
        result = []
        keys = appleTraits.keys()
        for key in keys:
            if traits & key == key:
                result.append( appleTraits[key])
        return result

    def makeFontRecord(fnt):
        psname, styl, weight, traits = fnt
        psname = makeunicode(psname)
        styl = makeunicode(styl)
        weight = float( weight )
        traits = int(traits)
        traitNames = makeTraitsList( traits )
        return FontRecord(psname, familyName, styl, weight, traits, traitNames)
        
    if flat:
        result = []
    else:
        result = {}
    for fn in l:
        familyName = makeunicode( fn )
        if not flat:
            result[familyName] = famfonts = {}

        subs = fm.availableMembersOfFontFamily_( familyName )
        for fnt in subs:
            fontRec = makeFontRecord( fnt )
            if not flat:
                result[familyName][fontRec.style] = fontRec
            else:
                result.append( fontRec )
    return result

def autotext(sourceFile):
    k = kgp.KantGenerator(sourceFile)
    return k.output()


def _copy_attr(v):
    if v is None:
        return None
    elif hasattr(v, "copy"):
        return v.copy()
    elif isinstance(v, list):
        return list(v)
    elif isinstance(v, tuple):
        return tuple(v)
    elif isinstance(v, (int, str, unicode, float, bool, long)):
        return v
    else:
        raise NodeBoxError, "Don't know how to copy '%s'." % v

def _copy_attrs(source, target, attrs):
    for attr in attrs:
        setattr(target, attr, _copy_attr(getattr(source, attr)))

