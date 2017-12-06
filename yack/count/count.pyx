# distutils: language=c++

import numpy as np
cimport numpy as np
DTYPE = np.uint64
ctypedef np.uint64_t DTYPE_t


def count_kmers(np.ndarray[DTYPE_t, ndim=1] ranks):
    cdef KmerCounter kmer_counter
    cdef DTYPE_t length = ranks.shape[0]

    for i in range(length):
        kmer_counter.count(ranks[i])

    cdef pair[vector[np.uint64_t], vector[np.uint64_t]] values = kmer_counter.values()
    return values
    