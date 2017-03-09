#!/usr/bin/env python

# -*- coding: utf-8 -*-

import argparse
import os
import sys
import traceback

from fbs.fbs import FBSType
from fbs.parser import load, load_fp
from fbs.parser.exc import FbsParserError, FbsGrammerError
from functools import partial
from jinja2 import Environment, FileSystemLoader

CPP_TEMPLATE='fbs_template_cpp.h'
IJAVA_TEMPLATE='fbs_template_interface.java'

def get_type(name, module, primitive):
    try:
        return primitive[name]
    except KeyError:
        try:
            for t in module.__fbs_meta__['tables']:
                if t.__name__ == name:
                    return t.__name__
            raise KeyError(name)
        except KeyError:
            try:
              for e in module.__fbs_meta__['enums']:
                  if e.__name__ == name:
                      return e.__name__
            except KeyError:
                traceback.print_exc()

def generate_cpp(path, tree):
    dirname, filename = os.path.split(os.path.abspath(path))
    env = Environment(loader=FileSystemLoader(['.', dirname]), trim_blocks=True)
    prefix, extension = os.path.splitext(filename)
    out_file = prefix + '.h'
    target = open(out_file, 'w')
    setattr(tree, 'cpp_types', FBSType._VALUES_TO_CPP_TYPES)
    setattr(tree, 'get_type', partial(get_type, primitive=tree.cpp_types, module=tree))
    target.write(env.get_template(CPP_TEMPLATE).render(tree.__dict__))

def generate_ijava(path, tree):
    dirname, filename = os.path.split(os.path.abspath(path))
    env = Environment(loader=FileSystemLoader(['.', dirname]), trim_blocks=True)
    prefix, extension = os.path.splitext(filename)
    out_file = 'I' + prefix + '.java'
    target = open(out_file, 'w')
    setattr(tree, 'java_types', FBSType._VALUES_TO_JAVA_TYPES)
    setattr(tree, 'get_type', partial(get_type, primitive=tree.java_types, module=tree))
    target.write(env.get_template(IJAVA_TEMPLATE).render(tree.__dict__))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpp", type=bool, default=False, help="Generate C++ code")
    parser.add_argument("--ijava", type=bool, default=True, help="Generate Java interface code")
    args, rest = parser.parse_known_args()
    filename = rest[0]
    if args.cpp:
        generate_cpp(filename, load(filename))
    if args.ijava:
        generate_ijava(filename, load(filename))
