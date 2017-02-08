#!/usr/bin/env python

# -*- coding: utf-8 -*-

import os
import sys

from fbs.fbs import FBSType
from fbs.parser import load, load_fp
from fbs.parser.exc import FbsParserError, FbsGrammerError
from jinja2 import Environment, FileSystemLoader

TEMPLATE='fbs_template_cpp.h'

def generate_cpp(filename, tree):
    dirname = os.path.dirname(os.path.abspath(filename))
    env = Environment(loader=FileSystemLoader(['.', dirname]), trim_blocks=True)
    prefix, extension = os.path.splitext(filename)
    out_file = prefix + '.h'
    target = open(out_file, 'w')
    setattr(tree, 'cpp_types', FBSType._VALUES_TO_CPP_TYPES)
    target.write(env.get_template(TEMPLATE).render(tree.__dict__))

if __name__ == '__main__':
    filename = sys.argv[1]
    generate_cpp(filename, load(filename))
