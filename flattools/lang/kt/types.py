from flattools.fbs.fbs import FBSType


class FBSKotlinType(FBSType):
    _VALUES_TO_KT_TYPES = {
        FBSType.BOOL: "Boolean",
        FBSType.BYTE: "Byte",
        FBSType.UBYTE: "UByte",
        FBSType.SHORT: "Short",
        FBSType.USHORT: "UShort",
        FBSType.INT: "Int",
        FBSType.UINT: "UInt",
        FBSType.FLOAT: "Float",
        FBSType.LONG: "Long",
        FBSType.ULONG: "ULong",
        FBSType.DOUBLE: "Double",
        FBSType.STRING: "String",
        FBSType.STRUCT: "interface",
        FBSType.TABLE: "interface",
        FBSType.UNION: "interface",
        FBSType.VECTOR: "interface",
        FBSType.ENUM: "enum class",
    }


def optionalize(primitive):
    return f"{primitive}?"
