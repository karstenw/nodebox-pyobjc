import os
import time
import datetime
import glob

import tempfile

import random as librandom
choice = librandom.choice

import unicodedata

import pdb
import pprint
pp = pprint.pprint

import PIL
import numpy as np

import objc
import Foundation
import AppKit
import PyObjCTools.Conversion

from . import kgp


__all__ = (
    'grid', 'random', 'choice', 'files', 'autotext',
    '_copy_attr',
    '_copy_attrs',
    'datestring','makeunicode', 'filelist', 'imagefiles',
    'fontnames', 'fontfamilies',
    'voices', 'voiceattributes', 'anySpeakers', 'say',
    'imagepalette', 'aspectRatio', 'dithertypes', 'ditherimage',
    'sortlistfunction')


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

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def sortlistfunction(thelist, thecompare):
    if py3:
        sortkeyfunction = cmp_to_key( thecompare )
        thelist.sort( key=sortkeyfunction )
    else:
        thelist.sort( thecompare )

g_voicetrash = []

_dithertypes = {
    'atkinson': 1,
    'floyd-steinberg': 2,
    'jarvis-judice-ninke': 3,
    'stucki': 4,
    'burkes': 5,
    'sierra-1': 6,
    'sierra-2': 7,
    'sierra-3': 8,
}

_ditherIDs = _dithertypes.values()



def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):

    if type(s) not in ( pstr,
                    punicode,
                    Foundation.NSMutableAttributedString,
                    objc.pyobjc_unicode,
                    Foundation.NSMutableStringProxyForMutableAttributedString,
                    Foundation.NSString):
        s = str(s)
    if type(s) not in (
            punicode,
            #Foundation.NSMutableAttributedString,
            #objc.pyobjc_unicode,
            #Foundation.NSMutableStringProxyForMutableAttributedString
            ):
        try:
            s = punicode(s, srcencoding)
        except TypeError as err:
            
            #print() 
            #print("makeunicode(): %s" % err)
            #print(repr(s))
            #print(type(s))
            #print()
            pass
    if type(s) in ( punicode,
                    #Foundation.NSMutableAttributedString,
                    #objc.pyobjc_unicode,
                    #Foundation.NSMutableStringProxyForMutableAttributedString,
                    #Foundation.NSString
                    ):
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
        librandom.shuffle(rowRange)
        librandom.shuffle(colRange)
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


def autotext(sourceFile):
    k = kgp.KantGenerator(sourceFile)
    return k.output()


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
    if type(folderpathorlist) in (pstr, punicode):
        folders = [folderpathorlist]
    result = []
    for folder in folders:
        folder = os.path.expanduser( folder )
        folder = os.path.abspath( folder )
        for root, dirs, files in os.walk( folder ):
            root = makeunicode( root )

            # skip if dir starts with '.'
            _, parentfolder = os.path.split(root)
            if parentfolder and parentfolder[0] == u".":
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
        # filter out the weird fontnames
        if i.startswith(u'.'):
            continue
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


def voices():
    """Return a list of voice names."""
    vcs = AppKit.NSSpeechSynthesizer.availableVoices()
    vcs = [makeunicode(t) for t in vcs]
    vcs = [x.replace(u"com.apple.speech.synthesis.voice.", u"") for x in vcs]
    return vcs


def voiceattributes(voice):
    """Return a dict with attributes for voice.
    
    voice is passed without the 'com.apple.speech.synthesis.voice.' prefix, e.g.
    'Albert' or 'petra.premium'.
    """
    result = {}
    if voice and voice in voices():
        voice = u"com.apple.speech.synthesis.voice.%s" % (voice,)
        attrs = AppKit.NSSpeechSynthesizer.attributesForVoice_( voice )
        result = PyObjCTools.Conversion.pythonCollectionFromPropertyList(attrs)
        keys = result.keys()
        for key  in keys:
            result[key] = makeunicode(result[key])
    return result


def anySpeakers():
    """Return if ANY application is currently speaking."""
    global g_voicetrash

    b = bool(AppKit.NSSpeechSynthesizer.isAnyApplicationSpeaking())
    if b == False:
        # empty accumulated voices
        while len(g_voicetrash) > 0:
            f = g_voicetrash.pop()
            del f
    return b


def say(txt, voice=None, outfile=None, wait=True):
    """Say txt with a voice. Write AIFF file to outfile if parent(outfile) exists.
    defer return if wait is True.
    """
    global g_voicetrash
    if voice and voice in voices():
        voice = u"com.apple.speech.synthesis.voice.%s" % (voice,)
    else:
        voice = AppKit.NSSpeechSynthesizer.defaultVoice()
    
    # outfile is a path to an AIFF file to be exported to
    # if the containing folder does not exist, abort
    path = url = None
    if outfile:
        path = os.path.abspath( makeunicode(outfile) )
        folder, filename = os.path.split( path )
        if not os.path.exists( folder ):
            path = None

    if path:
        url = Foundation.NSURL.fileURLWithPath_isDirectory_( path, False )
    speaker = AppKit.NSSpeechSynthesizer.alloc().initWithVoice_(voice)

    if speaker and url:
        g_voicetrash.append( speaker )
        speaker.startSpeakingString_toURL_(txt, url)
        return speaker

    if speaker:
        if wait:
            while anySpeakers():
                time.sleep(0.1)
        # it is importatnt that speaker gets added AFTER anySpeakers()
        # it does garbage collection
        g_voicetrash.append( speaker )
        speaker.startSpeakingString_(txt)
        return speaker


