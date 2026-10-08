

__all__ = ['rotate_matrix', 'length', 'normalize_vector', 'project']

import numpy as np

from mmparametriclib import length, normalize_vector

'''
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
                    np.where(index==2,  z(u,v), 1)
                    )
                 )
'''

# --- MATRIX ROTATION ------------------------------------------------------

def rotate_matrix(matrix, x, y, z):
    rot_x = np.array(
        ([1, 0, 0],
         [0, np.cos(x), -np.sin(x)],
         [0, np.sin(x),  np.cos(x)]
        ), np.float64
    )
    rot_y = np.array(
        ([np.cos(y), 0, np.sin(y)],
         [0, 1, 0],
         [-np.sin(y), 0, np.cos(y)]
        ), np.float64
    )
    rot_z = np.array(
        ([np.cos(z),  -np.sin(z), 0],
         [np.sin(z), np.cos(z), 0],
         [0, 0, 1]
        ), np.float64
    )
    matrix = np.matmul(matrix, rot_x)
    matrix = np.matmul(matrix, rot_y)
    matrix = np.matmul(matrix, rot_z)
    return matrix

# --- ORTHOGRAPHIC PROJECTION ----------------------------------------------

def project(rows, light, view):
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

            # Coloring scheme based on t between -1.0 and 1.0.
            _ctx.colormode( "hsb" ) # TODO: Why is HSB not in _ctx
            t = float(i) / len(rows) * 2 - 1
            _ctx.fill(
                0.6 + 0.2 * abs(t**2),
                0.8 - 0.4 * light_angle,
                0.3 + 0.7 * light_angle,
                0.75
            )
            
            # Draw only forward facing facets.
            if (np.dot(view, normal) > 0):
                _ctx.beginpath(
                    face[0, 0, 0],
                    face[0, 0, 1]
                )
                _ctx.lineto(
                    face[1, 0, 0],
                    face[1, 0, 1]
                )
                _ctx.lineto(
                    face[1, 1, 0],
                    face[1, 1, 1]
                )
                _ctx.lineto(
                    face[0, 1, 0],
                    face[0, 1, 1]
                )
                path = _ctx.endpath()
                # Save z with path for later z sorting.
                path.z = face[1,0,2]


