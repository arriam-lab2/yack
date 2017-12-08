"""
Main module
"""

from ctypes import POINTER, c_uint8, c_uint64
import itertools
import joblib
import numpy as np
import yack.count.count as countlib


KMER_VALIDATE_MESSAGE = 'k-mer size must be an integer between 1 and 32'
UNKNOWN_SYMBOL = 'N'
ALPHABET_LIST = ('A', 'C', 'G', 'T')
ALPHABET = dict(zip([char for char in ALPHABET_LIST], itertools.count()))


class SparseArray:
    def __init__(self, cols, data):
        self.cols = cols
        self.data = data

    def normalize(self):
        self.data /= np.sum(self.data)

    def __len__(self):
        return len(self.cols)


def validate_kmer_size(kmer_size):
    value = int(kmer_size)
    assert 1 <= value <= 32
    return value

def _transform(sequence):
    sequence = "".join([c if c in ALPHABET else UNKNOWN_SYMBOL for c in sequence])
    subseqs = sequence.split(UNKNOWN_SYMBOL)
    return [np.array([ALPHABET[char] for char in subseq.upper()], dtype=np.uint8) 
            for subseq in subseqs]

def count_kmers(sequences, kmer_size):
    counted = countlib.count_kmers([s.encode('ascii') for s in sequences], kmer_size, 1000)
    counted = list(zip(*counted))
    cols = np.array(counted[0], dtype=np.uint64)
    data = np.array(counted[1], dtype=np.float)
    return SparseArray(cols, data)


def _get_kmer_ranks(sequence, kmer_size):
    if sequence.size < kmer_size:
        return np.array([],  dtype=np.uint64)

    ranks = np.zeros(len(sequence) - kmer_size + 1, dtype=np.uint64)
    seq_pointer = sequence.ctypes.data_as(POINTER(c_uint8))
    ranks_pointer = ranks.ctypes.data_as(POINTER(c_uint64))
    ranklib.count_kmer_ranks(seq_pointer, ranks_pointer, len(sequence), kmer_size)
    return ranks


def dump(sparse_array, output_filename):
    joblib.dump(sparse_array, output_filename)

def hist(sparse_array):
    values = sorted(list(zip(sparse_array.cols, sparse_array.data)))
    
    print("\n".join(
        "{}: {:d}".format(k, int(v)) for k, v in values)
    )
