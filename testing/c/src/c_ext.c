#define PY_SSIZE_T_CLEAN
#define Py_LIMITED_API
#include <Python.h>

static PyObject*
say_hello(PyObject* self, PyObject* args)
{
  return PyUnicode_FromString("Hello, world!");
}

static PyObject* 
add(PyObject* self, PyObject* args) 
{
    long a, b;

    if (!PyArg_ParseTuple(args, "ll", &a, &b))
            return NULL;
    return PyLong_FromLong(a+b);
}

static struct PyMethodDef methods[] = {
  {"say_hello", (PyCFunction)say_hello, METH_NOARGS},
  {"add", (PyCFunction)add, METH_VARARGS},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef c_ext_module = {
  PyModuleDef_HEAD_INIT,
  "c_ext",
  NULL,
  -1,
  methods
};

PyMODINIT_FUNC 
PyInit_c_ext(void) {
    return PyModule_Create(&c_ext_module);
}

