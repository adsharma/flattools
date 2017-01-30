# -*- coding: utf-8 -*-

import pytest
from fbs.parser import load, load_fp
from fbs.parser.exc import FbsParserError, FbsGrammerError

def test_comments():
    load('parser-cases/comments.fbs')


def test_constants():
    fbs = load('parser-cases/constants.fbs')

def test_include():
    fbs = load('parser-cases/include.fbs', include_dirs=[
        './parser-cases'])
