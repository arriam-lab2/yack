# distutils: language=c++

from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libc.stdint cimport uint64_t

def count_kmers(seqs, size_t kmer_size, size_t num_bins):
    cdef vector[string] vector_seqs = seqs
    cdef cpp_result = count(vector_seqs, kmer_size, num_bins)
    return [p for p in cpp_result]
    