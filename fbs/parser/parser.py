# -*- coding: utf-8 -*-

"""
IDL Ref:
    https://google.github.io/flatbuffers/flatbuffers_grammar.html
"""



import collections
import operator
import os
import sys
import types
from ply import lex, yacc
from .lexer import *  # noqa
from .exc import FbsParserError, FbsGrammerError
from thriftpy._compat import urlopen, urlparse
from fbs.fbs import FBSType, FBSPayload
from thriftpy.thrift import gen_init

def p_error(p):
    if p is None:
        raise FbsGrammerError('Grammer error at EOF')
    raise FbsGrammerError('Grammer error %r at line %d' %
                             (p.value, p.lineno))


def p_start(p):
    '''start : include_seq body_seq'''


def p_include_seq(p):
    '''include_seq : include_seq include_one
                    | include_one
                    |'''

def p_body_seq(p):
    '''body_seq : body_seq body
                    | body
                    |'''

def p_include_one(p):
    '''include_one : INCLUDE LITERAL ';' '''
    fbs = fbs_stack[-1]
    if fbs.__fbs_file__ is None:
        raise FbsParserError('Unexcepted include statement while loading'
                                'from file like object.')
    replace_include_dirs = [os.path.dirname(fbs.__fbs_file__)] \
        + include_dirs_
    for include_dir in replace_include_dirs:
        path = os.path.join(include_dir, p[2])
        if os.path.exists(path):
            child = parse(path)
            setattr(fbs, child.__name__, child)
            _add_fbs_meta('includes', child)
            return
    raise FbsParserError(('Couldn\'t include fbs %s in any '
                             'directories provided') % p[2])

def p_body(p):
    '''body : namespace
            | typedef
            | enum
            | root
            | file_extension
            | file_identifier
            | attribute
            | object
            |'''

def p_namespace(p):
    '''namespace : NAMESPACE IDENTIFIER ';' '''
    setattr(fbs_stack[-1], 'namespace', p[2])

def p_root(p):
    '''root : ROOT_TYPE IDENTIFIER ';' '''
    setattr(fbs_stack[-1], 'root', p[2])

def p_file_extension(p):
    '''file_extension : FILE_EXTENSION LITERAL ';' '''
    setattr(fbs_stack[-1], 'file_extension', p[2])

def p_file_identifier(p):
    '''file_identifier : FILE_IDENTIFIER LITERAL ';' '''
    setattr(fbs_stack[-1], 'file_identifier', p[2])

def p_metadata(p):
    '''metadata : '(' metadata_seq ')'
                |'''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = []

def p_metadata_seq(p):
    '''metadata_seq : metadata_item ',' metadata_seq
                    | metadata_item
                    |'''
    _parse_seq(p)

def p_metadata_item(p):
    '''metadata_item : IDENTIFIER
                     | IDENTIFIER ':' scalar'''
    p[0] = [p[1]]

def p_attribute(p):
    '''attribute : ATTRIBUTE LITERAL ';' '''

def p_object(p):
    '''object : '{' field_seq '}' '''

def p_typedef(p):
    '''typedef : table
       typedef : struct '''
    if (p[1]):
        setattr(fbs_stack[-1], p[1][0], p[1][1])

def p_enum(p):  # noqa
    '''enum : ENUM IDENTIFIER metadata '{' enum_seq '}'
       enum : ENUM IDENTIFIER ':' simple_base_type metadata '{' enum_seq '}'
       enum : union'''
    if len(p) == 9:
        val = _make_enum(p[2], p[7])
    elif len(p) == 7:
        val = _make_enum(p[2], p[5])
    else:
        val = p[1]
    if (len(p) > 2):
        setattr(fbs_stack[-1], p[2], val)
        _add_fbs_meta('enums', val)


def p_enum_seq(p):
    '''enum_seq : enum_item ',' enum_seq
                | enum_item enum_seq
                |'''
    _parse_seq(p)


def p_enum_item(p):
    '''enum_item : IDENTIFIER '=' INTCONSTANT
                 | IDENTIFIER
                 |'''
    if len(p) == 4:
        p[0] = [p[1], p[3]]
    elif len(p) == 2:
        p[0] = [p[1], None]


def p_struct(p):
    '''struct : STRUCT IDENTIFIER metadata '{' field_seq '}' '''
    val = _make_empty_struct(p[2])
    setattr(fbs_stack[-1], p[1], val)
    val = _fill_in_struct(val, p[5])
    _add_fbs_meta('structs', val)

