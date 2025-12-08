from ._compat import with_metaclass


def build_named_set(primitives, names):
    return {names[v].lower() for v in primitives}


class FBSType(object):
    BOOL = 0
    BYTE = 1
    UBYTE = 2
    SHORT = 3
    USHORT = 4
    INT = 5
    UINT = 6
    FLOAT = 7
    LONG = 8
    ULONG = 9
    DOUBLE = 10
    STRING = 11
    STRUCT = 12
    TABLE = 13
    UNION = 14
    VECTOR = 15
    # Special type not defined upstream, but used
    # to distinguish enums from unions
    ENUM = 100

    _NUMBER_TYPES = {
        BOOL,
        BYTE,
        UBYTE,
        SHORT,
        USHORT,
        INT,
        UINT,
        FLOAT,
        LONG,
        ULONG,
        DOUBLE,
    }

    _BITS = {
        BOOL: 1,
        BYTE: 8,
        UBYTE: 8,
        SHORT: 16,
        USHORT: 16,
        INT: 32,
        UINT: 32,
        FLOAT: 32,
        LONG: 64,
        ULONG: 64,
        DOUBLE: 64,
    }

    _VALUES_TO_NAMES = {
        BOOL: "BOOL",
        BYTE: "BYTE",
        UBYTE: "UBYTE",
        SHORT: "SHORT",
        USHORT: "USHORT",
        INT: "INT",
        UINT: "UINT",
        FLOAT: "FLOAT",
        LONG: "LONG",
        ULONG: "ULONG",
        DOUBLE: "DOUBLE",
        STRING: "STRING",
        STRUCT: "STRUCT",
        TABLE: "TABLE",
        UNION: "UNION",
        VECTOR: "VECTOR",
        ENUM: "ENUM",
    }

    _VALUES_TO_NAMES_LOWER = {k: v.lower() for k, v in _VALUES_TO_NAMES.items()}

    _LOWER_NAMES_TO_VALUES = {v.lower(): k for k, v in _VALUES_TO_NAMES.items()}

    _PRIMITIVE_TYPES = _NUMBER_TYPES.union({STRING})

    _PRIMITIVE_TYPES_NAMES = build_named_set(_PRIMITIVE_TYPES, _VALUES_TO_NAMES)


class TPayloadMeta(type):
    def __new__(cls, name, bases, attrs):
        return super(TPayloadMeta, cls).__new__(cls, name, bases, attrs)


class FBSPayload(with_metaclass(TPayloadMeta, object)):

    __hash__ = None

    def __repr__(self):
        attrs = ["%s=%r" % (key, value) for key, value in list(self.__dict__.items())]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(attrs))

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


def gen_init(cls, fbs_spec=None, default_spec=None):
    return cls
