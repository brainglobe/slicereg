

def split_keyvalue_string(anchoring, sep1="&", sep2="="):
    """
    Returns a dict from a string with seperated keyvalue pairs with one separator and the pair with another separator

    Example:
        >>> split_keyvalue_string("a=3&b=6", "&", "=")
        {'a': 3., 'b': 6.}
    """
    return {(kv := pair.split(sep2))[0]: float(kv[1]) for pair in anchoring.split(sep1)}
