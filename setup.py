#!/usr/bin/env python

from distutils.core import setup

####### Used for compatability with python 2.2.3 ######
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
########################################################

with open('README.rst') as file:
    long_description = file.read()

setup(
        # Required information
        name='',
        version='',         # major.minor[.patch[.sub]]
        url='',

        # Switch out
        author='',          # or user maintainer
        author_email='',    # or use maintainer_email
        maintainer='',
        maintainer_email='',

        # optional
        description='',
        long_description=long_description,
        download_url='',
        classifiers=['', ''],
        platforms=['', ''],
        license='',
        )
