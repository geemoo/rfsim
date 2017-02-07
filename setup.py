#!/usr/bin/env python

from distutils.core import setup

setup(
    name='rfsim',
    version='0.1',
    description='RF Lineup Simulation Utility',
    author='Jean Richard',
    author_email='jean@geemoo.ca',
    packages=[ 
        'rfsim',
        'rfsim/parts'
    ]
)
