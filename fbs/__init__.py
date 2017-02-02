# -*- coding: utf-8 -*-

import sys

from .parser import load, load_module, load_fp

__version__ = '0.3.9'
__python__ = sys.version_info
__all__ = [ "load", "load_module", "load_fp", "fbs"]
