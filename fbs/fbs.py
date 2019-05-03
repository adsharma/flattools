from fbs._compat import with_metaclass


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
        BOOL : 1,
        BYTE : 8,
        UBYTE : 8,
        SHORT : 16,
        USHORT : 16,
        INT : 32,
        UINT : 32,
        FLOAT : 32,
        LONG : 64,
        ULONG : 64,
        DOUBLE : 64,
    }

    _VALUES_TO_NAMES = {
        BOOL :'BOOL',
        BYTE :'BYTE',
        UBYTE :'UBYTE',
        SHORT :'SHORT',
        USHORT :'USHORT',
        INT :'INT',
        UINT :'UINT',
        FLOAT :'FLOAT',
        LONG :'LONG',
        ULONG :'ULONG',
        DOUBLE :'DOUBLE',
        STRING :'STRING',
        STRUCT : 'STRUCT',
        TABLE : 'TABLE',
        UNION : 'UNION'
    }

    _VALUES_TO_NAMES_LOWER = {
      k : v.lower() for k, v in _VALUES_TO_NAMES.items()
    }

    _PRIMITIVE_TYPES = _NUMBER_TYPES.union({STRING})

    _PRIMITIVE_TYPES_NAMES = build_named_set(_PRIMITIVE_TYPES, _VALUES_TO_NAMES)

    _VALUES_TO_CPP_TYPES = {
        BOOL :'bool',
        BYTE :'char',
        UBYTE :'uchar',
        SHORT :'short',
        USHORT :'ushort',
        INT :'int64_t',
        UINT :'uint64_t',
        FLOAT :'float',
        LONG :'int64_t',
        ULONG :'uint64_t',
        DOUBLE :'double',
        STRING :'std::string',
        STRUCT : 'struct',
        TABLE : 'struct',
        UNION : 'union'
    }

    _VALUES_TO_JAVA_TYPES = {
        BOOL: 'boolean',
        BYTE: 'char',
        UBYTE: 'char',
        SHORT: 'short',
        USHORT: 'short',
        INT: 'int',
        UINT: 'int',
        FLOAT: 'float',
        LONG: 'long',
        ULONG: 'long',
        DOUBLE: 'double',
        STRING: 'String',
        STRUCT: 'interface',
        TABLE: 'interface',
        UNION: 'interface',
    }

    _VALUES_TO_PY_TYPES = {
        BOOL: 'bool',
        BYTE: 'bytes',
        UBYTE: 'bytes',
        SHORT: 'int',
        USHORT: 'int',
        INT: 'int',
        UINT: 'int',
        FLOAT: 'float',
        LONG: 'int',
        ULONG: 'int',
        DOUBLE: 'float',
        STRING: 'str',
        STRUCT: 'interface',
        TABLE: 'interface',
        UNION: 'interface',
    }

    _VALUES_TO_PY_C_TYPES = {
        BOOL: 'bool',
        BYTE: 'int8',
        UBYTE: 'uint8',
        SHORT: 'int16',
        USHORT: 'uint16',
        INT: 'int32',
        UINT: 'uint32',
        FLOAT: 'float32',
        LONG: 'int64',
        ULONG: 'uint16',
        DOUBLE: 'float64',
        STRING: 'int',
        STRUCT: 'int',
        TABLE: 'int',
        UNION: 'int',
    }


class TPayloadMeta(type):

    def __new__(cls, name, bases, attrs):
        if "default_spec" in attrs:
            spec = attrs.pop("default_spec")
            # attrs["__init__"] = init_func_generator(cls, spec)
        return super(TPayloadMeta, cls).__new__(cls, name, bases, attrs)


class FBSPayload(with_metaclass(TPayloadMeta, object)):

    __hash__ = None

    def __repr__(self):
        l = ['%s=%r' % (key, value) for key, value in list(self.__dict__.items())]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(l))

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


def gen_init(cls, fbs_spec=None, default_spec=None):
    return cls
