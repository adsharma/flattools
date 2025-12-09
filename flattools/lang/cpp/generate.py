from functools import partial

from flattools.fbs.fbs import FBSType
from flattools.lang.common import get_type, pre_generate_step
from flattools.lang.cpp.types import FBSCppType

CPP_TEMPLATE = "fbs_template_cpp.h.j2"


def generate_cpp(path, tree, template=CPP_TEMPLATE):
    (prefix, env) = pre_generate_step(path)
    out_file = prefix + "_generated.h"
    setattr(tree, "FBSType", FBSType)
    with open(out_file, "w") as target:
        setattr(tree, "cpp_types", FBSCppType._VALUES_TO_CPP_TYPES)
        setattr(
            tree, "get_type", partial(get_type, primitive=tree.cpp_types, module=tree)
        )
        target.write(env.get_template(template).render(tree.__dict__))
