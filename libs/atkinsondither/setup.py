from distutils.core import setup, Extension

atkinsondither = Extension("atkinsondither", sources = ["atkinsondither.c"])

setup (name = "atkinsondither",
       version = "0.1",
       author = "Karsten Wolf",
       description = "Atkinson dither of grayscale image.",
       ext_modules = [atkinsondither])

