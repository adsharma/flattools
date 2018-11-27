#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import platform

from os.path import join, dirname

from setuptools import setup, find_packages
from setuptools.extension import Extension

with open(join(dirname(__file__), 'fbs', '__init__.py'), 'r') as f:
    version = re.match(r".*__version__ = '(.*?)'", f.read(), re.S).group(1)

install_requires = [
    "ply>=3.4,<4.0",
]

dev_requires = [
    "flake8>=2.5",
    "pytest>=2.8",
]

setup(name="flattools",
      version=version,
      description="Pure python implementation of Flatbuffers.",
      keywords="flatbuffers python thriftpy",
      author="Arun Sharma",
      author_email="asharma@fb.com",
      packages=find_packages(exclude=['docs', 'tests']),
      package_data={"flattools": ["contrib/tracking/tracking.thrift"]},
      entry_points={
        'console_scripts': ["flatc=bin.flatc:main"],
      },
      url="https://github.com/adsharma/flattools",
      license="MIT",
      zip_safe=False,
      long_description=open("README.rst").read(),
      install_requires=install_requires,
      extras_require={
          "dev": dev_requires,
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
