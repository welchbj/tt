/**
 * Python C-extension for interfacing with the PicoSAT library.
 * See LICENSE file in tt/_clibs/picosat directory for PicoSAT license.
 *
 * All credit for PicoSAT functionaltiy goes to the library's authors. Thank
 * you for your hard work.
 *
 * Patterns in this C-extension are based off of the work done in the PyEDA and
 * Pycosat libraries. Thank you for leading the way.
 */

#include <Python.h>

#include "picosat.h"
#include "tt_cpython_compat.h"


//
// PicoSAT memory manager config methods
//

inline static void *
_cpython_malloc(void * mmgr, size_t bytes)
{
    return PyMem_Malloc(bytes);
}

inline static void *
_cpython_realloc(void * mmgr, void * ptr, size_t old, size_t new)
{
    return PyMem_Realloc(ptr, new);
}

inline static void
_cpython_free(void * mmgr, void * ptr, size_t bytes)
{
    PyMem_Free(ptr);
}


//
// PicoSAT interfacing methods
//

/**
 * Ensures the validity of Python args object, inits PicoSAT object, and adds
 * PicoSAT clauses + assumptions.
 *
 * Returns NULL if an error occurs.
 */
static PicoSAT *
_tt_setup_picosat(PyObject * args, PyObject * kwds)
{
    static char * keywords[] = {"clauses", "assumptions", NULL};

    PicoSAT * picosat;
    PyObject * clauses;             // List[List[int]]
    PyObject * assumptions = NULL;  // List[int]

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O", keywords,
                                     &clauses, &assumptions))
        return NULL;

    picosat = picosat_minit(NULL,
                            _cpython_malloc, _cpython_realloc, _cpython_free);

    if (_tt_add_picosat_assumptions(picosat, assumptions) < 0)
    {
        picosat_reset(picosat);
        return NULL;
    }

    if (_tt_add_picosat_clauses(picosat, clauses) < 0)
    {
        picosat_reset(picosat);
        return NULL;
    }

    // all good
    return picosat;
}


//
// PicoSAT functionality methods
//

/**
 * Add a clause to a PicoSAT instance. A clause is a list of non-zero ints.
 *
 * Returns 0 on success, -1 on error.
 */
static int
_tt_add_picosat_clause(PicoSAT * picosat, PyObject * clause)
{
    if (!PyList_Check(clause))
    {
        PyErr_SetString(PyExc_TypeError, "clause must be a list of non-zero ints");
        return -1;
    }

    if (PyList_Size(clause) < 1)
    {
        PyErr_SetString(PyExc_ValueError, "clause must be non-empty");
        return -1;
    }

    PyObject * clause_iterator;  // clause is an iterable of ints
    PyObject * literal;          // each literal is an int

    clause_iterator = PyObject_GetIter(clause);
    if (clause_iterator == NULL)
        return -1;

    while ((literal = PyIter_Next(clause_iterator)) != NULL)
    {
        if (!IS_INT(literal))
        {
            Py_DECREF(literal);
            Py_DECREF(clause_iterator);
            PyErr_SetString(PyExc_TypeError, "All literals expected to be ints");
            return -1;
        }

        int l = PyLong_AsLong(literal);
        Py_DECREF(literal);

        if (l == 0)
        {
            Py_DECREF(clause_iterator);
            PyErr_SetString(PyExc_ValueError, "All literals must be non-zero");
            return -1;
        }

        picosat_add(picosat, l);
    }

    Py_DECREF(clause_iterator);
    if (PyErr_Occurred())
        return -1;

    picosat_add(picosat, 0);  // terminate clause
    return 0;
}

/**
 * Add clauses to a PicoSAT instance. Clauses are a Python iterator of
 * iterators of non-zero ints.
 *
 * Returns 0 on success, -1 on error.
 */
static int
_tt_add_picosat_clauses(PicoSAT * picosat, PyObject * clauses)
{
    if (!PyList_Check(clauses))
    {
        PyErr_SetString(PyExc_TypeError, "clauses must be a list of lists of non-zero ints");
        return -1;
    }

    if (PyList_Size(clauses) < 1)
    {
        PyErr_SetString(PyExc_ValueError, "clause musts be non-empty");
        return -1;
    }

    PyObject * clauses_iterator;  // clauses is iterable of iterable of ints
    PyObject * clause;            // each clause is iterable of ints

    clauses_iterator = PyObject_GetIter(clauses);
    if (clauses_iterator == NULL)
        return -1;

    while ((clause = PyIter_Next(clauses_iterator)) != NULL)
    {
        if (_tt_add_picosat_clause(picosat, clause) < 0)
        {
            Py_DECREF(clause);
            Py_DECREF(clauses_iterator);
            return -1;
        }

        Py_DECREF(clause);
    }

    Py_DECREF(clauses_iterator);
    if (PyErr_Occurred())
        return -1;

    return 0;
}

/**
 * Add assumptions to a PicoSAT instance. assumptions is an iterable of
 * non-zero ints.
 *
 * Returns 0 on success, -1 on error.
 */
