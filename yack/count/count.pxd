# distutils: language=c++

from libc.stdint cimport uint64_t
from libcpp.vector cimport vector
from libcpp.utility cimport pair

import numpy as np
cimport numpy as np


cdef extern from "count.h":
    cdef cppclass KmerCounter:
        void count(uint64_t kmer_ref)
        size_t size()

        pair[vector[np.uint64_t], vector[np.uint64_t]] values()