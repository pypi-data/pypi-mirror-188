"""
Methods related with dicts management
"""


def clean_dict(data_dict: dict) -> dict:
    """
    Delete key from a dict where value is None

    Example:
    clean_dict({"id": "123", "field": None}) -> {"id": "123"}

    :param data_dict: dictionary to clean

    :return: dictionary with cleaned key-values

    """
    return_dict: dict = dict()
    for key, value in data_dict.items():
        if value:
            return_dict[key] = value

    return return_dict


def merge_dicts(*args: dict) -> dict:
    """
    Merges several dictionaries in one.

    Example:
    dic1 = {"a": 1, "b": 2}
    dic2 = {"b": 3, "c": 4}
    merge_dicts(dic1, dic2) -> {"a": 1, "b": 3, "c": 4}

    :param args: dictionaries to be merged

    :return: a new dictionary with the previous dictionaries merged
    """
    new_dict = dict()

    for d in args:
        new_dict.update(d)

    return new_dict
