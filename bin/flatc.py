#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import argparse

from fbs.parser import load
from lang.py.generate import generate_py
from lang.yaml.generate import generate_yaml
from lang.java.generate import generate_ijava
from lang.cpp.generate import generate_cpp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--includes", action="store", nargs="+", help="Directories to search"
    )
    parser.add_argument(
        "--templates", action="store", nargs="+", help="Filename to template"
    )
    parser.add_argument("--cpp", type=bool, default=False, help="Generate C++ code")
    parser.add_argument(
        "--ijava", type=bool, default=False, help="Generate Java interface code"
    )
    parser.add_argument("--yaml", type=bool, default=False, help="Generate Yaml code")
    parser.add_argument(
        "--python", type=bool, default=False, help="Generate Python code"
    )
    # TODO: pass args.sort to parser
    parser.add_argument(
        "--sort", type=bool, default=False, help="Sort everything alphabetically"
    )
    args, rest = parser.parse_known_args()
    for filename in rest:
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


if __name__ == "__main__":
    main()
