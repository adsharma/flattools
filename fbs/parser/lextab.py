# lextab.py. This file automatically created by PLY (version 3.4). Don't edit!
_tabversion = "3.4"
_lextokens = {
    "SHORT": 1,
    "BOOLCONSTANT": 1,
    "USHORT": 1,
    "UBYTE": 1,
    "DUBCONSTANT": 1,
    "FILE_IDENTIFIER": 1,
    "ULONG": 1,
    "FILE_EXTENSION": 1,
    "LONG": 1,
    "UNION": 1,
    "TABLE": 1,
    "IDENTIFIER": 1,
    "STRING": 1,
    "INTCONSTANT": 1,
    "ENUM": 1,
    "NAMESPACE": 1,
    "LITERAL": 1,
    "UINT": 1,
    "BYTE": 1,
    "INCLUDE": 1,
    "STRUCT": 1,
    "ROOT_TYPE": 1,
    "INT": 1,
    "ATTRIBUTE": 1,
    "FLOAT": 1,
    "BOOL": 1,
    "DOUBLE": 1,
}
_lexreflags = 0
_lexliterals = ":;,=*{}()<>[]"
_lexstateinfo = {"INITIAL": "inclusive"}
_lexstatere = {
    "INITIAL": [
        (
            "(?P<t_newline>\\n+)|(?P<t_ignore_SILLYCOMM>\\/\\*\\**\\*\\/)|(?P<t_ignore_MULTICOMM>\\/\\*[^*]\\/*([^*/]|[^*]\\/|\\*[^/])*\\**\\*\\/)|(?P<t_ignore_DOCTEXT>\\/\\*\\*([^*/]|[^*]\\/|\\*[^/])*\\**\\*\\/)|(?P<t_BOOLCONSTANT>\\btrue\\b|\\bfalse\\b)|(?P<t_DUBCONSTANT>-?\\d+\\.\\d*(e-?\\d+)?)|(?P<t_HEXCONSTANT>0x[0-9A-Fa-f]+)|(?P<t_INTCONSTANT>[+-]?[0-9]+)|(?P<t_LITERAL>(\\\"([^\\\\\\n]|(\\\\.))*?\\\")|\\'([^\\\\\\n]|(\\\\.))*?\\')|(?P<t_IDENTIFIER>[a-zA-Z_](\\.[a-zA-Z_0-9]|[a-zA-Z_0-9])*)|(?P<t_ignore_COMMENT>\\/\\/[^\\n]*)|(?P<t_ignore_UNIXCOMMENT>\\#[^\\n]*)",
            [
                None,
                ("t_newline", "newline"),
                ("t_ignore_SILLYCOMM", "ignore_SILLYCOMM"),
                ("t_ignore_MULTICOMM", "ignore_MULTICOMM"),
                None,
                ("t_ignore_DOCTEXT", "ignore_DOCTEXT"),
                None,
                ("t_BOOLCONSTANT", "BOOLCONSTANT"),
                ("t_DUBCONSTANT", "DUBCONSTANT"),
                None,
                ("t_HEXCONSTANT", "HEXCONSTANT"),
                ("t_INTCONSTANT", "INTCONSTANT"),
                ("t_LITERAL", "LITERAL"),
                None,
                None,
                None,
                None,
                None,
                ("t_IDENTIFIER", "IDENTIFIER"),
                None,
                (None, None),
                (None, None),
            ],
        )
    ]
}
_lexstateignore = {"INITIAL": " \t\r"}
_lexstateerrorf = {"INITIAL": "t_error"}
