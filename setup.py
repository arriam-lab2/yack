#!/usr/bin/env python

"""
Setuptools script
"""

import os
import sys
import numpy
from setuptools import setup, find_packages, Extension

AUTO = 'auto'

# Set this to True to enable building extensions using Cython.
# Set it to False to build extensions from the C++ file (that was previously created using Cython).
# Set it to AUTO to build with Cython if available, otherwise from the C++ file.
USE_CYTHON = False


if USE_CYTHON:
    try:
        from Cython.Distutils import build_ext
    except ImportError:
        if USE_CYTHON == AUTO:
            USE_CYTHON = False
        else:
            raise


cmdclass = {}
ext_modules = []

if USE_CYTHON:
    ext_modules += [
        Extension("yack.count", [ "yack/count.pyx" ], language="c++"),
    ]
    cmdclass.update({ 'build_ext': build_ext })
else:
    ext_modules += [
        Extension("yack.count", [ "yack/count.cpp" ]),
    ]

os.environ["CC"] = "g++"
os.environ["CFLAGS"] = '-O3 -Wall -std=c++17'

setup(
    name='yack',
    version='0.1.2',
    description = 'Yet another k-mer counter',
    license='MIT',
    author = 'Nikolai Romashchenko',
    author_email = 'nikolay.romashchenko@gmail.com',
    url = 'https://github.com/arriam-lab2/yack',
    keywords = ['k-mer', 'counting'],

    cmdclass = cmdclass,
    ext_modules = ext_modules,
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'biopython==1.70',
        'click==6.7',
        'cython==0.27.3',
        'joblib==0.11',
        'numpy==1.13.3',
    ],
    entry_points = '''
        [console_scripts]
        yack=yack.cli:cli
    ''',

    include_dirs = [numpy.get_include(), "third-party", "yack"]
)
