"""
Script for building NodeBox

Usage:
    python setup.py py2app
"""
from distutils.core import setup
from setuptools.extension import Extension

import py2app

import nodebox

NAME = 'NodeBox'
VERSION = nodebox.__version__


AUTHOR = "Frederik De Bleser",
AUTHOR_EMAIL = "frederik@pandora.be",
URL = "http://nodebox.net/",
CLASSIFIERS = (
    "Development Status :: 5 - Production/Stable",
    "Environment :: MacOS X :: Cocoa",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python",
    "Topic :: Artistic Software",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
    "Topic :: Multimedia :: Video",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: User Interfaces",
    "Topic :: Text Editors :: Integrated Development Environments (IDE)",
)

DESCRIPTION = u"Simple application for creating 2-dimensional graphics and animation using Python code"
LONG_DESCRIPTION = u"""NodeBox is a Mac OS X application that allows you to create visual output
with programming code. The application targets an audience of designers, with an easy set of state 
commands that is both intuitive and creative. It is essentially a learning environment and an automation tool.

The current version features:

* State-based graphics context
* Extensive reference documentation and tutorials
* PDF export for graphics
* QuickTime export for animations
* Manipulate every numeric variable in a script by command-dragging it, even during animation
* Creating simple user interfaces using text fields, sliders, and buttons
* Stop a running script by typing command-period
* Universal Binary
* Integrated bezier mathematics and boolean operations
* Command-line interface
* Zooming
"""



creator = 'NdBx'
bundleID = "net.nodebox.NodeBox"

setup(
    
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    classifiers = CLASSIFIERS,


    # data_files=["English.lproj"],

    app=[{
        'script': "macboot.py",

        "plist": {
            "NSPrincipalClass": 'NSApplication',
            "CFBundleIdentifier": bundleID,
            "CFBundleName": NAME,
            "CFBundleSignature": creator,
            "CFBundleShortVersionString": VERSION,
            "CFBundleGetInfoString": DESCRIPTION,
            # "NSHumanReadableCopyright": "",

            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeExtensions': [ 'py' ],
                    'CFBundleTypeIconFile': 'NodeBoxFile.icns',
                    'CFBundleTypeName': "Python File",
                    'CFBundleTypeOSTypes': [ '????', '****', 'utxt'],
                    'CFBundleTypeRole': 'Editor',
                    'NSDocumentClass': u'NodeBoxDocument',
                }
            ]
        }
    }],

    data_files=[
        "Resources/English.lproj/AskString.xib",
        "Resources/English.lproj/Credits.rtf",
        "Resources/English.lproj/ExportImageAccessory.xib",
        "Resources/English.lproj/ExportMovieAccessory.xib",
        "Resources/English.lproj/MainMenu.xib",
        "Resources/English.lproj/NodeBoxDocument.xib",
        "Resources/English.lproj/NodeBoxPreferences.xib",
        "Resources/English.lproj/ProgressBarSheet.xib",
        "Resources/NodeBox.icns",
        "Resources/NodeBoxFile.icns",
        "Resources/zoombig.png",
        "Resources/zoomsmall.png"
        ],

    ext_modules=[
        Extension('cGeo', ['libs/cGeo/cGeo.c']),
        Extension('cPathmatics', ['libs/pathmatics/pathmatics.c']),
        Extension('cPolymagic', ['libs/polymagic/gpc.c', 'libs/polymagic/polymagic.m'],
                extra_link_args=['-framework', 'AppKit', '-framework', 'Foundation'])
    ],

    options={
        "py2app": {
            "iconfile": "Resources/NodeBox.icns",

#             "packages": [
#                 'nodebox',
#                 'nodebox.geo',
#                 'nodebox.graphics',
#                 'nodebox.gui',
#                 'nodebox.gui.mac',
#                 'nodebox.gui.mac.util',
#                 'nodebox.util',
#                 ],

#             "includes": [
#                 'nodebox.geo.pathmatics',
#                 'nodebox.graphics.bezier',
#                 'nodebox.graphics.cocoa',
#                 'nodebox.gui.mac.AskString',
#                 'nodebox.gui.mac.dashboard',
#                 'nodebox.gui.mac.preferences',
#                 'nodebox.gui.mac.progressbar',
#                 'nodebox.gui.mac.PyDETextView',
#                 'nodebox.gui.mac.ValueLadder',
#                 'nodebox.util.kgp',
#                 'nodebox.util.ottobot',
#                 # 'nodebox.PyFontify'
#                 # 'nodebox.util.QTSupport'
#                 ]
        }
    } )
