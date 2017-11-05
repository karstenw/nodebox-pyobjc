#### How to use the integrated matplotlib

##### Step 1: Do your imports

```
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
```

Lines 3-6 prepare for a temp file which will be ``ìmage```'d at the end of the script.



##### Step 2: Do some fancy matplotlib stuff (or go through a tutorial)

```
X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)



plt.plot(X, C)
plt.plot(X, S)

```


##### Step 3: Conclude the script

```
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
```

This saves the plot in the temp file, cleares the figure cache, displays the generated image in NodeBox-land and deletes the temp file.

The figure cache clearing is necessary since matplotlib caches generated plots and accumulates them.