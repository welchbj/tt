/**
 * Helpers for maintaining CPython 2/3 extension compatibility.
 *
 * Ideas here are mainly from PycoSAT library compat efforts (https://github.com/ContinuumIO/pycosat).
 */

#include <Python.h>


#if PY_MAJOR_VERSION >= 3
    #define TT_IS_PYTHON_3
#endif

#ifdef TT_IS_PYTHON_3
    #define PyInt_FromLong  PyLong_FromLong
    #define IS_INT(x)  (PyLong_Check(x))
#else
    #define IS_INT(x)  (PyInt_Check(x) || PyLong_Check(x))
#endif
