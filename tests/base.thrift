struct Hello {
    1: optional string name,
    2: optional string greet
}

enum Code {
    OK = 0,
    WARNING = 1,
    DANDER = 2,
    ERROR = 3,
    UNKNOWN = 4,
}

typedef list<Code> codelist
typedef map<Code, i64> codemap
typedef set<Code> codeset
typedef i64 timestamp