def p_table(p):
    '''table : TABLE IDENTIFIER metadata '{' field_seq '}' '''
    val = _make_empty_struct(p[2])
    setattr(fbs_stack[-1], p[1], val)
    val = _fill_in_struct(val, p[5])
    _add_fbs_meta('tables', val)

def p_union(p):
    '''union : UNION IDENTIFIER metadata '{' enum_seq '}' '''
    val = _make_empty_struct(p[2])
    setattr(fbs_stack[-1], p[1], val)
    # Needs new code.
    #val = _fill_in_struct(val, p[5])
    _add_fbs_meta('unions', val)

def p_field_seq(p):
    '''field_seq : field field_seq
                 |'''
    _parse_seq(p)


def p_field(p):
    '''field : IDENTIFIER ':' type metadata ';'
             | IDENTIFIER ':' type '=' scalar metadata ';' '''
    if len(p) == 7:
        try:
            val = _cast(p[3])(p[5])
        except AssertionError:
            raise FbsParserError(
                'Type error for field %s '
                'at line %d' % (p[1], p.lineno(4)))
    else:
        val = None

    required = False
    if len(p) > 6:
        metadata = p[6]
    else:
        metadata = p[4]

    if metadata:
        # unbox the list (foo:bar is relatively uncommon)
        metadata = [ x[0] for x in metadata ]
        required = 'required' in metadata
    # field_id, required, type, name, value, metadata
    p[0] = [None, required, p[3], p[1], val, metadata]

def p_type(p):
    '''type : simple_base_type
            | '[' type ']'
            | IDENTIFIER'''
    if len(p) == 4:
        # XXX: Save vector=true somewhere
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_simple_base_type(p):  # noqa
    '''simple_base_type : BOOL
                        | BYTE
                        | UBYTE
                        | SHORT
                        | USHORT
                        | INT
                        | UINT
                        | FLOAT
                        | LONG
                        | ULONG
                        | DOUBLE
                        | STRING'''
    # TODO: make this less verbose and handle all types
    if p[1].upper() == 'BOOL':
        p[0] = FBSType.BOOL
    elif p[1].upper() == 'BYTE':
        p[0] = FBSType.BYTE
    elif p[1].upper() == 'SHORT':
        p[0] = FBSType.SHORT
    elif p[1].upper() == 'INT':
        p[0] = FBSType.INT
    elif p[1].upper() == 'LONG':
        p[0] = FBSType.LONG
    elif p[1].upper() == 'FLOAT':
        p[0] = FBSType.FLOAT
    elif p[1].upper() == 'DOUBLE':
        p[0] = FBSType.DOUBLE
    elif p[1].upper() == 'STRING':
        p[0] = FBSType.STRING
    else:
        p[0] = FBSType.STRUCT

def p_scalar(p):
    '''scalar : LITERAL
              | BOOLCONSTANT
              | DUBCONSTANT
              | INTCONSTANT
              | IDENTIFIER'''  # This violates grammar?

fbs_stack = []
include_dirs_ = ['.']
fbs_cache = {}

def sort_members(fbs):
   for member in ('tables', 'structs', 'unions', 'enum'):
      fbs.__fbs_meta__[member] = sorted(fbs.__fbs_meta__[member])

