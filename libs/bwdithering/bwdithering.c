

#include <stdlib.h>

#define PY_SSIZE_T_CLEAN
#include <Python.h>

// Karsten Wolf 2018-01-17

// black & white dither

// type for the errorBuffer. Possible: int, short, float
#define ERRBUFTYPE float
#define UNIT 1.0

enum {
    atkinsondither=1,
    floydsteinbergdither,
    jarvisjudiceninkedithering,
    stuckidithering,
    burkesdithering,
    sierra1dithering,
    sierra2dithering,
    sierra3dithering,
    zzsentinel
} dithertypes;

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
  #define IN_FORMAT "y#iiii"
  #define OUT_FORMAT "y#"
#else
  #define IN_FORMAT "s#iiii"
  #define OUT_FORMAT "s#"
#endif
static int arrayindex(int x, int y, int w){
    return (y * w + x);
}


static void distributeError( int x, int y,
                             int w, int h,
                             int type,
                             ERRBUFTYPE errval,
                             unsigned char destImage[], ERRBUFTYPE errorBuffer[] ) {
    /*
     * Distribute the error to neighbouring pixels.
     *
     * The distributions have been taken from
     * 
     * http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
     *
     *
     * The errors are mine. kw 2018-01
     */

    ERRBUFTYPE errdiv1, errdiv2, errdiv3, errdiv4;
    int idx;

    if (type < 0) {
        type = 0;
    }
    if  (type >= zzsentinel) {
        type = zzsentinel-1;
    }

    switch (type){
        case atkinsondither:
            // distribute the error
            // atkinson dithering divides by eight but distributes only 6/8
            errdiv1 = errval / (UNIT * 8);
            if ( x+1 < w ) {
                // x+1 ,y
                idx = arrayindex(x+1, y, w);
                errorBuffer[idx] += errdiv1;
                if ( x+2 < w ) {
                    // x+2 ,y
                    idx = arrayindex(x+2, y, w);
                    errorBuffer[idx] += errdiv1;
                }
            }

            if ( y+1 < h ) {
                // x ,y+1
                idx = arrayindex(x, y+1, w);
                errorBuffer[idx] += errdiv1;
                if (x-1 >= 0) {
                    // x-1, y+1
                    idx = arrayindex(x-1, y+1, w);
                    errorBuffer[idx] += errdiv1;
                }
                if ( y+2 < h ) {
                    // x, y+2
                    idx = arrayindex(x, y+2, w);
                    errorBuffer[idx] += errdiv1;
                }
                if (x+1 < w) {
                    // x+1, y+1
                    idx = arrayindex(x+1, y+1, w);
                    errorBuffer[idx] += errdiv1;
                }
            }
            break;

        case floydsteinbergdither:
            errdiv1 = errval / (UNIT * 16) * 7;
            errdiv2 = errval / (UNIT * 16) * 3;
            errdiv3 = errval / (UNIT * 16) * 5;
            errdiv4 = errval / (UNIT * 16) * 1;

            if ( x+1 < w ) {
                // x+1 ,y
                idx = arrayindex(x+1, y, w);
                // 7/16
                errorBuffer[idx] += errdiv1;
                if ( y+1 < h ) {
                    // x+1 ,y+1
                    idx = arrayindex(x+1, y+1, w);
                    // 1/16
                    errorBuffer[idx] += errdiv4;
                }
            }
            if ( y+1 < h ) {
                // x ,y+1
                idx = arrayindex(x, y+1, w);
                // 5/16
                errorBuffer[idx] += errdiv3;
                
                if (x > 0) {
                    // x-1 ,y+1
                    idx = arrayindex(x-1, y+1, w);
                    // 3/16
                    errorBuffer[idx] += errdiv2;
                }
            }

            break;

        case jarvisjudiceninkedithering:
            errdiv1 = errval / (UNIT * 48) * 7;
            errdiv2 = errval / (UNIT * 48) * 5;
            errdiv3 = errval / (UNIT * 48) * 3;
            errdiv4 = errval / (UNIT * 48) * 1;

            if ( x+1 < w ) {
                // x+1 ,y
                idx = arrayindex(x+1, y, w);
                // 7/48
                errorBuffer[idx] += errdiv1;
                if ( y+1 < h ) {
                    // x+1 ,y+1
                    idx = arrayindex(x+1, y+1, w);
                    // 5/48
                    errorBuffer[idx] += errdiv2;
                }
                if ( y+2 < h ) {
                    // x+1 ,y+2
                    idx = arrayindex(x+1, y+2, w);
                    // 3/48
                    errorBuffer[idx] += errdiv3;
                }

                if ( x+2 < w ) {
                    // x+2 ,y
                    idx = arrayindex(x+2, y, w);
                    // 5/48
                    errorBuffer[idx] += errdiv2;
                    if ( y+1 < h ) {
                        // x+2 ,y+1
                        idx = arrayindex(x+2, y+1, w);
                        // 3/48
                        errorBuffer[idx] += errdiv3;
                    }
                    if ( y+2 < h ) {
                        // x+2 ,y+2
                        idx = arrayindex(x+2, y+2, w);
                        // 1/48
                        errorBuffer[idx] += errdiv4;
                    }
                }
            }

            if (y+1 < h) {
                // x, y+1
                idx = arrayindex(x, y+1, w);
                // 7/48
                errorBuffer[idx] += errdiv1;
            }
            if (y+2 < h) {
                // x, y+2
                idx = arrayindex(x, y+2, w);
                // 5/48
                errorBuffer[idx] += errdiv2;
            }

            if ( x-1 > 0 ) {
                if (y+1 < h) {
                    // x-1, y+1
                    idx = arrayindex(x-1, y+1, w);
                    // 5/48
                    errorBuffer[idx] += errdiv2;
                }
                if (y+2 < h) {
                    // x-1, y+2
                    idx = arrayindex(x-1, y+2, w);
                    // 3/48
                    errorBuffer[idx] += errdiv3;
                }
            }
            if ( x-2 > 0 ) {
                if (y+1 < h) {
                    // x-2, y+1
                    idx = arrayindex(x-2, y+1, w);
                    // 3/48
                    errorBuffer[idx] += errdiv3;
                }
                if (y+2 < h) {
                    // x-2, y+2
                    idx = arrayindex(x-2, y+2, w);
                    // 1/48
                    errorBuffer[idx] += errdiv4;
                }
            }
            break;

        case stuckidithering:
            errdiv1 = errval / (UNIT * 42) * 8;
            errdiv2 = errval / (UNIT * 42) * 4;
            errdiv3 = errval / (UNIT * 42) * 2;
            errdiv4 = errval / (UNIT * 42) * 1;
            if ( x+1 < w ) {
                // x+1 ,y
                idx = arrayindex(x+1, y, w);
                // 8/42
                errorBuffer[idx] += errdiv1;
                if ( y+1 < h ) {
                    // x+1, y+1
                    idx = arrayindex(x+1, y+1, w);
                    // 4/42
                    errorBuffer[idx] += errdiv2;
                }
                if ( y+2 < h ) {
                    // x+1, y+2
                    idx = arrayindex(x+1, y+2, w);
                    // 2/42
                    errorBuffer[idx] += errdiv3;
                }
                if ( x+2 < w ) {
                    // x+2 ,y
                    idx = arrayindex(x+2, y, w);
                    // 4/42
                    errorBuffer[idx] += errdiv2;
                    if ( y+1 < h ) {
                        // x+2, y+1
                        idx = arrayindex(x+2, y+1, w);
                        // 2/42
                        errorBuffer[idx] += errdiv3;
                    }
                    if ( y+2 < h ) {
                        // x+2, y+2
                        idx = arrayindex(x+2, y+2, w);
                        // 1/42
                        errorBuffer[idx] += errdiv4;
                    }
                }
            }
            if (y+1 < h) {
                if (x-2 > 0) {
                    idx = arrayindex(x-2, y+1, w);
                    // 2/42
                    errorBuffer[idx] += errdiv3;
                }
                if (x-1 > 0) {
                    idx = arrayindex(x-1, y+1, w);
                    // 4/42
                    errorBuffer[idx] += errdiv2;
                }
                idx = arrayindex(x, y+1, w);
                // 8/42
                errorBuffer[idx] += errdiv1;
            }
            if (y+2 < h) {
                if (x-2 > 0) {
                    idx = arrayindex(x-2, y+2, w);
                    // 1/42
                    errorBuffer[idx] += errdiv4;
                }
                if (x-1 > 0) {
                    idx = arrayindex(x-1, y+2, w);
                    // 2/42
                    errorBuffer[idx] += errdiv2;
                }
                idx = arrayindex(x, y+2, w);
                // 4/42
                errorBuffer[idx] += errdiv2;
            }
            break;

        case burkesdithering:
            errdiv1 = errval / (UNIT * 32) * 8;
            errdiv2 = errval / (UNIT * 32) * 4;
            errdiv3 = errval / (UNIT * 32) * 2;

            if ( x+1 < w ) {
                // x+1 ,y
                idx = arrayindex(x+1, y, w);
                // 8/32
                errorBuffer[idx] += errdiv1;
                if ( y+1 < h ) {
                    // x+1, y+1
                    idx = arrayindex(x+1, y+1, w);
                    // 4/32
                    errorBuffer[idx] += errdiv2;
                }
                if ( x+2 < w ) {
                    // x+2 ,y
                    idx = arrayindex(x+2, y, w);
                    // 4/32
                    errorBuffer[idx] += errdiv2;
                    if ( y+1 < h ) {
                        // x+2, y+1
                        idx = arrayindex(x+2, y+1, w);
                        // 2/32
                        errorBuffer[idx] += errdiv3;
                    }
                }
            }
            if (y+1 < h) {
                if (x-2 > 0) {
                    idx = arrayindex(x-2, y+1, w);
                    // 2/32
                    errorBuffer[idx] += errdiv3;
                }
                if (x-1 > 0) {
                    idx = arrayindex(x-1, y+1, w);
                    // 4/32
                    errorBuffer[idx] += errdiv2;
                }
                idx = arrayindex(x, y+1, w);
                // 8/32
                errorBuffer[idx] += errdiv1;
            }
            break;

        case sierra1dithering:
            errdiv1 = errval / (UNIT * 32) * 5;
            errdiv2 = errval / (UNIT * 32) * 4;
            errdiv3 = errval / (UNIT * 32) * 3;
            errdiv4 = errval / (UNIT * 32) * 2;
            if ( x+1 < w ) {
                // x+1 ,y
                idx = arrayindex(x+1, y, w);
                // 5/32
                errorBuffer[idx] += errdiv1;
                if ( y+1 < h ) {
                    // x+1, y+1
                    idx = arrayindex(x+1, y+1, w);
                    // 4/32
                    errorBuffer[idx] += errdiv2;
                }
                if ( y+2 < h ) {
                    // x+1, y+2
                    idx = arrayindex(x+1, y+2, w);
                    // 2/32
                    errorBuffer[idx] += errdiv4;
                }
                if ( x+2 < w ) {
                    // x+2 ,y
                    idx = arrayindex(x+2, y, w);
                    // 3/16
                    errorBuffer[idx] += errdiv3;
                    if ( y+1 < h ) {
                        // x+2, y+1
                        idx = arrayindex(x+2, y+1, w);
                        // 2/16
                        errorBuffer[idx] += errdiv4;
                    }
                }
            }
            if (y+1 < h) {
                if (x-2 > 0) {
                    idx = arrayindex(x-2, y+1, w);
                    // 2/32
                    errorBuffer[idx] += errdiv4;
                }
                if (x-1 > 0) {
                    idx = arrayindex(x-1, y+1, w);
                    // 4/32
                    errorBuffer[idx] += errdiv2;
                }
                idx = arrayindex(x, y+1, w);
                // 5/32
                errorBuffer[idx] += errdiv1;
            }

            if (y+2 < h) {
                if (x-1 > 0) {
                    idx = arrayindex(x-1, y+2, w);
                    // 2/32
                    errorBuffer[idx] += errdiv4;
                }
                if (x+1 < w) {
                    idx = arrayindex(x+1, y+2, w);
                    // 2/32
                    errorBuffer[idx] += errdiv4;
                }
                idx = arrayindex(x, y+2, w);
                // 3/32
                errorBuffer[idx] += errdiv3;
            }


            break;

        case sierra2dithering:
            errdiv1 = errval / (UNIT * 16) * 4;
            errdiv2 = errval / (UNIT * 16) * 3;
            errdiv3 = errval / (UNIT * 16) * 2;
            errdiv4 = errval / (UNIT * 16) * 1;
            if ( x+1 < w ) {
                // x+1 ,y
                idx = arrayindex(x+1, y, w);
                // 4/16
                errorBuffer[idx] += errdiv1;
                if ( y+1 < h ) {
                    // x+1, y+1
                    idx = arrayindex(x+1, y+1, w);
                    // 2/16
                    errorBuffer[idx] += errdiv2;
                }
                if ( x+2 < w ) {
                    // x+2 ,y
                    idx = arrayindex(x+2, y, w);
                    // 3/16
                    errorBuffer[idx] += errdiv2;
                    if ( y+1 < h ) {
                        // x+2, y+1
                        idx = arrayindex(x+2, y+1, w);
                        // 1/16
                        errorBuffer[idx] += errdiv4;
                    }
                }
            }
            if (y+1 < h) {
                if (x-2 > 0) {
                    idx = arrayindex(x-2, y+1, w);
                    // 1/16
                    errorBuffer[idx] += errdiv4;
                }
                if (x-1 > 0) {
                    idx = arrayindex(x-1, y+1, w);
                    // 2/16
                    errorBuffer[idx] += errdiv3;
                }
                idx = arrayindex(x, y+1, w);
                // 3/16
                errorBuffer[idx] += errdiv2;
            }
            break;

        case sierra3dithering:
            errdiv1 = errval / (UNIT * 4) * 2;
            errdiv2 = errval / (UNIT * 4) * 1;

            if ( x+1 < w ) {
                // x+1 ,y
                idx = arrayindex(x+1, y, w);
                // 2/4
                errorBuffer[idx] += errdiv1;
            }
            if ( y+1 < h ) {
                // x, y+1
                idx = arrayindex(x, y+1, w);
                // 1/4
                errorBuffer[idx] += errdiv2;
                if ( x-1 > 0 ) {
                    // x-1, y+1
                    idx = arrayindex(x-1, y+1, w);
                    // 1/4
                    errorBuffer[idx] += errdiv2;
                }
            }
            break;
    }
}


