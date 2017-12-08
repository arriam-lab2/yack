from .core import count_kmers as _count_kmers


def count_kmers(sequences, kmer_size):
    return _count_kmers(sequences, kmer_size)
