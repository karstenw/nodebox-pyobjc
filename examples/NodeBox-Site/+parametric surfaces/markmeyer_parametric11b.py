# markmeyer_parametric11b

import math
import numpy as np

from mmparametriclib import rotate_matrix, length, normalize_vector

sin = math.sin
cos = math.cos
pi = math.pi
e = math.e
sqrt = math.sqrt




cell = 550
size( cell, cell )
background(0)
nofill()
stroke(0.6, 0.6, 0.7, 0.35)
strokewidth(0.5)

translate(WIDTH/2, HEIGHT/2)
 
# n defines how many vertices we find: the number will be n^2.
# Large values of n can take a while to render!
n = 27
 
# --- SPHERE EQUATION ------------------------------------------------------
 
# Define parametric equations for each axis.
# Although we define an z coordinate, 
# it is only used in transformations and shading; 
# it is not used in the drawing 
# (although it could be if you wanted to add perspective).
r = 240
def x(u, v): return r * np.sin(u) * np.cos(v)
def y(u, v): return r * np.sin(u) * np.sin(v)
def z(u, v): return r * np.cos(u)

def fit_to_domain(u, v):
    u = 1.0 * u/n * np.pi
    v = 1.0 * v/n * np.pi*2
    return u, v
 
# from Numeric import *
def matrix(u, v, index):
    u, v = fit_to_domain(u, v)
    return np.where(index==0, x(u, v),
                 np.where(index==1, y(u,v),
                    np.where(index==2,  z(u,v), 1)
                    )
                 )

# --- ORTHOGRAPHIC PROJECTION ----------------------------------------------
 
def project(rows):
    """
    Go through the array and draw rectangles.
    There is probably a more efficent way to do this.
    """
    for i in range(len(rows) -1):
        for j in range(len(rows[i])-1):
            face = rows[i:i+2, j:j+2]
            light_angle = (np.dot(normalize_vector(face), light))
            if (light_angle < 0): 
                light_angle = 0
            fill(
                light_angle + 0.02, 
                light_angle + 0.04,  
                light_angle + 0.08,
                1.0
            )
            beginpath(
                face[0, 0, 0], 
                face[0, 0, 1]
            ) 
            lineto(
                face[1, 0, 0], 
                face[1, 0, 1]
            )
            lineto(
                face[1, 1, 0], 
                face[1, 1, 1]
            )
            lineto(
                face[0, 1, 0], 
                face[0, 1, 1]
            )
            path = endpath()
 
# --- ROTATION SLIDERS -----------------------------------------------------
 
var("rot_x", NUMBER, 0.0, -pi, pi)
var("rot_y", NUMBER, 0.5, -pi, pi)
var("rot_z", NUMBER, 0.5, -pi, pi)
 
# --- LIGHTING SLIDERS -----------------------------------------------------
 
var("light_x", NUMBER, 0.0, -1.0, 1.0)
var("light_y", NUMBER, 0.0, -1.0, 1.0)
var("light_z", NUMBER, 0.5, -1.0, 1.0)
 
light = np.array([light_x, light_y, light_z], np.float64)
 
sphere = np.fromfunction(matrix, (n+1, n+1, 3))
sphere = rotate_matrix(sphere, rot_x, rot_y, rot_z)
project(sphere)

