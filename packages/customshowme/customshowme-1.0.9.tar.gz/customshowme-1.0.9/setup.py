#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from distutils.core import setup

def publish():
	"""Publish to PyPi"""
	os.system("python setup.py sdist upload")
	
if sys.argv[-1] == 'publish':
	publish()
	sys.exit()


setup(
	name='customshowme',
	version='1.0.9',
	description='Painless Debugging and Inspection for Python',
	long_description="TODO: long description",
	author='Navdeep Gill',
	author_email='mr.navdeepgill@gmail.com',
	url='http://github.com/a-t-0/customshowme',
	packages=['customshowme'],
	install_requires=[
		'colorama>=0.1.18', 
		'decorator>=3.2.0'
	],
	license='MIT',
	classifiers = [ 
	  'Development Status :: 5 - Production/Stable',
	  'Environment :: Console',
	  'Intended Audience :: Developers',
	  'License :: OSI Approved :: MIT License',
	  'Programming Language :: Python',
	  'Programming Language :: Python :: 2.5',
	  'Programming Language :: Python :: 2.6',
	  'Programming Language :: Python :: 2.7',
	  'Operating System :: MacOS :: MacOS X',
	  'Operating System :: Unix',
	  'Operating System :: POSIX',
	  'Topic :: Software Development',
	  'Topic :: Software Development :: Libraries',
	  'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
