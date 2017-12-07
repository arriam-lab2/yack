"""
Setuptools script
"""

import os
import sys
import numpy
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

os.environ["CC"] = "g++"
os.environ["CFLAGS"] = '-O3 -Wall -std=c++11'


extensions = cythonize(["yack/count/count.pyx", ]) + [
        Extension("yack.count.rank", ["yack/count/rank.cpp"], language='c++') 
]
print(extensions)
setup(
    name='yack',
    version='0.1',
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