static PyObject *
dither(PyObject *self, PyObject *args) {
    /*
     * 
     */
    // params
    int w, h, type, treshhold;

    // iterators
    int x, y;

    // calculated array index
    int idx;
    int count;

    ERRBUFTYPE *errorBuffer, errdiv, newval, errval;
    const unsigned char *sourceImage;
    unsigned char *resultImage;
    // unsigned char *sourceImage, *resultImage;
    PyObject *result;

    if (!PyArg_ParseTuple(args, IN_FORMAT, &sourceImage, &count, &w, &h, &type, &treshhold)) {
        return (NULL);
    }
    
    if (!count) {
        printf("count %d\n" , count);
        printf("w %d\n" , w);
        printf("h %d\n" , h);
        printf("type %d\n" , type);
        printf("treshhold %d\n" , treshhold);
    }

    // create the buffers
    resultImage = (unsigned char *)malloc( count );
    errorBuffer = (ERRBUFTYPE *)malloc( count*sizeof(ERRBUFTYPE));

    // init & check the buffers
    memcpy( (void *)resultImage, (const void *)sourceImage, count);
    memset( errorBuffer, 0, count*sizeof(ERRBUFTYPE));

    if (!resultImage) {
        PyErr_NoMemory();
        return NULL;
    }

    if (!errorBuffer) {
        PyErr_NoMemory();
        return NULL;
    }

    // iterate over all pixels (x,y)
    for (y = 0; y < h; y++) {
        for (x = 0; x < w; x++) {
            // calc array index for image and error buffers
            idx = arrayindex(x, y, w);
            newval = errorBuffer[idx] + resultImage[idx];
            
            // set pixel value
            if (newval >= treshhold) {
                errval = newval - 255;
                errdiv = errval / 8;
                resultImage[idx] = 255;
            } else {
                errval = newval;
                errdiv = errval / 8;
                resultImage[idx] = 0;
            }

            // cut short if nothing to add			
            if (errdiv == 0)
                continue;
            distributeError( x, y, w, h, type, errval, resultImage, errorBuffer);
        }
    }

    // build the return value
    result = Py_BuildValue(OUT_FORMAT, resultImage, count);
    free(errorBuffer);
    free(resultImage);
    return result;
}


static PyMethodDef bwdither_methods[]={ 
    { "dither", dither, METH_VARARGS },
    { NULL, NULL }
};


MOD_INIT(bwdithering) { 
    PyObject *m;
    // m = Py_InitModule("bwdithering", bwdither_methods);
    MOD_DEF(m, "bwdithering", "A bw dithering extension.", bwdither_methods)
#if PY_MAJOR_VERSION >= 3
    return(MOD_SUCCESS_VAL(m));
#else
	MOD_SUCCESS_VAL(m)
#endif
}

int main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);
    Py_Initialize();
#if PY_MAJOR_VERSION >= 3
    PyInit_bwdithering();
#else
    initbwdithering();
#endif
    return 0;
}


