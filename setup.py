#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    
import os

setup(
    name = "kombu-sqs",
    version = "0.1-alpha",
    #url = '',
	#download_url = '',
    license = 'BSD',
    #description = "",
    #author = '',
    #author_email = '',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Kombu',
        'Intended Audience :: Developers',
        'License :: BSD',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
