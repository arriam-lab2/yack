"""
Command line interface module
"""

import click

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


def _validate_kmer_size(ctx, param, value):
    from yack import core
    try:
        return core.validate_kmer_size(value)
    except (ValueError, AssertionError):
        raise click.BadParameter(core.KMER_VALIDATE_MESSAGE)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True), required=True)
@click.option('--output_dir', '-o', required=False, default='.')
@click.option("--kmer_size", "-k", callback=_validate_kmer_size, type=int, default=15)
@click.option('--dump', 'output', flag_value=DUMP, default=True)
@click.option('--hist', 'output', flag_value=HIST)
@click.option('--multiple', is_flag=True)
@click.option('--delimiter', type=str, default="_")
@click.option('--num-jobs', type=int, default=1)
def count(input_file: str, output_dir: str, kmer_size: int,
          output: str, multiple: bool, delimiter: str, num_jobs: int):
    """
    Count k-mers of size k in the INPUT_FILE (fasta or fastq)
    """

    import os
    from yack import core

    counted_samples = core.count_multiple_samples(kmer_size, input_file, output_dir, delimiter=delimiter, num_jobs=num_jobs) \
        if multiple else {input_file: core.count_sample(kmer_size, input_file)}

    for sample_file, sparse_array in counted_samples.items():
        print("Input file: ", sample_file)
        basename = os.path.basename(sample_file)
        output_filename = os.path.join(output_dir, os.path.splitext(basename)[0] + ".yack")

        if output == DUMP:
            core.dump(sparse_array, output_filename)
            print("Output file:", output_filename)
        elif output == HIST:
            core.hist(sparse_array)
        else:
            raise ValueError("Unknown option {}".format(output))
