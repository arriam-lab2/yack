"""
Setuptools script
"""

import os
import numpy
from distutils.core import Extension
from setuptools import setup, find_packages
from Cython.Distutils import build_ext

from Cython.Build import cythonize


os.environ["CC"] = "g++"
os.environ["CFLAGS"] = '-O3 -Wall -std=c++11'

extensions = [
    Extension("yack.count.count", 
              ["yack/count/count.pyx"], 
              include_dirs=[numpy.get_include(), "third-party"]),
]

setup(
    name='yack',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy==1.13.3',
        'click==6.7',
        'cython==0.27.3'
    ],
    entry_points='''
        [console_scripts]
        yack=yack.cli:cli
    ''',

    #cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize(extensions) + [
        Extension("yack.count.rank", ["yack/count/rank.cpp"], language='c++')
    ]
    #    
    

    #ext_modules=cythonize("yack/count/count.pyx",
    #                      language="c++"),
    #include_dirs=[numpy.get_include(), "third-party"]
)
