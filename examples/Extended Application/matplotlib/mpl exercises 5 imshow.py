import sys
import os
import tempfile
fob = tempfile.NamedTemporaryFile(mode='w+b', suffix='.png', delete=False)
fname = fob.name
fob.close()
import numpy as np
import scipy

import matplotlib
import matplotlib.pyplot as plt


dpi = 150

# code from http://www.scipy-lectures.org/intro/matplotlib/auto_examples/plot_imshow_ex.html


def f(x, y):
    return (1 - x / 2 + x ** 5 + y ** 3 ) * np.exp(-x ** 2 - y ** 2)

n = 10
x = np.linspace(-3, 3, 3.5 * n)
y = np.linspace(-3, 3, 3.0 * n)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

plt.axes([0.025, 0.025, 0.95, 0.95])
plt.imshow(Z, interpolation='nearest', cmap='bone', origin='lower')
plt.colorbar(shrink=.92)

plt.xticks(())
plt.yticks(())

# save the plot and load it as an image...
plt.savefig(fname, dpi=dpi)

# clear last plot
# pyplots overlap between runs. If that's a desired feature,
# comment the following three lines.
plt.cla()
plt.clf()
plt.close('all')

image(fname, 0, 0)
# print fname
os.remove( fname )
