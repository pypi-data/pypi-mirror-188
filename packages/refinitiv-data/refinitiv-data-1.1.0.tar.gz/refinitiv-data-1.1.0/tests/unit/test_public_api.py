import inspect
import json
from functools import lru_cache

SEPARATOR = "   "


def remove_private_and_magick(methods: list) -> list:
    return [i for i in methods if i[0] != "_"]


def extract_instances_from_dict(module, methods_list):
    if "installed_packages" in methods_list:
        methods_list.remove("installed_packages")

    return {i: getattr(module, i) for i in methods_list}


def name_formatter(name, inst, sep=SEPARATOR):
    inst = extract_module_name(inst)
    if " from " in inst:
        inst = inst.split("from")[0]
    elif len(inst) > 200:
        inst = f"{inst[:100]}....."

    name_str = f"{name}{sep}{inst}"

    return name_str


def extract_module_name(inst):
    if (
        (type(inst) is not str)
        and hasattr(inst, "__module__")
        and "class" not in f"{inst}"
    ):
        inst = f"{inst} located in <{inst.__module__}>"
    return f"{inst}"


@lru_cache()
def walker(modd):
    methods = remove_private_and_magick(dir(modd))
    methods = extract_instances_from_dict(modd, methods)

    struct = {"inst": f"{name_formatter('', modd, sep='')}", "resources": methods}
    for i in methods.items():
        if inspect.ismodule(i[1]):
            if "refinitiv.data" in i[1].__spec__.name:
                methods[i[0]] = walker(i[1])
            else:
                methods[i[0]] = f"{name_formatter('', i[1], sep='')} [external]"
        else:
            methods[i[0]] = f"{name_formatter('', i[1], sep='')}"

    return struct


def dict_compare(expected_dict, actual_dict):
    for expected_key, expected_val in expected_dict.items():
        if isinstance(expected_val, dict):
            try:
                dict_compare(expected_val, actual_dict.get(expected_key))
            except AttributeError:
                raise ValueError()
            except ValueError:
                raise Exception(f"{str(expected_val)};{str(expected_dict)};")

    is_equal = expected_dict.keys() == actual_dict.keys()
    assert is_equal, (
        f"These dicts are different:\n"
        f"Expected keys: {expected_dict.keys()}\n"
        f"Actual keys: {actual_dict.keys()}\n"
        f"expected_dict={expected_dict}\n"
        f"actual_dict={actual_dict}"
    )


def test_public_api():
    # given
    import refinitiv.data as rd

    actual_dict = walker(rd)

    # when
    file_path = "./tests/unit/cur_rdp_model.json"
    with open(file_path, "r") as fp:
        expected_dict = json.load(fp)

    # then
    dict_compare(expected_dict, actual_dict)
