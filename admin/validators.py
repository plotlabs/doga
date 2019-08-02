import keyword
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
    column_name_list = []
    for column in schema_list:
        if column["name"] == "":
            valid = False
            msg = "Column name cannot be empty."
            break
        if column["name"] in column_name_list:
            valid = False
            msg = "Columns cannot have same name."
            break
        if column["type"].split("(")[0] not in column_types():
            valid = False
            msg = "Invalid column type for column " + column["name"]
            break
        if column["foreign_key"] != "":
            if not check_table(column["foreign_key"], connection_name):
                valid = False
                msg = "The Foreign Key module does not exist."
                break
        if column["type"].lower().startswith("string"):
            if "(" not in column["type"] and ")" not in column["type"]:
                valid = False
                msg = "String column requires size."
                break
        if column["name"] in keyword.kwlist:
            valid = False
            msg = "Column name cannot be a default keyword."
            break
        column_name_list.append(column["name"])

    return valid, msg
