#  "Toroidal Polyhedron4" (by Dr. Ozan Yarman @ http://www.ozanyarman.com )
# http://support.nodebox.net/discussions/show-your-work/81-toroidal-polyhedron-code-based-on-torus-by-mark-meyer
#
#
# Based on the original "Torus" code by Mark Meyer @
# https://www.nodebox.net/code/index.php/Mark_Meyer_%7c_Parametric_surfaces_%7c_torus

import numpy as np

size(486, 486)
background(1)
nofill()
stroke(0.6, 5.6, 2.7, 0.65)
strokewidth(0.5)
 
translate(WIDTH/2, HEIGHT/2)
 
# n defines how many vertices we find: the number will be n^2.
# Large values of n can take a while to render!

# Utilize only integer numbers for n and m.

n = 8 # number of sides along the axis of revolution
m = 6 # number of sides around the poloidal axis
k = 4 # normalized phase of generator around the axis of revolution
q = float(n)/m
w = float(n)/n

 
# --- TORUS EQUATION --------------------------------------------------------
 
# Define parametric equations for each axis.
# Although we define an z coordinate,
# it is only used in transformations and shading;
# it is not used in the drawing
# (although it could be if you wanted to add perspective).
r1 = 155
r2 = 60
def x(u, v): return (r1 + r2 * np.cos(v)) * np.cos(u)
def y(u, v): return (r1 + r2 * np.cos(v)) * np.sin(u)
def z(u, v): return r2 * np.sin(v)
 
def fit_to_domain(u, v):
    u = w * u/n * np.pi*2
    v = q * v/n * np.pi*2 + ((k*np.pi)/(2*m))
    return u, v
 
# from Numeric import *
def matrix(u, v, index):
    u, v = fit_to_domain(u, v)
    return np.where(index==0, x(u, v),
           np.where(index==1, y(u, v),
           np.where(index==2, z(u, v), 1)))

# --- MATRIX ROTATION ------------------------------------------------------

def rotate_matrix(matrix, x, y, z):
    rot_x = np.array(
        ([0, np.cos(np.pi*x), -np.sin(np.pi*x)],
         [0, np.sin(np.pi*x),  np.cos(np.pi*x)],
         [1, 0, 0]
        ), np.float64
    )
    rot_y = np.array(
        ([np.cos((np.pi/np.e**2)*y), 0, np.sin((np.pi/np.e**2)*y)],
         [-np.sin((np.pi/np.e**2)*y), 0, np.cos((np.pi/np.e**2)*y)],
         [0, 1, 0]
        ), np.float64
    )
    rot_z = np.array(
        ([np.sin((np.pi/np.e)*z), np.cos((np.pi/np.e)*z), 0],
         [np.cos((np.pi/np.e)*z), -np.sin((np.pi/np.e)*z), 0],
         [0, 0, 1]
        ), np.float64
    )
    matrix = np.matmul(matrix, rot_x)
    matrix = np.matmul(matrix, rot_y)
    matrix = np.matmul(matrix, rot_z)
    return matrix
 
# --- VECTOR NORMALIZATION -------------------------------------------------
 
def length(vector):
    return np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
 
def normalize_vector(face):
    """ Calculate the normal vector between -1 and 1 for a flat surface """
    norm = np.cross((face[0,0] - face[1,1]), (face[1,0] - face[0,1]))
    return norm / length(norm)
 
# --- ORTHOGRAPHIC PROJECTION ----------------------------------------------
 
def project(rows):
    """
    Go through the array and draw rectangles.
    There is probably a more efficent way to do this.
    """
    for i in range(len(rows) -1):
        for j in range(len(rows[i])-1):
            face = rows[i:i+2, j:j+2]
            normal = normalize_vector(face)
            light_angle = (np.dot(normal, light))
            if (light_angle < 0):
                light_angle = 0
            fill(
                light_angle - 0.3,
                light_angle + 0.28,
                light_angle + 0.4,
                0.975
            )
            # Draw only forward facing facets.
            if (np.dot(view, normal) > 0):
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
                # Save z with path for later z sorting.
                path.z = face[1,-2,2]
 
# --- ROTATION SLIDERS -----------------------------------------------------
 
var("rot_x", NUMBER,    1.00, -np.pi, np.pi)
var("rot_y", NUMBER, np.pi/4, -np.pi, np.pi)
var("rot_z", NUMBER,   -np.e, -np.pi, np.pi)
 
# --- LIGHTING SLIDERS -----------------------------------------------------
 
var("light_x", NUMBER, 0.50, -1.0, 1.0)
var("light_y", NUMBER, -0.60, -1.0, 1.0)
var("light_z", NUMBER, -0.25, -1.0, 1.0)

light = np.array([light_x, light_y, light_z], np.float64)
 
# --- FACET CULLING --------------------------------------------------------
# Draw only forward facing facets.
view = np.array([0, 0, 2], np.float64)
 
sphere = np.fromfunction(matrix, (n+1, m+1, 3))
sphere = rotate_matrix(sphere, rot_x, rot_y, rot_z)
project(sphere)

def depthsort( a, b ):
    if a.z > b.z:
        return 1
    elif a.z < b.z:
        return -1
    return 0

# z-sort to avoid problems with overlapping surfaces:
sorted_grobs = list(canvas)
#sorted_grobs.sort(lambda p1, p2: cmp(p1.z, p2.z))
sortlistfunction( sorted_grobs, depthsort )
canvas._grobs = sorted_grobs