static int
_tt_add_picosat_assumptions(PicoSAT * picosat, PyObject * assumptions)
{
    if (assumptions == NULL || assumptions == Py_None)
    {
        // no assumptions provided
        return 0;
    }

    if (!PyList_Check(assumptions))
    {
        PyErr_SetString(PyExc_TypeError, "assumptions must be a list of non-zero ints");
        return -1;
    }

    if (PyList_Size(assumptions) < 1)
    {
        PyErr_SetString(PyExc_ValueError, "assumptions must be non-empty");
        return -1;
    }

    PyObject * assumptions_iterator;
    PyObject * assumption;

    assumptions_iterator = PyObject_GetIter(assumptions);

    if (assumptions_iterator == NULL)
        return -1;

    while ((assumption = PyIter_Next(assumptions_iterator)) != 0)
    {
        if (!IS_INT(assumption))
        {
            PyErr_SetString(PyExc_TypeError, "All assumption literals expected to be ints");
            Py_DECREF(assumption);
            Py_DECREF(assumptions_iterator);
            return -1;
        }

        int a = PyLong_AsLong(assumption);
        Py_DECREF(assumption);

        if (a == 0)
        {
            PyErr_SetString(PyExc_ValueError, "All assumption literals must be non-zero");
            Py_DECREF(assumptions_iterator);
            return -1;
        }

        picosat_assume(picosat, a);
    }

    Py_DECREF(assumptions_iterator);

    if (PyErr_Occurred())
        return -1;

    return 0;
}

/**
 * Retrieve the solution from a PicoSAT instance into a Python list of ints.
 */
static PyObject *
_tt_picosat_sol_to_py_list(PicoSAT * picosat)
{
    PyObject * list;
    PyObject * literal;
    int num_vars, i, v;

    num_vars = picosat_variables(picosat);
    list = PyList_New((Py_ssize_t)num_vars);
    if (list == NULL)
    {
        picosat_reset(picosat);
        return NULL;
    }

    for (i = 1; i <= num_vars; ++i)
    {
        v = picosat_deref(picosat, i);
        literal = PyInt_FromLong((long) (v * i));
        if (PyList_SetItem(list, (Py_ssize_t)(i - 1), literal) < 0)
        {
            Py_DECREF(literal);
            Py_DECREF(list);
            picosat_reset(picosat);
            return NULL;
        }
    }

    return list;
}


//
// Module-exposed methods
//

/**
 * Module-exposed method for finding a single, satisfiable solution.
 *
 *  Returns:
 *    List[int] of literals if a solution was found.
 *    None, if no solution was found.
 *
 *  Raises:
 *    TypeError:  If non-integer are passed as literals.
 *    ValueError: If integers equal to zero are passed as literals.
 */
static PyObject *
sat_one(PyObject * self, PyObject * args, PyObject * kwds)
{
    PicoSAT * picosat;
    int picosat_result;

    picosat = _tt_setup_picosat(args, kwds);
    if (picosat == NULL)
        return NULL;

    // run PicoSAT w/o the GIL
    Py_BEGIN_ALLOW_THREADS
    picosat_result = picosat_sat(picosat, -1);
    Py_END_ALLOW_THREADS

    switch (picosat_result)
    {
        case PICOSAT_SATISFIABLE:
            PyObject * ret = _tt_picosat_sol_to_py_list(picosat);
            picosat_reset(picosat);
            return ret;

        case PICOSAT_UNSATISFIABLE:
            picosat_reset(picosat);
            Py_RETURN_NONE;

        case PICOSAT_UNKNOWN:
            picosat_reset(picosat);
            PyErr_SetString(PyExc_RuntimeError, "PicoSAT unable to solve");
            return NULL;

        default:
            picosat_reset(picosat);
            PyErr_SetString(PyExc_RuntimeError, "PicoSAT returned unexpected value");
            return NULL;
    }
}

// TODO: sat_all


//
// Setting up the module
//

static PyMethodDef
PicosatMethods[] = {
    // TODO: add sat_all
    {"sat_one", (PyCFunction)sat_one, METH_VARARGS | METH_KEYWORDS, ""},
    {NULL, NULL, 0, NULL}  /* sentinel */
};

#ifdef TT_IS_PYTHON_3
//
// Python 3 module boilerplate
//
static PyModuleDef moduleDef = {
    PyModuleDef_HEAD_INIT, "picosat", "", -1, PicosatMethods
};

PyMODINIT_FUNC
PyInit_picosat(void)
{
    PyObject * m;
    m = PyModule_Create(&moduleDef);
#else
//
// Python 2 module boilerplate
//
PyMODINIT_FUNC
initpicosat(void)
{
    PyObject * m;
    m = Py_InitModule3("picosat", PicosatMethods, "");
#endif
//
// Module definition main body
//
    if (m == NULL)
        return NULL;

    if(PyModule_AddIntConstant(m, "VERSION", 965) < 0)
        return NULL;

    return m;
}
