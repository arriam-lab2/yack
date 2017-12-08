# distutils: language=c++


from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.utility cimport pair
from libc.stdint cimport uint64_t

import numpy as np
cimport numpy as np


cdef extern from "count.h":
    cdef vector[pair[uint64_t, uint64_t]] count(vector[string], size_t, size_t)