#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='Writeit-django',
      version='0.0',
      keywords=['POPlus', 'Writeit'],
      author=u"Ciudadano Inteligente",
      author_email='devteam@ciudadanointeligente.org',
      url='https://github.com/ciudadanointeligente/writeit',
      license='GNU Affero General Public License v3',
      classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU Affero General Public License v3',
      'Topic :: Internet :: WWW/HTTP'
      ],
      packages=find_packages())