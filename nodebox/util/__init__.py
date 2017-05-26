import os
import datetime
import glob


import random as librandom
choice = librandom.choice

import unicodedata
import objc

import pdb
import pprint
pp = pprint.pprint


import Foundation
NSMutableAttributedString = Foundation.NSMutableAttributedString
NSMutableStringProxyForMutableAttributedString = Foundation.NSMutableStringProxyForMutableAttributedString

import kgp



__all__ = ('grid', 'random', 'choice', 'files', 'autotext', '_copy_attr', '_copy_attrs',
           'datestring','makeunicode', 'filelist', 'imagefiles')


### Utilities ###

def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    typ = type(s)
    
    # convert to str first; for number types etc.
    if typ not in (str, unicode):
        s = str(s)
    if typ not in (unicode, NSMutableAttributedString, objc.pyobjc_unicode,
                   NSMutableStringProxyForMutableAttributedString):
        try:
            s = unicode(s, srcencoding)
        except TypeError, err:
            print 
            print "makeunicode():", err
            print repr(s)
            print type(s)
            #pdb.set_trace()
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


def filelist( folderpath, pathonly=True ):
    """Walk a folder and return paths for imagefiles."""

    result = []
    for root, dirs, files in os.walk( folderpath ):
        root = makeunicode( root )

        for thefile in files:
            thefile = makeunicode( thefile )
            basename, ext = os.path.splitext(thefile)

            # exclude dotfiles
            if thefile.startswith('.'):
                continue
            
            # exclude that nasty OS trash
            if thefile in (u"Thumbs.db", u"Icon\r"):
                continue

            # exclude the specials
            for item in (u'\r', u'\n', u'\t'):
                if item in thefile:
                    continue

            filepath = os.path.join( root, thefile )

            record = filepath
            if not pathonly:
                info = os.stat( filepath )
                lastmodified = datetime.datetime.fromtimestamp( info.st_mtime )
                record = (filepath, info.st_size, lastmodified, oct(info.st_mode) )
            yield record


def imagefiles( folderpath, pathonly=True ):
    result = []
    filetuples = filelist( folderpath, pathonly=pathonly )
    extensions = tuple(".pdf .eps .tif .tiff .gif .jpg .jpeg .png".split())
    for filetuple in filetuples:
        path = filetuple
        if not pathonly:
            path = filetuple[0]
        _, ext = os.path.splitext( path )
        if ext.lower() not in extensions:
            continue
        if pathonly:
            # result.append( path )
            yield path
        else:
            # result.append( filetuple )
            yield filetuple
    #return result


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

