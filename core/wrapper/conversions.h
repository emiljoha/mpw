#ifndef __CONVERSION_H_INCLUDED__
#define __CONVERSION_H_INCLUDED__

#include <boost/python.hpp>
#include <Python.h>

using namespace std;
using namespace boost::python;
struct MPMasterKey_to_python_string
{
  static PyObject* convert(MPMasterKey key)
      {
        object memoryView(
	    handle<>(
	        PyMemoryView_FromMemory((char *)key,
					 (Py_ssize_t)MPMasterKeySize,
					 PyBUF_READ)));
	return boost::python::incref(memoryView.ptr());
      }
};

#endif
