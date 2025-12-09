from flattools.fbs.fbs import FBSType


class FBSJavaType(FBSType):
    _VALUES_TO_JAVA_TYPES = {
        FBSType.BOOL: "boolean",
        FBSType.BYTE: "char",
        FBSType.UBYTE: "char",
        FBSType.SHORT: "short",
        FBSType.USHORT: "short",
        FBSType.INT: "int",
        FBSType.UINT: "int",
        FBSType.FLOAT: "float",
        FBSType.LONG: "long",
        FBSType.ULONG: "long",
        FBSType.DOUBLE: "double",
        FBSType.STRING: "String",
        FBSType.STRUCT: "interface",
        FBSType.TABLE: "interface",
        FBSType.UNION: "interface",
        FBSType.VECTOR: "interface",
        FBSType.ENUM: "interface",
    }
