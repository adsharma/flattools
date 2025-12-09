from flattools.fbs.fbs import FBSType


class FBSPyType(FBSType):
    _VALUES_TO_PY_TYPES = {
        FBSType.BOOL: "bool",
        FBSType.BYTE: "int8",
        FBSType.UBYTE: "int8",
        FBSType.SHORT: "int16",
        FBSType.USHORT: "int16",
        FBSType.INT: "int",
        FBSType.UINT: "int32",
        FBSType.FLOAT: "float",
        FBSType.LONG: "int64",
        FBSType.ULONG: "uint64",
        FBSType.DOUBLE: "float",
        FBSType.STRING: "str",
        FBSType.STRUCT: "interface",
        FBSType.TABLE: "interface",
        FBSType.UNION: "interface",
        FBSType.VECTOR: "interface",
        FBSType.ENUM: "interface",
    }

    _VALUES_TO_PY_C_TYPES = {
        FBSType.BOOL: "bool",
        FBSType.BYTE: "int8",
        FBSType.UBYTE: "uint8",
        FBSType.SHORT: "int16",
        FBSType.USHORT: "uint16",
        FBSType.INT: "int32",
        FBSType.UINT: "uint32",
        FBSType.FLOAT: "float32",
        FBSType.LONG: "int64",
        FBSType.ULONG: "uint16",
        FBSType.DOUBLE: "float64",
        FBSType.STRING: "int",
        FBSType.STRUCT: "int",
        FBSType.TABLE: "int",
        FBSType.UNION: "int",
        FBSType.VECTOR: "int",
        FBSType.ENUM: "int",
    }


def optionalize(primitive: str):
    return f"Option[{primitive}]"

def listify(primitive: str):
    return f"List[{primitive}]"
