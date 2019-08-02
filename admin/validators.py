import keyword
import requests
import json
from sqlalchemy import types
from templates.models import metadata

from admin.module_generator import check_table


def column_types():
    """Get a list of all possible column types"""
    type_list = filter(lambda t: not (
            t[0:1] == "_" or
            t.endswith(("type", "TYPE", "Type", "instance")) or
            t.startswith(("Type", "Unicode", "VARBINARY", "Variant"))
    ), dir(types))
    return list(type_list)


def column_validation(schema_list, connection_name, table_columns = None):
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
        if table_columns:
            if column["name"] not in table_columns:
                if column["type"] in ["Date", "DATETIME"] \
                        and column["nullable"] == "False":
                    valid = False
                    break
        column_name_list.append(column["name"])

    return valid, msg


def nullable_check(data):
    for table in metadata.sorted_tables:
        if table.name == data['table_name']:
            valid, msg = column_validation(data["columns"],
                              data['connection_name'], table.columns)
            if valid is False:
                model_data = requests.get('http://localhost:8080/' + data[
                    'table_name'])
                if len(json.loads(model_data.content)["result"]) != 0:
                    return True
                else:
                    return False

    return False
