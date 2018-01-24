#include <stdlib.h>
#include <Python.h>

// Karsten Wolf 2018-01-17

// atkinson dither

static int arrayindex(int x, int y, int w){
	return (y * w + x);
}

static PyObject *
atkinson(PyObject *self, PyObject *args) {
	/*
	 * 
	 */
	// params
    int w, h, treshhold;

	// iterators
    int x, y;

	// calculated array index
    int idx;

    float *errorBuffer, errdiv;
    const unsigned char *sourceImage;
    unsigned char *resultImage;
    int count, newval, errval;
    PyObject *result;

    if (!PyArg_ParseTuple(args, "s#iii", &sourceImage, &count, &w, &h, &treshhold)) {
    	return (NULL);
	}

	// create the buffers
	resultImage = (unsigned char *)malloc( count );
	errorBuffer = (float *)malloc( count*sizeof(float) );


	// init & check the buffers
	memcpy( (void *)resultImage, (const void *)sourceImage, count);
	memset( errorBuffer, 0, count*sizeof(float));

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
				errdiv = errval / 8.0;
				resultImage[idx] = 255;
			} else {
				errval = newval;
				errdiv = errval / 8.0;
				resultImage[idx] = 0;
			}
			
			// distribute the error
			// atkinson dithering divides by eight but distributes only 6/8
			if ( x+1 < w ) {
				// x+1 ,y
				idx = arrayindex(x+1, y, w);
				errorBuffer[idx] += errdiv;
				if ( x+2 < w ) {
					// x+2 ,y
					idx = arrayindex(x+2, y, w);
					errorBuffer[idx] += errdiv;
				}
			}

			if ( y+1 < h ) {
				// x ,y+1
				idx = arrayindex(x, y+1, w);
				errorBuffer[idx] += errdiv;
				if (x-1 >= 0) {
					// x-1, y+1
					idx = arrayindex(x-1, y+1, w);
					errorBuffer[idx] += errdiv;
				}
				if ( y+2 < h ) {
					// x, y+2
					idx = arrayindex(x, y+2, w);
					errorBuffer[idx] += errdiv;
				}
				if (x+1 < w) {
					// x+1, y+1
					idx = arrayindex(x+1, y+1, w);
					errorBuffer[idx] += errdiv;
				}
			}
		}
	}

	// build the return value
	result = Py_BuildValue("s#", resultImage, count);
	free(errorBuffer);
	free(resultImage);
    return result;
}


static PyMethodDef atkinsondither_methods[]={ 
    { "atkinson", atkinson, METH_VARARGS },
    { NULL, NULL }
};


PyMODINIT_FUNC initatkinsondither(void){ 
    PyObject *m;
    m = Py_InitModule("atkinsondither", atkinsondither_methods);
}


int main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);
    Py_Initialize();
    initatkinsondither();
    return 0;
}
