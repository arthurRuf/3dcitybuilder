from cpython.ref cimport PyObject

cdef extern from "capnp/helpers/capabilityHelper.h":
    cppclass PythonInterfaceDynamicImpl:
        PythonInterfaceDynamicImpl(PyObject *)

cdef extern from "capnp/helpers/capabilityHelper.h":
    void reraise_kj_exception()
    cdef cppclass PyRefCounter:
        PyRefCounter(PyObject *)

cdef extern from "capnp/helpers/rpcHelper.h":
    cdef cppclass PyRestorer:
        PyRestorer(PyObject *)
    cdef cppclass ErrorHandler:
        pass

cdef extern from "capnp/helpers/asyncHelper.h":
    cdef cppclass PyEventPort:
        PyEventPort(PyObject *)
