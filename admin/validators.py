from sqlalchemy import types

from admin.module_generator import check_table


def column_types():
    """Get a list of all possible column types"""
    type_list = filter(lambda t: not (
            t[0:1] == "_" or
            t.endswith(("type", "TYPE", "Type", "instance")) or
            t.startswith(("Type", "Unicode", "VARBINARY", "Variant"))
    ), dir(types))
    return list(type_list)


def column_validation(schema_list, connection_name):
    """Validate columns"""
    valid = True
    msg = ""
    for column in schema_list:
        if column["type"].split("(")[0] not in column_types():
            valid = False
            msg = "Invalid column type for column " + column["name"]
        if column["foreign_key"] != "":
            if not check_table(column["foreign_key"], connection_name):
                valid = False
                msg = "The Foreign Key module does not exist."

    return valid, msg
