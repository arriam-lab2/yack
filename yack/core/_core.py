"""
Main module
"""

import joblib
import numpy as np
import yack.ext.count as countlib


KMER_VALIDATE_MESSAGE = 'k-mer size must be an integer between 1 and 32'
DEFAULT_NUM_BINS = 1000


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


def count_kmers(sequences, kmer_size, num_bins=1000):
    counted = countlib.count_kmers([s.encode('ascii') for s in sequences], kmer_size, num_bins)
    counted = list(zip(*counted))
    cols = np.array(counted[0], dtype=np.uint64)
    data = np.array(counted[1], dtype=np.float)
    return SparseArray(cols, data)


def dump(sparse_array, output_filename):
    joblib.dump(sparse_array, output_filename)

def load(input_filename):
    return joblib.load(input_filename)

def hist(sparse_array):
    values = list(zip(sparse_array.cols, sparse_array.data))
    
    print("\n".join(
        "{}: {:d}".format(k, int(v)) for k, v in values)
    )
