"""
Main module
"""

import os
import joblib
import numpy as np
from Bio import SeqIO
from typing import List, Dict
import yack.count as countlib


KMER_VALIDATE_MESSAGE = 'k-mer size must be an integer between 1 and 32'
DEFAULT_NUM_BINS = 1000
DEFAULT_DELIMITER = "_"


class SparseArray:
    """
    Sparse array data structure
    """
    def __init__(self, cols, data):
        self.cols = cols
        self.data = data

    def normalize(self):
        self.data /= np.sum(self.data)

    def __len__(self):
        return len(self.cols)


def validate_kmer_size(kmer_size: str) -> int:
    """
    Transform and validate input k-mer size
    :param kmer_size: Input k-mer size as string
    :return: K-mer size as int
    """
    value = int(kmer_size)
    assert 1 <= value <= 32
    return value


def _parse_format(input_file: str) -> str:
    """
    Parse a file name to determine an input format
    :param input_file: Input file name
    :return: Canonical name of input format (fasta/fastq)
    """
    extensions = {"fastq": "fastq",
                  "fq": "fastq",
                  "fasta": "fasta",
                  "fna": "fasta",
                  "ffn": "fasta",
                  "faa": "fasta",
                  "frn": "fasta"}

    splitext = os.path.splitext(input_file)
    if len(splitext) < 2 or (splitext[1][1:].lower() not in extensions):
        raise ValueError("Unknown extension: {}".format(splitext[1][1:]))
    return extensions[splitext[1][1:]]


def count_seqs(sequences: List[str], kmer_size: int, num_bins: int = DEFAULT_NUM_BINS) -> SparseArray:
    """
    Count k-mers of input sequences
    :param sequences: List of input sequences
    :param kmer_size: Size of k-mer
    :param num_bins: Optional number of bins to split k-mers between while counting
    :return: Sparse array containing counted k-mers encoded as uint64_t numbers
    """
    counted = countlib.count_kmers([s.encode('ascii') for s in sequences], kmer_size, num_bins)
    counted = list(zip(*counted))
    cols = np.array(counted[0], dtype=np.uint64)
    data = np.array(counted[1], dtype=np.float)
    return SparseArray(cols, data)


def count_sample(input_file: str,
                 kmer_size: int,
                 num_bins: int = DEFAULT_NUM_BINS) -> SparseArray:
    """
    Count k-mers of sequences from input_file.
    :param input_file: Input file name
    :param kmer_size: Size of k-mer
    :param num_bins: Optional number of bins to split k-mers between while counting
    :return: Sparse array containing counted k-mers encoded as uint64_t numbers
    """
    input_format = _parse_format(input_file)
    sequences = [str(record.seq) for record in SeqIO.parse(input_file, input_format)]
    return count_seqs(sequences, kmer_size, num_bins=num_bins)


def count_multiple_samples(input_file: str,
                           output_dir: str,
                           kmer_size: int,
                           delimiter=DEFAULT_DELIMITER,
                           num_bins=DEFAULT_NUM_BINS) -> Dict[str, SparseArray]:
    """
    Count k-mers of several samples located in the same input_file.
    :param input_file: Input file name
    :param output_dir: Output directory
    :param kmer_size: Size of k-mer
    :param delimiter: Pattern for splitting a sequence record description to parse a sample name
    :param num_bins: Optional number of bins to split k-mers between while counting
    :return: List of sparse arrays containing counted k-mers encoded as uint64_t numbers
    """
    sample_files = _split_sequences(input_file, output_dir, delimiter=delimiter)
    return dict((sample_file, count_sample(sample_file, kmer_size, num_bins=num_bins))
                for sample_file in sample_files)


def dump(sparse_array: SparseArray, output_filename: str) -> None:
    """
    Dump a sparse array on the disk
    :param sparse_array: Input sparse array
    :param output_filename: Output file name
    :return: None
    """
    joblib.dump(sparse_array, output_filename)


def load(input_filename: str) -> SparseArray:
    """
    Load a sparse array from the disk
    :param input_filename: Input file name
    :return: Loaded sparse array
    """
    return joblib.load(input_filename)


def hist(sparse_array: SparseArray) -> None:
    """
    Pretty-print of a sparse array data
    :param sparse_array: Input sparse array
    :return: None
    """
    values = list(zip(sparse_array.cols, sparse_array.data))
    
    print("\n".join(
        "{}: {:d}".format(k, int(v)) for k, v in values)
    )


def _split_sequences(input_file: str, output_dir: str, delimiter: str = "_") -> List[str]:
    """
    Split sequences of several samples from input_file to several files
    :param input_file: Input file name
    :param output_dir: Output directory name
    :param delimiter: Pattern for splitting a sequence record description to parse a sample name
    :return: List of output file names
    """
    os.makedirs(output_dir, exist_ok=True)
    
    output_files = set()
    input_format = _parse_format(input_file)
    current_sample = ""
    with open(input_file, 'r') as infile:
        for seq_record in SeqIO.parse(infile, input_format):
            sample_name = seq_record.id.split(" ")[0]
            sample_name = sample_name.split(delimiter)[0]
            
            if current_sample != sample_name:
                output_filename = os.path.join(output_dir, sample_name + "." + input_format)
                output_files.add(output_filename)
                output = open(output_filename, "a")

            assert output
            SeqIO.write(seq_record, output, input_format)

    return list(output_files)
