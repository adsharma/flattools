#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import platform

from os.path import join, dirname

from setuptools import setup, find_packages
from setuptools.extension import Extension

with open(join(dirname(__file__), 'thriftpy', '__init__.py'), 'r') as f:
    version = re.match(r".*__version__ = '(.*?)'", f.read(), re.S).group(1)

install_requires = [
    "ply>=3.4,<4.0",
]

tornado_requires = [
    "tornado>=4.0,<5.0",
    "toro>=0.6"
]

dev_requires = [
    "flake8>=2.5",
    "pytest>=2.8",
    "sphinx-rtd-theme>=0.1.9",
    "sphinx>=1.3",
] + tornado_requires

setup(name="thriftpy",
      version=version,
      description="Pure python implementation of Apache Thrift.",
      keywords="thrift python thriftpy",
      author="Lx Yu",
      author_email="i@lxyu.net",
      packages=find_packages(exclude=['benchmark', 'docs', 'tests']),
      package_data={"thriftpy": ["contrib/tracking/tracking.thrift"]},
      entry_points={},
      url="https://thriftpy.readthedocs.org/",
      license="MIT",
      zip_safe=False,
      long_description=open("README.rst").read(),
      install_requires=install_requires,
      tests_require=tornado_requires,
      extras_require={
          "dev": dev_requires,
          "tornado": tornado_requires
      },
      classifiers=[
          "Topic :: Software Development",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
      ])