def aspectRatio(size, maxsize=None, maxw=None, maxh=None):
    """scale a size tuple (w,h) to 
        - maxsize (max w or h)
        - or max width maxw
        - or max height maxh."""
    w, h = size
    denom = maxcurrent = 1

    if maxsize:
        maxcurrent = max(size)
        denom = maxsize
    elif maxw:
        maxcurrent = w
        denom = maxw
    elif maxh:
        maxcurrent = h
        denom = maxh

    if maxcurrent == denom:
        return size
    elif maxsize == 0:
        return size

    ratio = maxcurrent / float(denom)

    neww = int(round(w / ratio))
    newh = int(round(h / ratio))
    return neww, newh


def palette(pilimage, mask):
    """
    Return palette in descending order of frequency
    """
    result = []
    arr = np.asarray(pilimage)
    if mask != None:
        if 0 <= mask <= 255:
            arr = arr & int(mask)
    palette, index = np.unique(asvoid(arr).ravel(), return_inverse=True)
    palette = palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    count = np.bincount(index)
    order = np.argsort(count)
    
    p = palette[order[::-1]]

    for col in p:
        r,g,b = col
        
        result.append( (r / 255.0, g / 255.0, b / 255.0) )
    return result


def asvoid(arr):
    """View the array as dtype np.void (bytes)
    This collapses ND-arrays to 1D-arrays, so you can perform 1D operations on them.
    http://stackoverflow.com/a/16216866/190597 (Jaime)
    http://stackoverflow.com/a/16840350/190597 (Jaime)
    Warning:
    >>> asvoid([-0.]) == asvoid([0.])
    array([False], dtype=bool)
    """
    arr = np.ascontiguousarray(arr)
    result = arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))
    return result


def imagepalette( pathOrPILimgage, mask=None ):
    t = type(pathOrPILimgage)
    result = []
    if t in (pstr, punicode):
        f = PIL.Image.open( pathOrPILimgage )
        f = f.convert("RGB")
        result = palette( f, mask )
    else:
        try:
            result = palette( pathOrPILimgage, mask )
        except Exception as err:
            pass
    return result


def tempimagepath(mode='w+b', suffix='.png'):
    """Create a temporary file with mode and suffix.
    Returns pathstring."""
    fob = tempfile.NamedTemporaryFile(mode=mode, suffix=suffix, delete=False)
    fname = fob.name
    fob.close()
    return fname


def dithertypes():
    """Return names of all supported dither types."""
    return list(_dithertypes.keys())


def ditherimage(pathOrPILimgage, dithertype, threshhold):
    # argh, a circular import. Dang!
    from nodebox.geo import dither

    t = type(pathOrPILimgage)

    if dithertype in list(_dithertypes):
        dithername = dithertype
        ditherid = _dithertypes.get( dithertype )
    elif dithertype in _ditherIDs:
        ditherid = dithertype
        dithername = _dithertypes.get( dithertype )
        # pass
    else:
        ditherid = 0
        dithername = "unknown"

    if t in (pstr, punicode):
        img = PIL.Image.open( pathOrPILimgage ).convert('L')
    else:
        img = pathOrPILimgage

    # pdb.set_trace()

    w, h = img.size
    bin = img.tobytes(encoder_name='raw')
    resultimg = bytearray( len(bin) )
    result = dither(bin, w, h, ditherid, threshhold)
    # result = dither(bin, resultimg, w, h, ditherid, threshhold)

    out = PIL.Image.frombytes( 'L', (w,h), result, decoder_name='raw')

    name = "dither_%s_%s.png" % (datestring(nocolons=True), dithername)
    out.convert('1').save(name, format="PNG")
    del out, bin, result
    if img != pathOrPILimgage:
        del img
    return os.path.abspath(name)


def _copy_attr(v):
    if v is None:
        return None
    elif hasattr(v, "copy"):
        return v.copy()
    elif isinstance(v, list):
        return list(v)
    elif isinstance(v, tuple):
        return tuple(v)
    elif isinstance(v, (int, pstr, punicode, float, bool, long)):
        return v
    else:
        raise NodeBoxError("Don't know how to copy '%s'." % v)


def _copy_attrs(source, target, attrs):
    for attr in attrs:
        setattr(target, attr, _copy_attr(getattr(source, attr)))


