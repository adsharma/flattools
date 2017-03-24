# -*- coding: utf-8 -*-



from .exc import FbsLexerError


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


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ignore_SILLYCOMM(t):
    r'\/\*\**\*\/'
    t.lexer.lineno += t.value.count('\n')


def t_ignore_MULTICOMM(t):
    r'\/\*[^*]\/*([^*/]|[^*]\/|\*[^/])*\**\*\/'
    t.lexer.lineno += t.value.count('\n')


def t_ignore_DOCTEXT(t):
    r'\/\*\*([^*/]|[^*]\/|\*[^/])*\**\*\/'
    t.lexer.lineno += t.value.count('\n')


def t_ignore_UNIXCOMMENT(t):
    r'\#[^\n]*'


def t_ignore_COMMENT(t):
    r'\/\/[^\n]*'


def t_BOOLCONSTANT(t):
    r'\btrue\b|\bfalse\b'
    t.value = t.value == 'true'
    return t


def t_DUBCONSTANT(t):
    r'-?\d+\.\d*(e-?\d+)?'
    t.value = float(t.value)
    return t


def t_HEXCONSTANT(t):
    r'0x[0-9A-Fa-f]+'
    t.value = int(t.value, 16)
    t.type = 'INTCONSTANT'
    return t


def t_INTCONSTANT(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t


def t_LITERAL(t):
    r'(\"([^\\\n]|(\\.))*?\")|\'([^\\\n]|(\\.))*?\''
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


def t_IDENTIFIER(t):
    r'[a-zA-Z_](\.[a-zA-Z_0-9]|[a-zA-Z_0-9])*'

    if t.value in keywords:
        t.type = t.value.upper()
        return t
    if t.value in fbs_reserved_keywords:
        raise ThriftLexerError('Cannot use reserved language keyword: %r'
                               ' at line %d' % (t.value, t.lineno))
    return t
