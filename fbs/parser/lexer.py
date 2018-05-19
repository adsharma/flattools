# -*- coding: utf-8 -*-



from .exc import FbsLexerError
from ply.lex import TOKEN


literals = ':;,=*{}()<>[]'


fbs_reserved_keywords = (
)


# https://google.github.io/flatbuffers/flatbuffers_grammar.html
keywords = (
    'namespace',
    'include',
    'attribute',
    'table',
    'struct',
    'enum',
    'union',
    'root_type',
    'bool',
    'byte',
    'ubyte',
    'short',
    'ushort',
    'int',
    'uint',
    'float',
    'long',
    'ulong',
    'double',
    'string',
    'file_extension',
    'file_identifier',
    'rpc_service',
)


tokens = (
    'BOOLCONSTANT',
    'INTCONSTANT',
    'DUBCONSTANT',
    'LITERAL',
    'IDENTIFIER',
) + tuple([kw.upper() for kw in keywords])


t_ignore = ' \t\r'   # whitespace


def t_error(t):
    raise ThriftLexerError('Illegal characher %r at line %d' %
                           (t.value[0], t.lineno))


@TOKEN(r'\n+')
def t_newline(t):
    t.lexer.lineno += len(t.value)

@TOKEN(r'\/\*\**\*\/')
def t_ignore_SILLYCOMM(t):
    t.lexer.lineno += t.value.count('\n')

@TOKEN(r'\/\*[^*]\/*([^*/]|[^*]\/|\*[^/])*\**\*\/')
def t_ignore_MULTICOMM(t):
    t.lexer.lineno += t.value.count('\n')

@TOKEN(r'\/\*\*([^*/]|[^*]\/|\*[^/])*\**\*\/')
def t_ignore_DOCTEXT(t):
    t.lexer.lineno += t.value.count('\n')

t_ignore_UNIXCOMMENT = r'\#[^\n]*'

t_ignore_COMMENT = r'\/\/[^\n]*'

@TOKEN(r'\btrue\b|\bfalse\b')
def t_BOOLCONSTANT(t):
    t.value = t.value == 'true'
    return t

@TOKEN(r'-?\d+\.\d*(e-?\d+)?')
def t_DUBCONSTANT(t):
    t.value = float(t.value)
    return t

@TOKEN(r'0x[0-9A-Fa-f]+')
def t_HEXCONSTANT(t):
    t.value = int(t.value, 16)
    t.type = 'INTCONSTANT'
    return t

@TOKEN(r'[+-]?[0-9]+')
def t_INTCONSTANT(t):
    t.value = int(t.value)
    return t

@TOKEN(r'(\"([^\\\n]|(\\.))*?\")|\'([^\\\n]|(\\.))*?\'')
def t_LITERAL(t):
    s = t.value[1:-1]
    maps = {
        't': '\t',
        'r': '\r',
        'n': '\n',
        '\\': '\\',
        '\'': '\'',
        '"': '\"'
    }
    i = 0
    length = len(s)
    val = ''
    while i < length:
        if s[i] == '\\':
            i += 1
            if s[i] in maps:
                val += maps[s[i]]
            else:
                msg = 'Unexcepted escaping characher: %s' % s[i]
                raise ThriftLexerError(msg)
        else:
            val += s[i]

        i += 1

    t.value = val
    return t

@TOKEN(r'[a-zA-Z_](\.[a-zA-Z_0-9]|[a-zA-Z_0-9])*')
def t_IDENTIFIER(t):
    if t.value in keywords:
        t.type = t.value.upper()
        return t
    if t.value in fbs_reserved_keywords:
        raise ThriftLexerError('Cannot use reserved language keyword: %r'
                               ' at line %d' % (t.value, t.lineno))
    return t
