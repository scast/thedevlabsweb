# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import thedevlabsweb
version = thedevlabsweb.__version__

setup(
    name='thedevlabsweb',
    version=version,
    author='',
    author_email='scastb@gmail.com',
    packages=[
        'thedevlabsweb',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.1',
    ],
    zip_safe=False,
    scripts=['thedevlabsweb/manage.py'],
)