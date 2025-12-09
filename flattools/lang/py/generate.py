import os
import re
from functools import partial
from keyword import kwlist
from typing import List, Optional, Tuple

from flattools.fbs.fbs import FBSType
from flattools.lang.common import (
    _NAMESPACE_TO_TYPE,
    get_bases,
    get_module_name,
    get_type,
    lookup_fbs_type,
    parse_types,
    pre_generate_step,
    pre_process_module,
)
from flattools.lang.py.types import FBSPyType, listify, optionalize

PYTHON_TEMPLATE = "fbs_template.py.j2"


def c_int_from_fbs_type(fbs_type: FBSType) -> Optional[str]:
    if fbs_type in FBSType._PRIMITIVE_TYPES:
        py_type = FBSPyType._VALUES_TO_PY_TYPES[fbs_type]
        if re.search(r"int\d", py_type):
            return py_type
    return None


def c_int_types(module) -> List:
    """Figure out what int types need to be imported from ctypes"""
    c_types = []
    for namespace in _NAMESPACE_TO_TYPE.keys():
        for t in module.__fbs_meta__[namespace]:
            if namespace == "unions":
                continue
            if namespace == "enums":
                py_type = c_int_from_fbs_type(t._FBSType)
                if py_type:
                    c_types.append(py_type)
                continue
            for _, mtype in t._fspec.items():
                fbs_type = mtype[1]
                py_type = c_int_from_fbs_type(fbs_type)
                if py_type:
                    c_types.append(py_type)
    return c_types


# Should be compatible with GenTypeBasic() upstream
def py_gen_type(fbs_type) -> str:
    return FBSType._VALUES_TO_PY_C_TYPES[fbs_type]


# Should be compatible with GenMethod() upstream
def py_gen_method(fbs_type) -> str:
    is_primitive = fbs_type in FBSType._PRIMITIVE_TYPES
    if is_primitive:
        return camel_case(py_gen_type(fbs_type))
    elif fbs_type == FBSType.STRUCT:
        return "Struct"
    else:
        return "UOffsetTRelative"


# Similar to, but not compatible with GenGetter() upstream
def py_gen_getter(fbs_type) -> Tuple[str, Tuple]:
    if fbs_type == FBSType.STRING:
        return ("String", ())
    elif fbs_type == FBSType.UNION or fbs_type == FBSType.ENUM:
        return ("Get", ("flatbuffers.number_types.{}Flags".format("Int8"),))
    elif fbs_type == FBSType.VECTOR:
        _, _, _, element_type, _ = parse_types(fbs_type, get_type(fbs_type))
        return (
            "Get",
            (
                "flatbuffers.number_types.{}Flags".format(
                    camel_case(py_gen_type(element_type))
                ),
            ),
        )
    else:
        return (
            "Get",
            (
                "flatbuffers.number_types.{}Flags".format(
                    camel_case(py_gen_type(fbs_type))
                ),
            ),
        )


def camel_case(text: str) -> str:
    return "".join([x.title() for x in text.split("_")])


def generate_py(
    path,
    tree,
    templates=[PYTHON_TEMPLATE, None, None],
    separate=False,
):
    (prefix, env) = pre_generate_step(path)
    if not os.path.exists(prefix):
        os.mkdir(prefix)
        open(os.path.join(prefix, "__init__.py"), "a").close()
    table_template, union_template, enum_template = templates
    setattr(tree, "module", tree)
    pre_process_module(tree, kwlist)
    # Type related methods
    setattr(tree, "FBSType", FBSType)
    setattr(tree, "python_types", FBSPyType._VALUES_TO_PY_TYPES)
    setattr(
        tree, "get_type", partial(get_type, primitive=tree.python_types, optionalize=optionalize, listify=listify, module=tree)
    )
    setattr(tree, "get_module_name", partial(get_module_name, module=tree))
    setattr(tree, "get_bases", partial(get_bases, module=tree))
    setattr(tree, "lookup_fbs_type", lookup_fbs_type)
    setattr(tree, "parse_types", parse_types)
    setattr(tree, "c_int_types", partial(c_int_types, module=tree))
    # Strings
    setattr(tree, "camel_case", camel_case)
    setattr(tree, "python_reserved", kwlist)
    # Python specific
    setattr(tree, "py_gen_type", py_gen_type)
    setattr(tree, "py_gen_method", py_gen_method)
    setattr(tree, "py_gen_getter", py_gen_getter)
    if not separate:
        _, filename = os.path.split(path)
        py_filename = os.path.splitext(filename)[0] + ".py"
        out_file = os.path.join(prefix, py_filename)
        with open(out_file, "w") as target:
            target.write(env.get_template(table_template).render(tree.__dict__))
        return
    for table in tree.__fbs_meta__["tables"]:
        out_file = os.path.join(prefix, table.__name__ + ".py")
        with open(out_file, "w") as target:
            setattr(tree, "table", table)
            target.write(env.get_template(table_template).render(tree.__dict__))
    for fbs_union in tree.__fbs_meta__["unions"]:
        out_file = os.path.join(prefix, fbs_union.__name__ + ".py")
        with open(out_file, "w") as target:
            setattr(tree, "fbs_union", fbs_union)
            target.write(env.get_template(union_template).render(tree.__dict__))
    for fbs_enum in tree.__fbs_meta__["enums"]:
        out_file = os.path.join(prefix, fbs_enum.__name__ + ".py")
        with open(out_file, "w") as target:
            setattr(tree, "fbs_enum", fbs_enum)
            target.write(env.get_template(enum_template).render(tree.__dict__))
