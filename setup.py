#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

import io
import os
import re
import sys

from about import description, version
from setuptools import setup, find_packages

RE_REQUIREMENT = re.compile(r'^\s*-r\s*(?P<filename>.*)$')

PYPI_RST_FILTERS = (
    # Replace Python crossreferences by simple monospace
    (r':(?:class|func|meth|mod|attr|obj|exc|data|const):`~(?:\w+\.)*(\w+)`', r'``\1``'),
    (r':(?:class|func|meth|mod|attr|obj|exc|data|const):`([^`]+)`', r'``\1``'),
    # replace doc references
    (r':doc:`(.+) <(.*)>`', r'`\1 <http://cb-manager.readthedocs.org/en/stable\2.html>`_'),
    # replace issues references
    (r':issue:`(.+?)`', r'`#\1 <https://github.com/astrid-project/cb-manager/issues/\1>`_'),
    # replace pr references
    (r':pr:`(.+?)`', r'`#\1 <https://github.com/astrid-project/cb-manager/pull/\1>`_'),
    # replace commit references
    (r':commit:`(.+?)`', r'`#\1 <https://github.com/astrid-project/cb-manager/commit/\1>`_'),
    # Drop unrecognised currentmodule
    (r'\.\. currentmodule:: .*', ''),
)


def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    Remove unsupported github tags:
     - code-block directive
     - all badges
    '''
    content = io.open(filename).read()
    for regex, replacement in PYPI_RST_FILTERS:
        content = re.sub(regex, replacement, content)
    return content



def pip(dirname):
    '''Parse pip requirements file and transform it to setuptools requirements.'''
    requirements = []
    for line in io.open(os.path.join(dirname, 'requirements.txt')):
        line = line.strip()
        if not line or '://' in line or line.startswith('#'):
            continue
        requirements.append(line)
    return requirements


long_description = '\n'.join((
    rst('README.rst'),
    rst('CHANGELOG.rst'),
    ''
))

install_require = pip('.')
docs_require = pip('docs') + install_require
tests_require = pip('tests') + install_require
dev_require = pip('dev') + docs_require + tests_require

setup(
    name='cb-manager',
    version=version,
    description=description,
    long_description=long_description,
    url='https://github.com/astrid-project/cb-manager',
    author='Alex Carrega',
    author_email='alessndro.carrega@cnit.it',
    packages=find_packages(exclude=['test', 'test.*']),
    include_package_data=True,
    install_requires=install_require,
    tests_require=tests_require,
    dev_require=dev_require,
    license='MIT',
    zip_safe=False,
    keywords='context-broker ebpf monitoring-agents database elasticsearch logstash kafka python java manager programmability agents cb-manager api openapi rest',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: System :: Software Distribution',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
