"""
Main module
"""

from ctypes import POINTER, c_uint8, c_uint64
import os
import itertools
import functools
import operator as op
import joblib
from Bio import SeqIO
import numpy as np
from yack.count import ranklib
import yack.count.count as countlib


class SparseArray:
    def __init__(self, cols, data):
        self.cols = cols
        self.data = data

    def normalize(self):
        self.data /= np.sum(self.data)


def count_kmers(input_file, kmer_size):
    sample = Sample(input_file)
    kmer_refs = np.concatenate(list(_get_kmer_ranks(seq, kmer_size) for seq in sample.iter_seqs()))
    
    counted = countlib.count_kmers(kmer_refs)
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


_alphabet = dict(zip([char for char in ('A', 'C', 'G', 'T')], itertools.count()))


def _isvalid(sequence):
    return functools.reduce(op.and_, [char in _alphabet for char in sequence])


def _validate(sequence):
    return sequence if _isvalid(sequence) else []


def _transform(sequence):
    return np.array([_alphabet[char] for char in sequence], dtype=np.uint8)


def _parse_sample_name(sample_file):
    with open(sample_file, 'r') as f:
        line = ' '
        while line[0] != '>':
            line = f.readline()
        
        return line.split('_')[0].split('>')[1].strip()
        


class SampleFile:
    def __init__(self, path: str):
        self._path = path
        self._format = os.path.splitext(os.path.basename(path))[1][1:]
        if self._format == 'fna':
            self._format = 'fasta'

    @property
    def path(self):
        return self._path

    @property
    def file_format(self):
        return self._format


class Sample:
    def __init__(self, input_file):
        self._name = _parse_sample_name(input_file)
        self._sample_file = SampleFile(input_file)
        self._kmer_index = None

    def iter_seqs(self):
        seqs_records = SeqIO.parse(open(self._sample_file.path), self._sample_file.file_format)
        for seq_rec in seqs_records:
            yield _transform(_validate(seq_rec.seq))