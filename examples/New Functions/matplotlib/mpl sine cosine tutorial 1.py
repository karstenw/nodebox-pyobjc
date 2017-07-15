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

# code from http://www.scipy-lectures.org/intro/matplotlib/matplotlib.html



X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)



plt.plot(X, C)
plt.plot(X, S)


# save the plot and load it as an image...
plt.savefig(fname, dpi=150)

# clear last plot
# pyplots overlap between runs. If that's a desired feature,
# comment the following three lines.
plt.cla()
plt.clf()
plt.close('all')

image(fname, 0, 0)
os.remove( fname )