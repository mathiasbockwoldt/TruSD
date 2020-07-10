#!/usr/bin/env python3

import setuptools

long_description = open('README.md').read()

setuptools.setup(
    name='TruSD', # Replace with your own username
    version='0.0.1',
    author='Mathias Bockwoldt',
    author_email='mathias.bockwoldt@uit.no',
    description='TruSD co-infers selection coefficients and genetic drift from allele trajectories using a maximum-likelihood framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mathiasbockwoldt/TruSD',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['trusd = trusd.cli:main']},
    install_requires=[
        'numpy>=1.15.1',
        'scipy>=0.16.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    #python_requires='>=3.6',
)
