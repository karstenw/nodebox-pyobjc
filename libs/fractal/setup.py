from distutils.core import setup, Extension

fractal = Extension("fractal", sources = ["fractal.c"])

setup (name = "fractal",
       version = "0.1",
       author = "Karsten Wolf",
       description = "Fractals in C.",
       ext_modules = [fractal])

