from distutils.core import setup, Extension

atkinsondither = Extension("bwdither", sources = ["bwdithering.c"])

setup (name = "bwdither",
       version = "0.1",
       author = "Karsten Wolf",
       description = "Atkinson, Floyd-Steinberg and other ditherings of grayscale images.",
       ext_modules = [bwdithering])

