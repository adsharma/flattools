#!/usr/bin/env python

# -*- coding: utf-8 -*-

import argparse
import os
import sys
import traceback

from fbs.fbs import FBSType
from fbs.parser import load
from fbs.parser.exc import FbsParserError, FbsGrammerError
from functools import partial
from jinja2 import Environment, FileSystemLoader

CPP_TEMPLATE='fbs_template_cpp.h'
IJAVA_TEMPLATE='fbs_template_interface.java'
YAML_TEMPLATE='fbs_template_yaml.yaml'
PYTHON_TEMPLATE='fbs_template.py'

def get_type(name, module, primitive):
    try:
        return primitive[name]
    except KeyError:
        for namespace in ('tables', 'enums', 'unions'):
            for t in module.__fbs_meta__[namespace]:
                if t.__name__ == name:
                    return t.__name__
        return name

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

def generate_cpp(path, tree):
    (prefix, env) = pre_generate_step(path)
    out_file = prefix + '_generated.h'
    with open(out_file, 'w') as target:
        setattr(tree, 'cpp_types', FBSType._VALUES_TO_CPP_TYPES)
        setattr(tree, 'get_type', partial(get_type, primitive=tree.cpp_types, module=tree))
        target.write(env.get_template(CPP_TEMPLATE).render(tree.__dict__))

def generate_ijava(path, tree):
    (prefix, env) = pre_generate_step(path)
    out_file = 'I' + prefix + '.java'
    with open(out_file, 'w') as target:
        setattr(tree, 'java_types', FBSType._VALUES_TO_JAVA_TYPES)
        setattr(tree, 'get_type', partial(get_type, primitive=tree.java_types, module=tree))
        target.write(env.get_template(IJAVA_TEMPLATE).render(tree.__dict__))

def generate_yaml(path, tree):
    (prefix, env) = pre_generate_step(path)
    out_file = prefix + '.yaml'
    with open(out_file, 'w') as target:
        setattr(tree, 'yaml_types', FBSType._VALUES_TO_NAMES_LOWER)
        setattr(tree, 'get_type', partial(get_type, primitive=tree.yaml_types, module=tree))
        target.write(env.get_template(YAML_TEMPLATE).render(tree.__dict__))

def generate_py(path, tree):
    (prefix, env) = pre_generate_step(path)
    if not os.path.exists(prefix):
        os.mkdir(prefix)
        open(os.path.join(prefix, '__init__.py'), "a").close()
    for table in tree.__fbs_meta__['tables']:
        out_file = os.path.join(prefix, table.__name__ + '.py')
        with open(out_file, 'w') as target:
            setattr(tree, 'python_types', FBSType._VALUES_TO_PY_TYPES)
            setattr(tree, 'get_type', partial(get_type, primitive=tree.python_types, module=tree))
            setattr(tree, 'table', table)
            setattr(tree, 'camel_case', camel_case)
            target.write(env.get_template(PYTHON_TEMPLATE).render(tree.__dict__))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--includes", action='store', nargs='+', help="Directories to search")
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
            generate_py(filename, load(filename))

if __name__ == '__main__':
    main()
