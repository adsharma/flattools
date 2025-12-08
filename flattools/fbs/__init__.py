# -*- coding: utf-8 -*-

import sys

from .parser import load, load_fp, load_module

__version__ = "0.6"
__python__ = sys.version_info
__all__ = ["load", "load_module", "load_fp", "fbs"]
