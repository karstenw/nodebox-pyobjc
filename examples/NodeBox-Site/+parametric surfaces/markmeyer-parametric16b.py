size(550, 550)
background(0)
nofill()
stroke(0.6, 0.6, 0.7, 0.35)
strokewidth(0.5)

translate(WIDTH/2, HEIGHT/2)

import numpy as np

# n defines how many vertices we find: the number will be n^2.
# Large values of n can take a while to render!
n = 50

# --- FUNNEL EQUATION -------------------------------------------------------

# Define parametric equations for each axis.
# Although we define an z coordinate,
# it is only used in transformations and shading; 
# it is not used in the drawing 
# (although it could be if you wanted to add perspective).
r = 300

def x(u, v):
    return r * np.cos(v)**2 * np.cos(u)**3

def y(u, v):
    return r * np.sin(v-1)**2 * np.cos(u)**3

def z(u, v):
    return r * np.sin(u)**2

def fit_to_domain(u, v):
    u = -np.pi + u * np.pi / n
    v = -np.pi + v * np.pi / n
    return u, v

# from Numeric import *

def matrix(u, v, index):
    u, v = fit_to_domain(u, v)
    return np.where(index==0, x(u, v),
                 np.where(index==1, y(u,v),
                    np.where(index==2,  z(u,v), 1)
                    )
                 )

# --- MATRIX ROTATION ------------------------------------------------------

def rotate_matrix(matrix, x, y, z):
    rot_x = np.array(
        ([1, 0, 0],
         [0, np.cos(x), -np.sin(x)],
         [0, np.sin(x),  np.cos(x)]
        ), np.float64
    )
    rot_y = np.array(
        ([ np.cos(y), 0, np.sin(y)],
         [0, 1, 0],
         [-np.sin(y), 0, np.cos(y)]
        ), np.float64
    )
    rot_z = np.array(
        ([ np.cos(z),  -np.sin(z), 0],
         [ np.sin(z),   np.cos(z), 0],
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
    # norm = cross_product((face[0,0] - face[1,1]), (face[1,0] - face[0,1]))
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
            light_angle = ( np.dot(normal, light) )
            if (light_angle < 0):
                light_angle = 0

            fill(
                light_angle + 0.02,
                light_angle + 0.04,
                light_angle + 0.08,
                1.0
            )
            # Draw only forward facing facets.
            #if ( np.dot(view, normal) > 0):
            if True:
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
                path.z = face[1,0,2]

# --- ROTATION SLIDERS -----------------------------------------------------

var("rot_x", NUMBER,  0,         -np.pi, np.pi)
var("rot_y", NUMBER, -np.pi*3/4, -np.pi, np.pi)
var("rot_z", NUMBER,  np.pi,     -np.pi, np.pi)

# --- LIGHTING SLIDERS -----------------------------------------------------

var("light_x", NUMBER,  0.50, -1.0, 1.0)
var("light_y", NUMBER, -0.60, -1.0, 1.0)
var("light_z", NUMBER, -0.25, -1.0, 1.0)

light = np.array([light_x, light_y, light_z], np.float64)

# --- FACET CULLING --------------------------------------------------------
# Draw only forward facing facets.
view = np.array([0, 0, 1], np.float64)

sphere = np.fromfunction(matrix, (n+1, n+1, 3))
sphere = rotate_matrix(sphere, rot_x, rot_y, rot_z)
project(sphere)

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
