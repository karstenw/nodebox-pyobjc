size(910, 950)
import numpy as np

(0, 0, WIDTH, HEIGHT)
stroke(.2, .2, .3, .35)
translate(510, 410)
background(None)
nofill()
strokewidth(.1)

# n defines how many vertices we find: the number will be n^2
n = 200

def rotate(matrix, x, y, z):
	rotY = np.array(([np.cos(y), 0, np.sin(y)],[0, 1, 0],[-np.sin(y), 0, np.cos(y)]))
	rotX = np.array(([1, 0, 0],[0, np.cos(x), -np.sin(x)],[0, np.sin(x), np.cos(x)]))
	rotZ = np.array(([np.cos(z), -np.sin(z), 0],[np.sin(z), np.cos(z), 0],[0, 0, 1]))
	matrix = np.dot(matrix, rotX)
	matrix = np.dot(matrix, rotY)
	matrix = np.dot(matrix, rotZ)
	return matrix

u, v = np.mgrid[ -13.2:13.2:n*1j,
                 -37.4:37.4:n*1j]
b = 0.4
r = 1 - b**2;

from math import sqrt
w = sqrt(r);

denom = b*((w * np.cosh(b*u))**2 + (b * np.sin(w*v))**2)

x = -u + (2*r*np.cosh(b*u) * np.sinh(b*u)) / denom
y = (2 * w * np.cosh(b*u) * (-(w * np.cos(v) * np.cos(w*v)) - np.sin(v) * np.sin(w*v))) / denom
z = (2 * w * np.cosh(b*u) * (-(w * np.sin(v) * np.cos(w*v)) + np.cos(v) * np.sin(w*v)))/denom
x.shape = (n**2,)
y.shape = (n**2,)
z.shape = (n**2,)
rows = np.column_stack((x,y, z))
rows = rotate(rows, 0, np.pi/5, 1.2) * 60
n = n-1
#create face array (4 x n)
faces = np.sum(np.mgrid[0:n:1, 0:n**2:n], 0).reshape(n**2,1)+ np.array([0, n+1, n+2, 1])
#draw quads
for f in faces:
	beginpath(rows[f[0]][0], rows[f[0]][1])
	lineto(rows[f[1]][0], rows[f[1]][1])
	lineto(rows[f[2]][0], rows[f[2]][1])
	lineto(rows[f[3]][0], rows[f[3]][1])
	endpath()
