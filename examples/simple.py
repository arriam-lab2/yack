"""
A simple example of using yack
"""

import os
import click
import yack
from Bio import SeqIO


@click.command()
@click.argument('input_file', type=click.Path(exists=True), required=True)
def main(input_file):
    input_format = os.path.splitext(input_file)[1][1:]
    sequences = [str(record.seq) for record in SeqIO.parse(input_file, input_format)]
    k = 15
    print(yack.count_kmers(sequences, k))

    
if __name__ == "__main__":
    main()