def parse(path, module_name=None, include_dirs=None, include_dir=None,
          lexer=None, parser=None, enable_cache=True, enable_sort=False):
    """Parse a single fbs file to module object, e.g.::

        >>> from thriftpy.parser.parser import parse
        >>> note_fbs = parse("path/to/note.fbs")
        <module 'note_fbs' (built-in)>

    :param path: file path to parse, should be a string ending with '.fbs'.
    :param module_name: the name for parsed module, the default is the basename
                        without extension of `path`.
    :param include_dirs: directories to find fbs files while processing
                         the `include` directive, by default: ['.'].
    :param include_dir: directory to find child fbs files. Note this keyword
                        parameter will be deprecated in the future, it exists
                        for compatiable reason. If it's provided (not `None`),
                        it will be appended to `include_dirs`.
    :param lexer: ply lexer to use, if not provided, `parse` will new one.
    :param parser: ply parser to use, if not provided, `parse` will new one.
    :param enable_cache: if this is set to be `True`, parsed module will be
                         cached, this is enabled by default. If `module_name`
                         is provided, use it as cache key, else use the `path`.
    """
    if os.name == 'nt' and sys.version_info < (3, 2):
        os.path.samefile = lambda f1, f2: os.stat(f1) == os.stat(f2)

    # dead include checking on current stack
    for fbs in fbs_stack:
        if fbs.__fbs_file__ is not None and \
                os.path.samefile(path, fbs.__fbs_file__):
            raise FbsParserError('Dead including on %s' % path)

    global fbs_cache

    cache_key = module_name or os.path.normpath(path)

    if enable_cache and cache_key in fbs_cache:
        return fbs_cache[cache_key]

    if lexer is None:
        lexer = lex.lex()
    if parser is None:
        parser = yacc.yacc(debug=False, write_tables=0)

    global include_dirs_

    if include_dirs is not None:
        include_dirs_ = include_dirs
    if include_dir is not None:
        include_dirs_.append(include_dir)

    if not path.endswith('.fbs'):
        raise FbsParserError('Path should end with .fbs')

    url_scheme = urlparse(path).scheme
    if url_scheme == 'file':
        with open(urlparse(path).netloc + urlparse(path).path) as fh:
            data = fh.read()
    elif url_scheme == '':
        with open(path) as fh:
            data = fh.read()
    elif url_scheme in ('http', 'https'):
        data = urlopen(path).read()
    else:
        raise FbsParserError('thriftpy does not support generating module '
                                'with path in protocol \'{}\''.format(
                                    url_scheme))

    if module_name is not None and not module_name.endswith('_fbs'):
        raise FbsParserError('thriftpy can only generate module with '
                                '\'_fbs\' suffix')

    if module_name is None:
        basename = os.path.basename(path)
        module_name = os.path.splitext(basename)[0]

    fbs = types.ModuleType(module_name)
    setattr(fbs, '__fbs_file__', path)
    fbs_stack.append(fbs)
    lexer.lineno = 1
    parser.parse(data)
    fbs_stack.pop()

    if enable_cache:
        fbs_cache[cache_key] = fbs
    if enable_sort:
        sort_members(fbs)
    return fbs


def parse_fp(source, module_name, lexer=None, parser=None, enable_cache=True,
             enable_sort=False):
    """Parse a file-like object to fbs module object, e.g.::

        >>> from thriftpy.fbs.parser.parser import parse_fp
        >>> with open("path/to/note.fbs") as fp:
                parse_fp(fp, "note_fbs")
        <module 'note_fbs' (built-in)>

    :param source: file-like object, expected to have a method named `read`.
    :param module_name: the name for parsed module, shoule be endswith
                        '_fbs'.
    :param lexer: ply lexer to use, if not provided, `parse` will new one.
    :param parser: ply parser to use, if not provided, `parse` will new one.
    :param enable_cache: if this is set to be `True`, parsed module will be
                         cached by `module_name`, this is enabled by default.
    """
    if not module_name.endswith('_fbs'):
        raise FbsParserError('thriftpy can only generate module with '
                                '\'_fbs\' suffix')

    if enable_cache and module_name in fbs_cache:
        return fbs_cache[module_name]

    if not hasattr(source, 'read'):
        raise FbsParserError('Except `source` to be a file-like object with'
                                'a method named \'read\'')

    if lexer is None:
        lexer = lex.lex()
    if parser is None:
        parser = yacc.yacc(debug=False, write_tables=0)

    data = source.read()

    fbs = types.ModuleType(module_name)
    setattr(fbs, '__fbs_file__', None)
    fbs_stack.append(fbs)
    lexer.lineno = 1
    parser.parse(data)
    fbs_stack.pop()

    if enable_cache:
        fbs_cache[module_name] = fbs
    if enable_sort:
        sort_members(fbs)
    return fbs


def _add_fbs_meta(key, val):
    fbs = fbs_stack[-1]

    if not hasattr(fbs, '__fbs_meta__'):
        meta = collections.defaultdict(list)
        setattr(fbs, '__fbs_meta__',  meta)
    else:
        meta = getattr(fbs, '__fbs_meta__')

    meta[key].append(val)


def _parse_seq(p):
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 1:
        p[0] = []


def _cast(t):  # noqa
    if t == FBSType.BOOL:
        return _cast_bool
    if t == FBSType.BYTE:
        return _cast_byte
    if t == FBSType.SHORT:
        return _cast_short
    if t == FBSType.INT:
        return _cast_int
    if t == FBSType.LONG:
        return _cast_long
    if t == FBSType.DOUBLE:
        return _cast_double
    if t == FBSType.STRING:
        return _cast_string
    if t[0] == FBSType.I32:
        return _cast_enum(t)
    if t[0] == FBSType.STRUCT:
        return _cast_struct(t)


