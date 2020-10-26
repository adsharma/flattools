import os
from typing import Optional, Tuple

from jinja2 import Environment, FileSystemLoader

from fbs.fbs import FBSType

GLOBAL_OPTIONS = {"trim_blocks": True, "lstrip_blocks": True}

_NAMESPACE_TO_TYPE = {
    "tables": FBSType.TABLE,
    "structs": FBSType.STRUCT,
    "enums": FBSType.ENUM,
    "unions": FBSType.UNION,
}


def get_type(name, module, primitive, optional=False, optionalize=None):
    try:
        base = primitive[name]
        if optional and optionalize:
            return optionalize(base)
        return base
    except KeyError:
        for namespace in _NAMESPACE_TO_TYPE.keys():
            for t in module.__fbs_meta__[namespace]:
                if t.__name__ == name:
                    return t.__name__
        if name.startswith("["):
            element_type = get_type(
                name[1:-1], module, module.FBSType._LOWER_NAMES_TO_VALUES
            )
            return "[{}]".format(get_type(element_type, module, primitive))
        return name


def get_module_name(name, module):
    for namespace in _NAMESPACE_TO_TYPE.keys():
        for mod in [module] + module.__fbs_meta__["includes"]:
            for t in mod.__fbs_meta__[namespace]:
                if t.__name__ == name:
                    return t.__module__
    return None


def parse_types(fbs_type, py_type) -> Tuple[bool, int, bool, Optional[FBSType], bool]:
    number_type = fbs_type in FBSType._NUMBER_TYPES
    bits = FBSType._BITS[fbs_type] if number_type else 0
    if py_type.startswith("["):
        primitive_type = False
        element_type = py_type[1:-1]
        element_type_primitive = element_type in FBSType._PRIMITIVE_TYPES_NAMES
    else:
        element_type = None
        element_type_primitive = False
        primitive_type = fbs_type in FBSType._PRIMITIVE_TYPES
    return (number_type, bits, primitive_type, element_type, element_type_primitive)


def lookup_fbs_type(module, fbs_type) -> Optional[FBSType]:
    """For complex types, check if something is a struct,
       table, union or an enum"""
    for namespace in _NAMESPACE_TO_TYPE.keys():
        for mod in [module] + module.__fbs_meta__["includes"]:
            for t in mod.__fbs_meta__[namespace]:
                if t.__name__ == fbs_type:
                    return _NAMESPACE_TO_TYPE[namespace]
    return None


def pre_generate_step(path):
    dirname, filename = os.path.split(os.path.abspath(path))
    env = Environment(
        loader=FileSystemLoader([".", "templates", dirname]), **GLOBAL_OPTIONS
    )
    prefix, extension = os.path.splitext(filename)
    return (prefix, env)
