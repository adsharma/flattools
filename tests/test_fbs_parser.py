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

def test_monsters():
    fbs = load('parser-cases/monster_test.fbs')
    assert fbs.root == 'Monster'
    assert fbs.file_extension == 'mon'
    assert fbs.file_identifier == 'MONS'

    stats = fbs.__fbs_meta__['tables'][2]
    assert stats._fspec['id1'] == (False, "[string]", [])

def test_thrift2fbs():
    fbs = load('parser-cases/thrift2fbs.fbs')
