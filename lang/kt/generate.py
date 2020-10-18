import os
import re
from functools import partial
from keyword import kwlist
from typing import List, Tuple

from fbs.fbs import FBSType
from lang.common import (
    _NAMESPACE_TO_TYPE,
    get_module_name,
    get_type,
    lookup_fbs_type,
    parse_types,
    pre_generate_step,
)
from lang.kt.types import FBSKotlinType

KOTLIN_TEMPLATE = "fbs_template.kt.j2"

# https://kotlinlang.org/docs/reference/grammar.html#identifiers
KT_KWLIST = {
    "abstract",
    "annotation",
    "by",
    "catch",
    "companion",
    "constructor",
    "crossinline",
    "data",
    "dynamic",
    "enum",
    "external",
    "final",
    "finally",
    "import",
    "infix",
    "init",
    "inline",
    "inner",
    "internal",
    "lateinit",
    "noinline",
    "open",
    "operator",
    "out",
    "override",
    "private",
    "protected",
    "public",
    "reified",
    "sealed",
    "tailrec",
    "vararg",
    "where",
    "get",
    "set",
    "field",
    "property",
    "receiver",
    "param",
    "setparam",
    "delegate",
    "file",
    "expect",
    "actual",
    "const",
    "suspend",
}


def camel_case(text: str) -> str:
    return "".join([x.title() for x in text.split("_")])


def generate_kt(
    path, tree, templates=[KOTLIN_TEMPLATE, KOTLIN_TEMPLATE, KOTLIN_TEMPLATE]
):
    (prefix, env) = pre_generate_step(path)
    if not os.path.exists(prefix):
        os.mkdir(prefix)
    table_template, union_template, enum_template = templates
    setattr(tree, "module", tree)
    # Type related methods
    setattr(tree, "FBSType", FBSType)
    setattr(tree, "kotlin_types", FBSKotlinType._VALUES_TO_KT_TYPES)
    setattr(
        tree, "get_type", partial(get_type, primitive=tree.kotlin_types, module=tree)
    )
    setattr(tree, "get_module_name", partial(get_module_name, module=tree))
    setattr(tree, "lookup_fbs_type", lookup_fbs_type)
    setattr(tree, "parse_types", parse_types)
    # Strings
    setattr(tree, "camel_case", camel_case)
    setattr(tree, "kotlin_reserved", KT_KWLIST)
    # Python specific
    for table in tree.__fbs_meta__["tables"]:
        out_file = os.path.join(prefix, table.__name__ + ".kt")
        with open(out_file, "w") as target:
            setattr(tree, "table", table)
            target.write(env.get_template(table_template).render(tree.__dict__))
    for fbs_union in tree.__fbs_meta__["unions"]:
        out_file = os.path.join(prefix, fbs_union.__name__ + ".kt")
        with open(out_file, "w") as target:
            setattr(tree, "fbs_union", fbs_union)
            target.write(env.get_template(union_template).render(tree.__dict__))
    for fbs_enum in tree.__fbs_meta__["enums"]:
        out_file = os.path.join(prefix, fbs_enum.__name__ + ".kt")
        with open(out_file, "w") as target:
            setattr(tree, "fbs_enum", fbs_enum)
            target.write(env.get_template(enum_template).render(tree.__dict__))
