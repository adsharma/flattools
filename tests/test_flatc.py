# TODO: Duplicate code
# Figure out how to import from flatc.py
def get_attrs_dict(attrs):
    attrs_dict = {x[0]: x[1] for x in attrs if len(x) == 2}
    ret = {x[0]: None for x in attrs}
    ret.update(attrs_dict)
    return ret


def test_attrs_dict():
    assert get_attrs_dict(["a", ["b", 10], "c"]) == {"a": None, "b": 10, "c": None}
