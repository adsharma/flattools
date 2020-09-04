#!/usr/bin/env python

# -*- coding: utf-8 -*-

import argparse
import os
import re
import sys
import traceback

from fbs.fbs import FBSType
from fbs.parser import load
from fbs.parser.exc import FbsParserError, FbsGrammerError
from functools import partial
from jinja2 import Environment, FileSystemLoader
from keyword import kwlist
from typing import Optional, List, Tuple

CPP_TEMPLATE='fbs_template_cpp.h'
IJAVA_TEMPLATE='fbs_template_interface.java'
YAML_TEMPLATE='fbs_template_yaml.yaml'
PYTHON_TEMPLATE='fbs_template.py'

_NAMESPACE_TO_TYPE = {
    'tables': FBSType.TABLE,
    'structs': FBSType.STRUCT,
    'enums': FBSType.ENUM,
    'unions': FBSType.UNION,
}

def get_type(name, module, primitive):
    try:
        return primitive[name]
    except KeyError:
        for namespace in _NAMESPACE_TO_TYPE.keys():
            for t in module.__fbs_meta__[namespace]:
                if t.__name__ == name:
                    return t.__name__
        if name.startswith("["):
            element_type = get_type(name[1:-1], module, module.FBSType._LOWER_NAMES_TO_VALUES)
            return '[{}]'.format(get_type(element_type, module, primitive))
        return name

def get_module_name(name, module):
    for namespace in _NAMESPACE_TO_TYPE.keys():
        for mod in [module] + module.__fbs_meta__['includes']:
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
        for mod in [module] + module.__fbs_meta__['includes']:
            for t in mod.__fbs_meta__[namespace]:
                if t.__name__ == fbs_type:
                    return _NAMESPACE_TO_TYPE[namespace]
    return None

def c_int_types(module) -> List:
    """Figure out what int types need to be imported from ctypes"""
    c_types = []
    for namespace in _NAMESPACE_TO_TYPE.keys():
        for t in module.__fbs_meta__[namespace]:
           for _, mtype in t._fspec.items():
                fbs_type = mtype[1]
                if fbs_type in FBSType._PRIMITIVE_TYPES:
                    py_type = FBSType._VALUES_TO_PY_TYPES[fbs_type]
                    if re.search("int\d", py_type):
                        c_types.append(py_type)
    return c_types

# Should be compatible with GenTypeBasic() upstream
def py_gen_type(fbs_type) -> str:
    return FBSType._VALUES_TO_PY_C_TYPES[fbs_type]

# Should be compatible with GenMethod() upstream
def py_gen_method(fbs_type) -> str:
    is_primitive = fbs_type in FBSType._PRIMITIVE_TYPES
    if is_primitive:
        return camel_case(py_gen_type(fbs_type))
    elif fbs_type == FBSType.STRUCT:
        return "Struct"
    else:
        return "UOffsetTRelative"

# Similar to, but not compatible with GenGetter() upstream
def py_gen_getter(fbs_type) -> Tuple[str, Tuple]:
    if fbs_type == FBSType.STRING:
        return ("String", ())
    elif fbs_type == FBSType.UNION or fbs_type == FBSType.ENUM:
        return ("Get", ("flatbuffers.number_types.{}Flags".format("Int8"),))
    elif fbs_type == FBSType.VECTOR:
        _, _, _, element_type, _ = parse_types(fbs_type, get_type(fbs_type))
        return ("Get", ("flatbuffers.number_types.{}Flags".format(camel_case(py_gen_type(element_type))),))
    else:
        return ("Get", ("flatbuffers.number_types.{}Flags".format(camel_case(py_gen_type(fbs_type))),))

def camel_case(text: str) -> str:
    return ''.join([x.title() for x in text.split('_')])

GLOBAL_OPTIONS = {
  'trim_blocks' : True,
  'lstrip_blocks' : True,
}

def pre_generate_step(path):
    dirname, filename = os.path.split(os.path.abspath(path))
    env = Environment(loader=FileSystemLoader(['.', dirname]), **GLOBAL_OPTIONS)
    prefix, extension = os.path.splitext(filename)
    return (prefix, env)

def generate_cpp(path, tree, template=CPP_TEMPLATE):
    (prefix, env) = pre_generate_step(path)
    out_file = prefix + '_generated.h'
    setattr(tree, 'FBSType', FBSType)
    with open(out_file, 'w') as target:
        setattr(tree, 'cpp_types', FBSType._VALUES_TO_CPP_TYPES)
        setattr(tree, 'get_type', partial(get_type, primitive=tree.cpp_types, module=tree))
        target.write(env.get_template(template).render(tree.__dict__))

