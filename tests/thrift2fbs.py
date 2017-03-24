# -*- coding: utf-8 -*-

import sys

from thriftpy.thrift import TType
from fbs.fbs import FBSType
from thriftpy.parser import load
from thriftpy.parser.exc import ThriftParserError, ThriftGrammerError

thrift2_fbs_typemap = {
    TType.BOOL : FBSType.BOOL,
    TType.BYTE : FBSType.BYTE,
    TType.I16 : FBSType.SHORT,
    TType.I32 : FBSType.INT,
    TType.I64 : FBSType.LONG,
    TType.DOUBLE : FBSType.DOUBLE,
    TType.STRING : FBSType.STRING,
}

def fbstype(ttype):
    try:
        name = FBSType._VALUES_TO_NAMES[thrift2_fbs_typemap[ttype[0]]]
        return name.lower()
    except:
        # structs retain their name
        if (ttype[0] == TType.STRUCT):
            return ttype[2].__name__

def check_fbs_unsupported(tree):
    '''Throw ThriftParserError if features unsupported by fbs are used.'''
    meta = tree.__thrift_meta__
    for feature in ['services', 'consts', 'exceptions']:
        if meta[feature]:
            raise ThriftParserError("%s not supported" % feature)

def generate_fbs(tree):
    meta = tree.__thrift_meta__
    for s in meta['structs']:
        print('table', s.__name__, '{')
        for order, field in list(s.thrift_spec.items()):
            print('  ', field[1], ':', fbstype(field), ';')
        print('}')
        print()
    for e in meta['enums']:
        print('enum', e.__name__, ':', fbstype([e._ttype]), '{')
        for field, value in list(e._NAMES_TO_VALUES.items()):
            print("  %s = %s," % (field, value))
        print('}')
        print()

if __name__ == '__main__':
    tree = load(sys.argv[1])
    check_fbs_unsupported(tree)
    generate_fbs(tree)
