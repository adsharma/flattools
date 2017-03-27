# -*- coding: utf-8 -*-

"""
    fbs.parser
    ~~~~~~~~~~~~~~~

    Flatbuffer parser using ply
"""



import os
import sys

from .parser import parse, parse_fp


def load(path, module_name=None, include_dirs=None, include_dir=None):
    """Load fbs file as a module.

    The module loaded and objects inside may only be pickled if module_name
    was provided.

    Note: `include_dir` will be depreacated in the future, use `include_dirs`
    instead. If `include_dir` was provided (not None), it will be appended to
    `include_dirs`.
    """
    real_module = bool(module_name)
    fbs = parse(path, module_name, include_dirs=include_dirs,
                   include_dir=include_dir)

    if real_module:
        sys.modules[module_name] = fbs
    return fbs


def load_fp(source, module_name):
    """Load fbs file like object as a module.
    """
    fbs = parse_fp(source, module_name)
    sys.modules[module_name] = fbs
    return fbs


def _import_module(import_name):
    if '.' in import_name:
        module, obj = import_name.rsplit('.', 1)
        return getattr(__import__(module, None, None, [obj]), obj)
    else:
        return __import__(import_name)


def load_module(fullname):
    """Load fbs by fullname, fullname should have '_fbs' as
    suffix.
    The loader will replace the '_fbs' with '.fbs' and use it as
    filename to locate the real fbs file.
    """
    if not fullname.endswith("_fbs"):
        raise ImportError(
            "FlatbufferPy can only load module with '_fbs' suffix")

    if fullname in sys.modules:
        return sys.modules[fullname]

    if '.' in fullname:
        module_name, fbs_module_name = fullname.rsplit('.', 1)
        module = _import_module(module_name)
        path_prefix = os.path.dirname(os.path.abspath(module.__file__))
        path = os.path.join(path_prefix, fbs_module_name)
    else:
        path = fullname
    fbs_file = "{0}.fbs".format(path[:-7])

    module = load(fbs_file, module_name=fullname)
    sys.modules[fullname] = module
    return sys.modules[fullname]