def _cast_bool(v):
    assert isinstance(v, (bool, int))
    return bool(v)


def _cast_byte(v):
    assert isinstance(v, int)
    return v


def _cast_short(v):
    assert isinstance(v, int)
    return v


def _cast_int(v):
    assert isinstance(v, int)
    return v


def _cast_long(v):
    assert isinstance(v, int)
    return v


def _cast_double(v):
    assert isinstance(v, (float, int))
    return float(v)


def _cast_string(v):
    assert isinstance(v, str)
    return v


def _cast_enum(t):
    assert t[0] == FBSType.I32

    def __cast_enum(v):
        assert isinstance(v, int)
        if v in t[1]._VALUES_TO_NAMES:
            return v
        raise FbsParserError('Couldn\'t find a named value in enum '
                                '%s for value %d' % (t[1].__name__, v))
    return __cast_enum


def _cast_struct(t):   # struct/exception/union
    assert t[0] == FBSType.STRUCT

    def __cast_struct(v):
        if isinstance(v, t[1]):
            return v  # already cast

        assert isinstance(v, dict)
        tspec = getattr(t[1], '_tspec')

        for key in tspec:  # requirement check
            if tspec[key][0] and key not in v:
                raise FbsParserError('Field %r was required to create '
                                        'constant for type %r' %
                                        (key, t[1].__name__))

        for key in v:  # cast values
            if key not in tspec:
                raise FbsParserError('No field named %r was '
                                        'found in struct of type %r' %
                                        (key, t[1].__name__))
            v[key] = _cast(tspec[key][1])(v[key])
        return t[1](**v)
    return __cast_struct


def _make_enum(name, kvs):
    attrs = {'__module__': fbs_stack[-1].__name__}
    cls = type(name, (object, ), attrs)

    _values_to_names = {}
    _names_to_values = {}

    if kvs:
        val = kvs[0][1]
        if val is None:
            val = -1
        for item in kvs:
            if item[1] is None:
                item[1] = val + 1
            val = item[1]
        for key, val in kvs:
            setattr(cls, key, val)
            _values_to_names[val] = key
            _names_to_values[key] = val
    setattr(cls, '_VALUES_TO_NAMES', _values_to_names)
    setattr(cls, '_NAMES_TO_VALUES', _names_to_values)
    return cls

def _make_empty_struct(name, FBSType=FBSType.STRUCT, base_cls=FBSPayload):
    attrs = {'__module__': fbs_stack[-1].__name__, '_FBSType': FBSType}
    return type(name, (base_cls, ), attrs)


def _fill_in_struct(cls, fields, _gen_init=True):
    # XXX: Is fbs_spec needed, since flatbuffers don't have field order?
    fbs_spec = collections.OrderedDict()
    default_spec = []
    _fspec = collections.OrderedDict()

    # Use sorted() here like so:
    # for field in fields, key=operator.itemgetter(3)):
    # Only if args.sorted is set in main
    for field in fields:
        # field format: field_id, required, type, name, value, metadata
        # See p_field() above for details
        if field[3] in _fspec:
            raise FbsGrammerError(('\'%s\' field identifier/name has '
                                      'already been used') % (field[3]))
        FBSType = field[2]
        fbs_spec[field[3]] = _fbstype_spec(FBSType, field[3], field[1])
        default_spec.append((field[3], field[4]))
        _fspec[field[3]] = field[1], FBSType, field[5]
    setattr(cls, 'fbs_spec', fbs_spec)
    setattr(cls, 'default_spec', default_spec)
    setattr(cls, '_fspec', _fspec)
    if _gen_init:
        gen_init(cls, fbs_spec, default_spec)
    return cls


def _make_struct(name, fields, FBSType=FBSType.STRUCT, base_cls=FBSPayload,
                 _gen_init=True):
    cls = _make_empty_struct(name, FBSType=FBSType, base_cls=base_cls)
    return _fill_in_struct(cls, fields, _gen_init=_gen_init)

def _fbstype_spec(fbstype, name, required=False):
    return fbstype, name, required


def _get_fbstype(inst, default_fbstype=None):
    if hasattr(inst, '__dict__') and '_fbstype' in inst.__dict__:
        return inst.__dict__['_fbstype']
    return default_fbstype
