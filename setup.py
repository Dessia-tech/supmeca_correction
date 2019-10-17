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

from os.path import dirname, isdir, join
import re
from subprocess import CalledProcessError, check_output


def readme():
    with open('README.rst') as f:
        return f.read()


tag_re = re.compile(r'\btag: %s([0-9][^,]*)\b')
version_re = re.compile('^Version: (.+)$', re.M)


#def get_version():
#    # Return the version if it has been injected into the file by git-archive
#    version = tag_re.search('$Format:%D$')
#    if version:
#        return version.group(1)
#
#    d = dirname(__file__)
#    
#    if isdir(join(d, '.git')):
#        cmd = 'git describe --tags'
#        try:
#            version = check_output(cmd.split()).decode().strip()[:]
#        except CalledProcessError:
#            raise RuntimeError('Unable to get version number from git tags')
#        if version[0]=='v':
#            version = version[1:]
#        # PEP 440 compatibility
#        if '-' in version:
#            future_version = version.split('-')[0].split('.')
#            future_version[-1] = str(int(future_version[-1])+1)
#            future_version = '.'.join(future_version)
#            number_commits = version.split('-')[1]
#            version = '{}.dev{}'.format(future_version, number_commits)
#            return version
#
#    else:
#        # Extract the version from the PKG-INFO file.
#        with open(join(d, 'PKG-INFO')) as f:
#            version = version_re.search(f.read()).group(1)
#                 
#    return version


#import powertransmission
setup(name='supmeca_correction',
#      version=get_version(),
      description="Modules correction",
      long_description='',
      keywords='',
      url='',
#      cmdclass['register']=None,
      author='Ghislain Jézéquel',
      author_email='jezequel@dessia.tech',
      packages=['supmeca_correction'],
      install_requires=[''])
