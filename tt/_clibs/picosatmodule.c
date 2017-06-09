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
#include "_compat/tt_cpython_compat.h"

//
// Struct definition for solution iteration
//

typedef struct {
    PyObject_HEAD
    PicoSAT * picosat;
    PyObject * assumptions;
    signed char _temp_mem;
} soliter_obj;


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
    PyObject * clause_iterator;  // clause is an iterable of ints
    PyObject * literal;          // each literal is an int
    int l;

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

        l = PyLong_AsLong(literal);
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
    PyObject * clauses_iterator;  // clauses is iterable of iterable of ints
    PyObject * clause;            // each clause is iterable of ints

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
 * Assert validity of Python list of int assumptions.
 *
 * Returns 0 on success, -1 on error.
 */
static int
_tt_assert_picosat_assumptions(PyObject * assumptions)
{
    PyObject * assumptions_iterator;
    PyObject * assumption;
    int a;

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

        a = PyLong_AsLong(assumption);
        Py_DECREF(assumption);

        if (a == 0)
        {
            PyErr_SetString(PyExc_ValueError, "All assumption literals must be non-zero");
            Py_DECREF(assumptions_iterator);
            return -1;
        }
    }

    Py_DECREF(assumptions_iterator);

    if (PyErr_Occurred())
        return -1;

    return 0;
}


/**
 * Add assumptions to a PicoSAT instance. assumptions is an iterable of
 * non-zero ints. Expects assumptions to be of valid form.
 *
 * Returns 0 on success, -1 on error.
 */
static int
_tt_add_picosat_assumptions(PicoSAT * picosat, PyObject * assumptions)
{
    PyObject * assumptions_iterator;
    PyObject * assumption;
    int a;

    if (assumptions == NULL || assumptions == Py_None)
    {
        // no assumptions provided
        return 0;
    }

    assumptions_iterator = PyObject_GetIter(assumptions);

    if (assumptions_iterator == NULL)
        return -1;

    while ((assumption = PyIter_Next(assumptions_iterator)) != 0)
    {
        a = PyLong_AsLong(assumption);
        Py_DECREF(assumption);
        picosat_assume(picosat, a);
    }

    Py_DECREF(assumptions_iterator);

    if (PyErr_Occurred())
        return -1;

    return 0;
}

/**
 * Ensures the validity of Python args object, inits PicoSAT object, and adds
 * PicoSAT clauses + assumptions.
 *
 * Returns NULL if an error occurs.
 */
static PicoSAT *
_tt_setup_picosat(PyObject * args, PyObject * kwds, soliter_obj * iter)
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

    if (_tt_assert_picosat_assumptions(assumptions) < 0)
    {
        picosat_reset(picosat);
        return NULL;
    }

    if (_tt_add_picosat_assumptions(picosat, assumptions) < 0)
    {
        picosat_reset(picosat);
        return NULL;
    }

    if (iter != NULL)
    {
        iter->assumptions = assumptions;
        Py_INCREF(assumptions);
    }

    if (_tt_add_picosat_clauses(picosat, clauses) < 0)
    {
        picosat_reset(picosat);
        return NULL;
    }

    // all good
    return picosat;
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

/**
 * Block a solution from being returned again in the passed PicoSAT instance.
 *
 * Returns 0 on success, -1 on error.
 */
static int
_tt_block_sol(PicoSAT * picosat, signed char * mem)
{
    int num_vars, i;

    num_vars = picosat_variables(picosat);
    if (mem == NULL)
    {
        mem = PyMem_Malloc(num_vars + 1);
        if (mem == NULL)
        {
            PyErr_NoMemory();
            return -1;
        }
    }

    for (i = 1; i <= num_vars; ++i)
        mem[i] = (picosat_deref(picosat, i) > 0) ? 1 : -1;
    for (i = 1; i <= num_vars; ++i)
        picosat_add(picosat, (mem[i] < 0) ? i : -i);
    picosat_add(picosat, 0);

    return 0;
}


//
// New type definition for iterating sat_all solutions
//

static PyTypeObject SolIter_Type;

