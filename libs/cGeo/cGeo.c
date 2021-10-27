#include <Python.h>
#include <math.h>

// FAST INVERSE SQRT
// Chris Lomont, http://www.math.purdue.edu/~clomont/Math/Papers/2003/InvSqrt.pdf

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
float _fast_inverse_sqrt(float x) { 
    float xhalf = 0.5f*x; 
    int i = *(int*)&x;
    i = 0x5f3759df - (i>>1);
    x = *(float*)&i;
    x = x*(1.5f-xhalf*x*x);
    return x; 
}
static PyObject *
fast_inverse_sqrt(PyObject *self, PyObject *args) {
    double x;   
    if (!PyArg_ParseTuple(args, "d", &x))
        return NULL;
    x = _fast_inverse_sqrt(x);
    return Py_BuildValue("d", x);
}

// ANGLE
void _angle(double x0, double y0, double x1, double y1, double *a) {
    *a = atan2(y1-y0, x1-x0) / M_PI * 180;
}
static PyObject *
angle(PyObject *self, PyObject *args) {
    double x0, y0, x1, y1, a;    
    if (!PyArg_ParseTuple(args, "dddd", &x0, &y0, &x1, &y1))
        return NULL;
    _angle(x0, y0, x1, y1, &a);
    return Py_BuildValue("d", a);
}

// DISTANCE
void _distance(double x0, double y0, double x1, double y1, double *d) {
    // this is not much faster but inaccurate
    // *d = 1.0 / _fast_inverse_sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0));
    // *d = sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0));
    double dx = x1-x0, dy = y1-y0;
    *d = sqrt(dx*dx + dy*dy);
}
static PyObject *
distance(PyObject *self, PyObject *args) {
    double x0, y0, x1, y1, d;   
    if (!PyArg_ParseTuple(args, "dddd", &x0, &y0, &x1, &y1))
        return NULL;
    _distance(x0, y0, x1, y1, &d);
    return Py_BuildValue("d", d);
}

// COORDINATES
void _coordinates(double x0, double y0, double d, double a, double *x1, double *y1) {
    *x1 = x0 + cos(a/180*M_PI) * d;
    *y1 = y0 + sin(a/180*M_PI) * d;
}
static PyObject *
coordinates(PyObject *self, PyObject *args) {
    double x0, y0, d, a, x1, y1;   
    if (!PyArg_ParseTuple(args, "dddd", &x0, &y0, &d, &a))
        return NULL;
    _coordinates(x0, y0, d, a, &x1, &y1);
    return Py_BuildValue("dd", x1, y1);
}

static PyMethodDef geometry_methods[]={ 
    { "fast_inverse_sqrt", fast_inverse_sqrt, METH_VARARGS },
    { "angle", angle, METH_VARARGS }, 
    { "distance", distance, METH_VARARGS }, 
    { "coordinates", coordinates, METH_VARARGS },  
    { NULL, NULL }
};


MOD_INIT(cGeo) { 
    PyObject *m;
    // m = Py_InitModule("cGeo", geometry_methods);
    MOD_DEF(m, "cGeo", "angle, distance and coordinates.", geometry_methods)
#if PY_MAJOR_VERSION >= 3
    return( m );
#endif
}

int main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);
    Py_Initialize();
#if PY_MAJOR_VERSION >= 3
    PyInit_cGeo();
#else
    initcGeo();
#endif
    return 0;
}
