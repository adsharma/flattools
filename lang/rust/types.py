from flattools.fbs.fbs import FBSType


class FBSRustType(FBSType):
    _VALUES_TO_RUST_TYPES = {
        FBSType.BOOL: "bool",
        FBSType.BYTE: "i8",
        FBSType.UBYTE: "u8",
        FBSType.SHORT: "i16",
        FBSType.USHORT: "u16",
        FBSType.INT: "i32",
        FBSType.UINT: "u32",
        FBSType.FLOAT: "f32",
        FBSType.LONG: "i64",
        FBSType.ULONG: "u64",
        FBSType.DOUBLE: "f64",
        FBSType.STRING: "String",
        FBSType.STRUCT: "interface",
        FBSType.TABLE: "interface",
        FBSType.UNION: "interface",
        FBSType.VECTOR: "interface",
        FBSType.ENUM: "enum",
    }


def optionalize(primitive):
    return f"Option<{primitive}>"
