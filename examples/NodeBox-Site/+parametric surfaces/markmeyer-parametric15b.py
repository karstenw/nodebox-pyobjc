# markmeyer-parametric15b

import numpy as np

#from mmparametriclib import rotate_matrix, project
mmp = ximport("mmparametriclib")
rotate_matrix = mmp.rotate_matrix
project = mmp.project


size(850, 850)
background(0)
nofill()
stroke(0.5, 0.25)
strokewidth(0.5)

translate(WIDTH/2, HEIGHT/2)

# n defines how many vertices we find: the number will be n^2.
# Large values of n can take a while to render!
n = 150

# --- TREFOIL EQUATION ------------------------------------------------------

# Define parametric equations for each axis.
# Although we define an z coordinate,
# it is only used in transformations and shading;
# it is not used in the drawing
# (although it could be if you wanted to add perspective).
r = 120
def x(u, v):
    return  r * np.sin(3*u) / (2 + np.cos(v))

def y(u, v):
    return r * ((  np.sin(u)
                 + 2 * np.sin(2*u))
             / (2 + np.cos(v + 2*np.pi/3)))

def z(u, v):
    return (   r / 2
            * (np.cos(u) - 2 * np.cos(2*u))
            * (2 + np.cos(v))
            * (2 + np.cos(v + 2*np.pi/3)) / 4)

def fit_to_domain(u, v):
    u = -np.pi + u * 2 * np.pi / n
    v = -np.pi + v * 2 * np.pi / (n-1)
    return u, v

def matrix(u, v, index):
    """
    Numeric's fromfunction() gives us integers for each index in the array.
    With matrix() applied, fromfunction() returns an array with all
    the vertices we want.
    """
    # for library purposes this is the responsibility of the caller
    u, v = fit_to_domain(u, v)
    return np.where(index==0, x(u, v),
           np.where(index==1, y(u,v),
           np.where(index==2,  z(u,v), 1)))


# --- ROTATION SLIDERS -----------------------------------------------------

var("rot_x", NUMBER, 0.00, -np.pi, np.pi)
var("rot_y", NUMBER, np.pi/2, -np.pi, np.pi)
var("rot_z", NUMBER, 0.00, -np.pi, np.pi)

# --- LIGHTING SLIDERS -----------------------------------------------------

var("light_x", NUMBER,  1.0, -1.0, 1.0)
var("light_y", NUMBER,  1.0, -1.0, 1.0)
var("light_z", NUMBER,  1.0, -1.0, 1.0)

light = np.array([light_x, light_y, light_z], np.float64)

# --- FACET CULLING --------------------------------------------------------
# Draw only forward facing facets.
view = np.array([0, 0, 1], np.float64)

sphere = np.fromfunction(matrix, (n+1, n+1, 3))
sphere = rotate_matrix(sphere, rot_x, rot_y, rot_z)
project(sphere, light, view)

# z-sort to avoid problems with overlapping surfaces:
sorted_grobs = list(canvas)

def depthsort( a, b ):
    if a.z > b.z:
        return 1
    elif a.z < b.z:
        return -1
    return 0
sortlistfunction( sorted_grobs, depthsort )
canvas._grobs = sorted_grobs
