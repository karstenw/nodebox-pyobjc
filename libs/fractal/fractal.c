#include <stdlib.h>
#include <stdio.h>
#include <complex.h>

#define PY_SSIZE_T_CLEAN
#include <Python.h>

// Karsten Wolf 2020-06-21

// mandelbrot calculations

#if PY_MAJOR_VERSION >= 3
  #define MOD_ERROR_VAL NULL
  #define MOD_SUCCESS_VAL(val) val
  #define MOD_INIT(name) PyMODINIT_FUNC PyInit_##name(void)
  #define MOD_DEF(ob, name, doc, methods) \
          static struct PyModuleDef moduledef = { \
            PyModuleDef_HEAD_INIT, name, doc, -1, methods, }; \
          ob = PyModule_Create(&moduledef);
#else
  #define MOD_ERROR_VAL
  #define MOD_SUCCESS_VAL(val)
  #define MOD_INIT(name) void init##name(void)
  #define MOD_DEF(ob, name, doc, methods) \
    ob = Py_InitModule3(name, methods, doc);
#endif
#if PY_MAJOR_VERSION >= 3
  #define IN_FORMAT "y#iiiddddddd"
  #define OUT_FORMAT "y#"
#else
  #define IN_FORMAT "s#iiiddddddd"
  #define OUT_FORMAT "s#"
#endif

static PyObject *
fractalimage(PyObject *self, PyObject *args) {
    /*
     * The errors are mine. kw 2020-06
     */

    int x, y;

    // params
    int clutsize, w, h, iterations;
    double x1, y1, dx, dy, nreal, nimag, limit;
    // double creal, cimag, 
    unsigned char *pixels;
    const unsigned char *clut;


    int count = 0;
    
    // int dbg = 0;

    PyObject *result;

    // s# -> 2vars; d double; 
    if (!PyArg_ParseTuple(args, IN_FORMAT,
                          &clut, &clutsize,
                          &w, &h, &iterations, 
                          &x1, &y1, &dx, &dy, &nreal, &nimag, &limit )) {
        return (NULL);
    }

    count = w * h * 4;

    // if (dbg)
    //     printf("count: %d\n", count);

    // create the buffers
    pixels = (unsigned char *)malloc( count );
    memset( pixels, 0, count);

    if (!pixels) {
        PyErr_NoMemory();
        return NULL;
    }

    double scalex = 1.0 / (double)w * dx;
    double scaley = 1.0 / (double)h * dy;

    // iterate over all pixels (x,y)
    for (y=0; y < h; y++) {
        for (x=0; x < w; x++) {
            int v = 0, iter;

            double xc = x1 + (double)x * scalex;
            double yc = y1 + (double)y * scaley;
            
            double complex z = xc + yc * I;
            double complex c = nreal + nimag * I;


            // calc pixel value v
            for (iter=0; iter < iterations; iter++) {
                if (cabs(c) <= limit) {
                    c = c*c + z;
                } else {
                    v = iter;
                    break;
                }
            }
            // copy clut values
            int idx = v * 4;
            int o = (y * w + x) * 4;
            for (iter=0; iter < 4; iter++) {
                if ((o+iter < count) && (idx+iter < clutsize))
                    pixels[o+iter] = clut[idx+iter];
                /*
                else if (dbg) {
                    printf("BOUNDS crossed\n");
                    if (o+iter < count)
                        printf("o+iter %d  count %d\n", o+iter, count);
                    if (idx+iter < clutsize)
                        printf("idx+iter %d clutsize %d\n", o+iter, clutsize);
                
                }
                */
            }
        }
    }

    // build the return value
    result = Py_BuildValue(OUT_FORMAT, pixels, count);
    free(pixels);
    return result;
}


static PyMethodDef fractal_methods[]={ 
    { "fractalimage", fractalimage, METH_VARARGS },
    { NULL, NULL }
};


MOD_INIT(fractal) { 
    PyObject *m;
    //m = Py_InitModule("fractal", fractal_methods);
    MOD_DEF(m, "fractal", "A mandelbrot renderer.", fractal_methods)
#if PY_MAJOR_VERSION >= 3
    return( m );
#endif
}

int main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);
    Py_Initialize();
#if PY_MAJOR_VERSION >= 3
    PyInit_fractal();
#else
    initfractal();
#endif
    return 0;
}

