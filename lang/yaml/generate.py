from functools import partial

from flattools.fbs.fbs import FBSType
from lang.common import get_type, pre_generate_step

YAML_TEMPLATE = "fbs_template_yaml.yaml.j2"


def generate_yaml(path, tree, template=YAML_TEMPLATE):
    (prefix, env) = pre_generate_step(path)
    out_file = prefix + ".yaml"
    setattr(tree, "FBSType", FBSType)
    with open(out_file, "w") as target:
        setattr(tree, "yaml_types", FBSType._VALUES_TO_NAMES_LOWER)
        setattr(
            tree, "get_type", partial(get_type, primitive=tree.yaml_types, module=tree)
        )
        target.write(env.get_template(template).render(tree.__dict__))
