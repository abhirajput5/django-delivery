#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit(0)

with open('README.rst') as f:
    long_description = f.read()

VERSION = __import__('delivery').__version__

setup(
    name='django-delivery',
    version=VERSION,
    url='https://github.com/dakrauth/django-delivery',
    author_email='dakrauth@gmail.com',
    description='Basic Email Delivery.',
    long_description=long_description,
    author='David A Krauth',
    platforms=['any'],
    license='MIT License',
    classifiers=(
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ),
    packages=find_packages(),
)
