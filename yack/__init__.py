from .core import count_kmers as _count_kmers,\
                  hist as _hist


def count_kmers(sequences, kmer_size, num_bins=core.DEFAULT_NUM_BINS):
    return _count_kmers(sequences, kmer_size, num_bins)


def hist(sparse_array):
    return _hist(sparse_array)