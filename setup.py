#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 18:27:17 2019

@author: jezequel
"""

# -*- coding: utf-8 -*-
"""
@author: Steven Masfaraud
"""

from setuptools import setup
import re

def readme():
    with open('README.rst') as f:
        return f.read()

tag_re = re.compile(r'\btag: %s([0-9][^,]*)\b')
version_re = re.compile('^Version: (.+)$', re.M)

setup(name='supmeca_correction',
      description="Modules correction",
      long_description='',
      keywords='',
      url='',
      author='Ghislain Jézéquel',
      author_email='jezequel@dessia.tech',
      packages=['supmeca_correction'],
      install_requires=['matplotlib'])
