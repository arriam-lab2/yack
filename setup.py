"""
Setuptools script
"""

import os
import sys
import numpy
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

os.environ["CC"] = "g++"
os.environ["CFLAGS"] = '-O3 -Wall -std=c++17'


extensions = cythonize(["yack/ext/count.pyx", ])

setup(
    name='yack',
    version='0.1',
    description = 'Yet another k-mer counter',
    author = 'Nikolay Romashchenko',
    author_email = 'nikolay.romashchenko@gmail.com',
    url = 'https://github.com/arriam-lab2/yack',
    download_url = 'https://github.com/arriam-lab2/yack/archive/v0.1.tar.gz',
    keywords = ['k-mer', 'counting'],

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'biopython==1.70',
        'click==6.7',
        'cython==0.27.3',
        'joblib==0.11',
        'numpy==1.13.3',
    ],
    entry_points='''
        [console_scripts]
        yack=yack.cli:cli
    ''',

    ext_modules = extensions,
    include_dirs=[numpy.get_include(), "third-party"]
)
