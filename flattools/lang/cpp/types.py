from flattools.fbs.fbs import FBSType


class FBSCppType(FBSType):
    _VALUES_TO_CPP_TYPES = {
        FBSType.BOOL: "bool",
        FBSType.BYTE: "char",
        FBSType.UBYTE: "uchar",
        FBSType.SHORT: "short",
        FBSType.USHORT: "ushort",
        FBSType.INT: "int64_t",
        FBSType.UINT: "uint64_t",
        FBSType.FLOAT: "float",
        FBSType.LONG: "int64_t",
        FBSType.ULONG: "uint64_t",
        FBSType.DOUBLE: "double",
        FBSType.STRING: "std::string",
        FBSType.STRUCT: "struct",
        FBSType.TABLE: "struct",
        FBSType.UNION: "union",
        FBSType.VECTOR: "vector_t",
        FBSType.ENUM: "enum",
    }
