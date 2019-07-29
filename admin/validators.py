from sqlalchemy import types


def column_types():
    """Get a list of all possible column types"""
    type_list = filter(lambda t: not (
            t[0:1] == "_" or
            t.endswith(("type", "TYPE", "Type", "instance")) or
            t.startswith(("Type", "Unicode", "VARBINARY", "Variant"))
    ), dir(types))
    return list(type_list)
