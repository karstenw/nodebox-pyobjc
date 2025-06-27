"""
Script for building NodeBox

Usage:
    python setup.py py2app
"""

#import setuptools, distutils
#from setuptools.extension import Extension
# from distutils.core import setup, Extension
import platform
from setuptools import setup
from setuptools.extension import Extension

import py2app

import nodebox

machine = platform.machine()

NAME = 'NodeBox'
VERSION = nodebox.__version__
py3 = nodebox.py3

BUNDLENAME = NAME + "_intel"
if machine.startswith("arm"):
    BUNDLENAME = NAME + "_arm"

AUTHOR = "Frederik De Bleser",
AUTHOR_EMAIL = "frederik@pandora.be",
URL = "http://nodebox.net/",
CLASSIFIERS = [
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
]

DESCRIPTION = (u"Simple application for creating 2-dimensional graphics "
               u"and animation using Python code")
LONG_DESCRIPTION = u"""NodeBox is a Mac OS X application that allows you to create visual output with programming code. The application targets an audience of designers, with an easy set of state commands that is both intuitive and creative. It is essentially a learning environment and an automation tool.

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

    app=[{
        'script': "macboot.py",

        "plist": {
            "NSPrincipalClass": 'NodeBoxApplication',
            "CFBundleIdentifier": bundleID,
            "CFBundleName": BUNDLENAME,
            "CFBundleSignature": creator,
            "CFBundleShortVersionString": VERSION,
            "CFBundleGetInfoString": DESCRIPTION,
            "NSHumanReadableCopyright": "Copyright (c) 2015 Frederik De Bleser",

            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeExtensions': [ 'py', 'bot', 'pv' ],
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
        "Resources/English.lproj/AskString.nib",
        "Resources/English.lproj/Credits.rtf",
        "Resources/English.lproj/ExportImageAccessory.nib",
        "Resources/English.lproj/ExportMovieAccessory.nib",
        "Resources/English.lproj/MainMenu.nib",
        "Resources/English.lproj/NodeBoxDocument.nib",
        "Resources/English.lproj/NodeBoxPreferences.nib",
        "Resources/English.lproj/ProgressBarSheet.nib",
        "Resources/NodeBox.icns",
        "Resources/NodeBoxFile.icns",
        "Resources/zoombig.png",
        "Resources/zoomsmall.png"
        ],

    ext_modules=[
        Extension('bwdithering', ['libs/bwdithering/bwdithering.c']),
        Extension('fractal', ['libs/fractal/fractal.c']),
        Extension('cGeo', ['libs/cGeo/cGeo.c']),
        Extension('cPathmatics', ['libs/pathmatics/pathmatics.c']),
        Extension('cPolymagic', ['libs/polymagic/gpc.c', 'libs/polymagic/polymagic.m'],
                extra_link_args=['-framework', 'AppKit', '-framework', 'Foundation'])
    ],

    options={
        "py2app": {
            "iconfile": "Resources/NodeBox.icns",
            "packages": [ "requests", "numpy", #"scipy", "matplotlib", "sympy",
                        # "pandas", "cv2", "dlib", "skimage", "sklearn"],
            ],
            "excludes": [
                'TkInter', 'tkinter', 'tk', 'wx', 'sphinx',
                'pyqt5', 'qt5', 'PyQt5', 
                
                # 'certifi', 'pytz', 
                'notebook', 'nbformat', 'jedi', 'testpath', 'docutils',
                'ipykernel', 'parso', 'Cython', 'sphinx_rtd_theme', 'alabaster',
                'tornado', 'IPython', 'numpydoc', 'nbconvert', 
                'scipy', 'matplotlib', 
                'pandas', 'cv2', 'dlib', 'skimage', 'sklearn', 'mpl_toolkits', 
            ],
        }
    } )