static PyObject * _tt_soliter_next(soliter_obj * iter)
{
    PyObject * ret = NULL;
    int picosat_result;

    assert(PyObject_TypeCheck(iter, &SolIter_Type));

    // run PicoSAT w/o the GIL
    Py_BEGIN_ALLOW_THREADS
    picosat_result = picosat_sat(iter->picosat, -1);
    Py_END_ALLOW_THREADS

    switch (picosat_result)
    {
        case PICOSAT_SATISFIABLE:
            ret = _tt_picosat_sol_to_py_list(iter->picosat);
            if (_tt_block_sol(iter->picosat, iter->_temp_mem) < 0)
                return NULL;
            if (_tt_add_picosat_assumptions(iter->picosat, iter->assumptions) < 0)
                return NULL;
            break;
        case PICOSAT_UNSATISFIABLE:
        case PICOSAT_UNKNOWN:
            // exhausted all solutions, so stop iteration
            break;
        default:
            picosat_reset(iter->picosat);
            PyErr_SetString(PyExc_RuntimeError, "PicoSAT returned unexpected value");
            return NULL;
    }

    return ret;
}

static void _tt_soliter_dealloc(soliter_obj * iter)
{
    PyObject_GC_UnTrack(iter);
    Py_DECREF(iter->assumptions);
    if (iter->_temp_mem)
        PyMem_Free(iter->_temp_mem);
    picosat_reset(iter->picosat);
    PyObject_GC_Del(iter);
}

static int _tt_soliter_traverse(soliter_obj * iter, visitproc visit, void * arg)
{
    return 0;
}

static PyTypeObject SolIter_Type = {

#ifdef TT_IS_PYTHON_3
    PyVarObject_HEAD_INIT(NULL, 0)
#else
    PyObject_HEAD_INIT(NULL)
    0,                                        // ob_size
#endif
    "soliter",                                // tp_name
    sizeof(soliter_obj),                      // tp_basicsize
    0,                                        // tp_itemsize
    // methods
    (destructor) _tt_soliter_dealloc,         // tp_dealloc
    0,                                        // tp_print
    0,                                        // tp_getattr
    0,                                        // tp_setattr
    0,                                        // tp_compare
    0,                                        // tp_repr
    0,                                        // tp_as_number
    0,                                        // tp_as_sequence
    0,                                        // tp_as_mapping
    0,                                        // tp_hash
    0,                                        // tp_call
    0,                                        // tp_str
    PyObject_GenericGetAttr,                  // tp_getattro
    0,                                        // tp_setattro
    0,                                        // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,  // tp_flags
    0,                                        // tp_doc
    (traverseproc) _tt_soliter_traverse,      // tp_traverse
    0,                                        // tp_clear
    0,                                        // tp_richcompare
    0,                                        // tp_weaklistoffset
    PyObject_SelfIter,                        // tp_iter
    (iternextfunc) _tt_soliter_next,          // tp_iternext
    0                                         // tp_methods

};


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
    PyObject * ret;
    int picosat_result;

    picosat = _tt_setup_picosat(args, kwds, NULL);
    if (picosat == NULL)
        return NULL;

    // run PicoSAT w/o the GIL
    Py_BEGIN_ALLOW_THREADS
    picosat_result = picosat_sat(picosat, -1);
    Py_END_ALLOW_THREADS

    switch (picosat_result)
    {
        case PICOSAT_SATISFIABLE:
            ret = _tt_picosat_sol_to_py_list(picosat);
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

/**
 * Return an instance of the custom solution iterator type.
 *
 * Accepts the same arguments as the `sat_one` method.
 */
static PyObject *
sat_all(PyObject * self, PyObject * args, PyObject * kwds)
{
    soliter_obj * iter;

    iter = PyObject_GC_New(soliter_obj, &SolIter_Type);
    if (iter == NULL)
        return NULL;

    iter->picosat = _tt_setup_picosat(args, kwds, iter);
    if (iter->picosat == NULL)
        return NULL;

    iter->_temp_mem = NULL;
    PyObject_GC_Track(iter);

    return (PyObject *)iter;
}


//
// Setting up the module
//

static PyMethodDef
PicosatMethods[] = {
    {"sat_one", (PyCFunction)sat_one, METH_VARARGS | METH_KEYWORDS, ""},
    {"sat_all", (PyCFunction)sat_all, METH_VARARGS | METH_KEYWORDS, ""},
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

    if (m == NULL)
        return NULL;

    if(PyModule_AddIntConstant(m, "VERSION", 965) < 0)
        return NULL;

    return m;
}
#else
//
// Python 2 module boilerplate
//
PyMODINIT_FUNC
initpicosat(void)
{
    PyObject * m;
    m = Py_InitModule3("picosat", PicosatMethods, "");
    PyModule_AddIntConstant(m, "VERSION", 965);
}
#endif
