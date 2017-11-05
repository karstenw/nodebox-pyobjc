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

# code from http://www.scipy-lectures.org/intro/matplotlib/auto_examples/plot_pie_ex.html

n = 20

N = np.ones(n)
Z = np.ones(n)
Z[-1] *= 2
Z[1] = 4
Z[10] = 3

plt.axes([0.025, 0.025, 0.95, 0.95])

plt.pie(Z, explode=Z*0.05, colors = ['%f' % (i/float(n)) for i in range(n)])
plt.axis('equal')
plt.xticks(())
plt.yticks()

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
