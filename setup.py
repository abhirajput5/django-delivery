#!/usr/bin/env python
import os, sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
        'Programming Language :: Python :: 2.7',
    ),
    packages=['delivery', 'delivery.management', 'delivery.management.commands'],
    install_requires=['django<2.0']
)
