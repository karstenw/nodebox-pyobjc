

import numpy as np
from pprint import pprint as pp

# from mmparametriclib import matrix

cell = 896
size( cell, cell )
background(0)
nofill()
stroke(0.6, 0.6, 0.7, 0.35)
strokewidth(0.5)
 
translate(WIDTH/2, HEIGHT/2)
 
# n defines how many vertices we find: the number will be n^2.
# Large values of n can take a while to render!
n = 18

# --- FUNNEL EQUATION -------------------------------------------------------

# Define parametric equations for each axis.
# Although we define an z coordinate,
# it is only used in transformations and shading; 
# it is not used in the drawing 
# (although it could be if you wanted to add perspective).
r = 400

def x(u, v):
    return r * np.sin(u) * np.cos(v)

def y(u, v):
    return r * np.sin(u) * np.sin(v)

def z(u, v):
    return r * np.cos(u)
 
def fit_to_domain(u, v):
    u = 1.0 * u / n * np.pi
    v = 1.0 * v / n * np.pi * 2
    return u, v


def matrix(u, v, index):
    """
    Numeric's fromfunction() gives us integers for each index in the array.
    With matrix() applied, fromfunction() returns an array with all 
    the vertices we want. 
    """
    # for library purposes this is the responsibility of the caller
    #
    # not now - matrix needs to be individualized
    #
    u, v = fit_to_domain(u, v)
    return np.where(index==0, x(u, v),
           np.where(index==1, y(u, v),
           np.where(index==2, z(u, v),
                    1)))


def project(rows):
    """
    Go through the array and draw rectangles.
    There is probably a more efficent way to do this.
    """
    for i in range(len(rows)-1):
        for j in range(len(rows[i])-1):
            beginpath(
                rows[i][j][0], 
                rows[i][j][1]
            ) 
            lineto(
                rows[i+1][j][0], 
                rows[i+1][j][1]
            )
            lineto(
                rows[i+1][j+1][0], 
                rows[i+1][j+1][1]
            )
            lineto(
                rows[i][j+1][0], 
                rows[i][j+1][1]
            )
            endpath()
            
sphere = np.fromfunction(matrix, (n+1, n+1, 3))
# pp(sphere)
project(sphere)

