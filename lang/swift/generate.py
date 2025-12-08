import os
import re
from functools import partial
from keyword import kwlist
from typing import List, Tuple

from flattools.fbs.fbs import FBSType
from lang.common import (
    _NAMESPACE_TO_TYPE,
    get_bases,
    get_module_name,
    get_type,
    lookup_fbs_type,
    parse_types,
    pre_generate_step,
    pre_process_module,
)
from lang.swift.types import FBSSwiftType

SWIFT_TEMPLATE = "fbs_template.swift.j2"

SWIFT_KWLIST = {}


def camel_case(text: str) -> str:
    return "".join([x.title() for x in text.split("_")])


def generate_swift(path, tree, templates=[SWIFT_TEMPLATE, None, None], separate=False):
    (prefix, env) = pre_generate_step(path)
    if not os.path.exists(prefix):
        os.mkdir(prefix)
    table_template, union_template, enum_template = templates
    setattr(tree, "module", tree)
    pre_process_module(tree, SWIFT_KWLIST)
    # Type related methods
    setattr(tree, "FBSType", FBSType)
    setattr(tree, "swift_types", FBSSwiftType._VALUES_TO_SWIFT_TYPES)
    setattr(
        tree, "get_type", partial(get_type, primitive=tree.swift_types, module=tree)
    )
    setattr(tree, "get_module_name", partial(get_module_name, module=tree))
    setattr(tree, "lookup_fbs_type", lookup_fbs_type)
    setattr(tree, "parse_types", parse_types)
    setattr(tree, "get_bases", partial(get_bases, module=tree))
    # Strings
    setattr(tree, "camel_case", camel_case)
    setattr(tree, "swift_reserved", SWIFT_KWLIST)
    if not separate:
        _, filename = os.path.split(path)
        swift_filename = os.path.splitext(filename)[0] + ".swift"
        out_file = os.path.join(prefix, swift_filename)
        with open(out_file, "w") as target:
            target.write(env.get_template(table_template).render(tree.__dict__))
        return
    for table in tree.__fbs_meta__["tables"]:
        out_file = os.path.join(prefix, table.__name__ + ".swift")
        with open(out_file, "w") as target:
            setattr(tree, "table", table)
            target.write(env.get_template(table_template).render(tree.__dict__))
    for fbs_union in tree.__fbs_meta__["unions"]:
        out_file = os.path.join(prefix, fbs_union.__name__ + ".swift")
        with open(out_file, "w") as target:
            setattr(tree, "fbs_union", fbs_union)
            target.write(env.get_template(union_template).render(tree.__dict__))
    for fbs_enum in tree.__fbs_meta__["enums"]:
        out_file = os.path.join(prefix, fbs_enum.__name__ + ".swift")
        with open(out_file, "w") as target:
            setattr(tree, "fbs_enum", fbs_enum)
            target.write(env.get_template(enum_template).render(tree.__dict__))