def generate_ijava(path, tree, template=IJAVA_TEMPLATE):
    (prefix, env) = pre_generate_step(path)
    out_file = 'I' + prefix + '.java'
    setattr(tree, 'FBSType', FBSType)
    with open(out_file, 'w') as target:
        setattr(tree, 'java_types', FBSType._VALUES_TO_JAVA_TYPES)
        setattr(tree, 'get_type', partial(get_type, primitive=tree.java_types, module=tree))
        target.write(env.get_template(template).render(tree.__dict__))

def generate_yaml(path, tree, template=YAML_TEMPLATE):
    (prefix, env) = pre_generate_step(path)
    out_file = prefix + '.yaml'
    setattr(tree, 'FBSType', FBSType)
    with open(out_file, 'w') as target:
        setattr(tree, 'yaml_types', FBSType._VALUES_TO_NAMES_LOWER)
        setattr(tree, 'get_type', partial(get_type, primitive=tree.yaml_types, module=tree))
        target.write(env.get_template(template).render(tree.__dict__))

def generate_py(path, tree, templates=[PYTHON_TEMPLATE, None, None]):
    (prefix, env) = pre_generate_step(path)
    if not os.path.exists(prefix):
        os.mkdir(prefix)
        open(os.path.join(prefix, '__init__.py'), "a").close()
    table_template, union_template, enum_template = templates
    setattr(tree, 'module', tree)
    # Type related methods
    setattr(tree, 'FBSType', FBSType)
    setattr(tree, 'python_types', FBSType._VALUES_TO_PY_TYPES)
    setattr(tree, 'get_type', partial(get_type, primitive=tree.python_types, module=tree))
    setattr(tree, 'get_module_name', partial(get_module_name, module=tree))
    setattr(tree, 'lookup_fbs_type', lookup_fbs_type)
    setattr(tree, 'parse_types', parse_types)
    setattr(tree, 'c_int_types', partial(c_int_types, module=tree))
    # Strings
    setattr(tree, 'camel_case', camel_case)
    setattr(tree, 'python_reserved', kwlist)
    # Python specific
    setattr(tree, 'py_gen_type', py_gen_type)
    setattr(tree, 'py_gen_method', py_gen_method)
    setattr(tree, 'py_gen_getter', py_gen_getter)
    for table in tree.__fbs_meta__['tables']:
        out_file = os.path.join(prefix, table.__name__ + '.py')
        with open(out_file, 'w') as target:
            setattr(tree, 'table', table)
            target.write(env.get_template(table_template).render(tree.__dict__))
    for fbs_union in tree.__fbs_meta__['unions']:
        out_file = os.path.join(prefix, fbs_union.__name__ + '.py')
        with open(out_file, 'w') as target:
            setattr(tree, 'fbs_union', fbs_union)
            target.write(env.get_template(union_template).render(tree.__dict__))
    for fbs_enum in tree.__fbs_meta__['enums']:
        out_file = os.path.join(prefix, fbs_enum.__name__ + '.py')
        with open(out_file, 'w') as target:
            setattr(tree, 'fbs_enum', fbs_enum)
            target.write(env.get_template(enum_template).render(tree.__dict__))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--includes", action='store', nargs='+', help="Directories to search")
    parser.add_argument("--templates", action='store', nargs='+', help="Filename to template")
    parser.add_argument("--cpp", type=bool, default=False, help="Generate C++ code")
    parser.add_argument("--ijava", type=bool, default=False, help="Generate Java interface code")
    parser.add_argument("--yaml", type=bool, default=False, help="Generate Yaml code")
    parser.add_argument("--python", type=bool, default=False, help="Generate Python code")
    # TODO: pass args.sort to parser
    parser.add_argument("--sort", type=bool, default=False, help="Sort everything alphabetically")
    args, rest = parser.parse_known_args()
    for filename in rest:
        parsed = load(filename, include_dirs=args.includes)
        if args.cpp:
            generate_cpp(filename, load(filename))
        if args.ijava:
            generate_ijava(filename, load(filename))
        if args.yaml:
            generate_yaml(filename, load(filename))
        if args.python:
            if args.templates:
                generate_py(filename, load(filename), args.templates)
            else:
                generate_py(filename, load(filename))

if __name__ == '__main__':
    main()
