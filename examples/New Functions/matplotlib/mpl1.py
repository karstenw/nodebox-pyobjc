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


from scipy import special, optimize

f = lambda x: -special.jv(3, x)
sol = optimize.minimize(f, 1.0)
x = np.linspace(0, 10, 5000)

plt.plot(x, special.jv(3, x), '-', sol.x, -sol.fun, 'o')

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
