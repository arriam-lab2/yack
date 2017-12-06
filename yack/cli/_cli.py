"""
Command line interface module
"""

import os
import click
from yack.core import count_kmers, dump, hist


DUMP = 'dump'
HIST = 'hist'
OUTPUT_FORMATS = [DUMP, HIST]
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group()
def cli():
    """
    Yack is yet another k-mer counter.
    """
    pass


def validate_kmer_size(ctx, param, value):
    try:
        kmer_size = int(value)
        assert 1 <= kmer_size <= 32
        return kmer_size
    except (ValueError, AssertionError):
        raise click.BadParameter('k-mer size must be an integer between 1 and 32')


@cli.command()
@click.argument("input_file", type=click.Path(exists=True), required=True)
@click.option("--kmer_size", "-k", callback=validate_kmer_size, type=int, default=15)
@click.option('--dump', 'output', flag_value=DUMP, default=True)
@click.option('--hist', 'output', flag_value=HIST)
@click.option('--output_filename', '-o', required=False, default='')
def count(input_file, kmer_size, output, output_filename):
    """
    Count k-mers of size k in the INPUT_FILE.
    """
    sparse_array = count_kmers(input_file, kmer_size)

    if not output_filename:
        basename = os.path.basename(input_file)
        output_filename = os.path.join(os.path.dirname(input_file), os.path.splitext(basename)[0] + ".yack")
        
    if output == DUMP:
        dump(sparse_array, output_filename)
        print("Output:", output_filename)
    elif output == HIST:
        hist(sparse_array)
    else:
        raise ValueError("Unknown output format")

