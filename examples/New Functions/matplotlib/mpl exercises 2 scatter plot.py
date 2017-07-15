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

# code from http://www.scipy-lectures.org/intro/matplotlib/auto_examples/plot_scatter_ex.html


n = 1024
X = np.random.normal(0, 1, n)
Y = np.random.normal(0, 1, n)
T = np.arctan2(Y, X)

plt.axes([0.025, 0.025, 0.95, 0.95])
plt.scatter(X, Y, s=75, c=T, alpha=.5)

plt.xlim(-1.5, 1.5)
plt.xticks(())
plt.ylim(-1.5, 1.5)
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
