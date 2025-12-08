from functools import partial

from flattools.fbs.fbs import FBSType
from lang.common import get_type, pre_generate_step
from lang.java.types import FBSJavaType

IJAVA_TEMPLATE = "fbs_template_interface.java.j2"


def generate_ijava(path, tree, template=IJAVA_TEMPLATE):
    (prefix, env) = pre_generate_step(path)
    out_file = "I" + prefix + ".java"
    setattr(tree, "FBSType", FBSType)
    with open(out_file, "w") as target:
        setattr(tree, "java_types", FBSJavaType._VALUES_TO_JAVA_TYPES)
        setattr(
            tree, "get_type", partial(get_type, primitive=tree.java_types, module=tree)
        )
        target.write(env.get_template(template).render(tree.__dict__))
