from flattools.fbs.fbs import FBSType


class FBSSwiftType(FBSType):
    _VALUES_TO_SWIFT_TYPES = {
        FBSType.BOOL: "Bool",
        FBSType.BYTE: "Int8",
        FBSType.UBYTE: "UInt8",
        FBSType.SHORT: "Int16",
        FBSType.USHORT: "UInt16",
        FBSType.INT: "Int",
        FBSType.UINT: "UInt",
        FBSType.FLOAT: "Float",
        FBSType.LONG: "Int64",
        FBSType.ULONG: "UInt64",
        FBSType.DOUBLE: "Double",
        FBSType.STRING: "String",
        FBSType.STRUCT: "interface",
        FBSType.TABLE: "interface",
        FBSType.UNION: "interface",
        FBSType.VECTOR: "interface",
        FBSType.ENUM: "enum",
    }


def optionalize(primitive):
    return f"{primitive}?"
