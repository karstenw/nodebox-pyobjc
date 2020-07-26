from distutils.core import setup, Extension

bwdither = Extension("bwdither", sources = ["bwdithering.c"])

setup (name = "bwdither",
       version = "0.1",
       author = "Karsten Wolf",
       description = "Atkinson, Floyd-Steinberg and other ditherings of grayscale images.",
       ext_modules = [bwdither])

