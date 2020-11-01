import datetime
import json
import keyword
import requests


from sqlalchemy import types
from templates.models import metadata

from dbs import DB_DICT
from admin.module_generator import check_table
from config import HOST, PORT


def column_types():
    """Get a list of all possible column types"""
    type_list = filter(lambda t: not (
        t[0:1] == "_" or
        t.endswith(("type", "TYPE", "Type", "instance")) or
        t.startswith(("Type", "Unicode", "VARBINARY", "Variant"))
    ), dir(types))
    return list(type_list)


def column_validation(schema_list, connection_name, table_columns=None):
    """Validate columns"""
    valid = True
    msg = ""
    column_name_list = []
    for column in schema_list:
        if column["name"] in column_name_list:
            valid = False
            msg = "Columns cannot have same name."
            break
        if column["type"].split("(")[0] not in column_types():
            valid = False
            msg = "Invalid column type for column {}.".format(
                column["name"])
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
        if column["type"].upper() in ['TEXT'] and \
            DB_DICT[connection_name].startswith("mysql") and \
                column["unique"] == 'True':
            valid = False
            msg = "Unique constraint on TEXT column type is not" \
                " allowed for mysql database."
            break
        if column["name"] in keyword.kwlist:
            valid = False
            msg = "Column name cannot be a default keyword."
            break
        if column["default"]:
            if column["type"].upper() in ['INTEGER', 'BIGINTEGER', 'BIGINT',
                                          'FLOAT', 'INT', 'SMALLINT',
                                          'NUMERIC', 'SMALLINTEGER',
                                          'DECIMAL', 'REAL']:
                if isinstance(column["default"], str):
                    valid = False
                    msg = "The default value entered for column {} is string" \
                          " and not of type {}.".format(column["name"],
                                                        column["type"])
                    break

            if column["type"].upper() in ['DATE']:
                try:
                    date_val = datetime.datetime.strptime(column["default"],
                                                          "%Y-%m-%d")
                except ValueError:
                    valid = False
                    msg = "The format entered for column {} is not correct. " \
                          "Correct format should be of type: " \
                          "YYYY-MM-DD.".format(column["name"])
                    break
                except TypeError:
                    valid = False
                    msg = "The format entered for column {} is not correct. " \
                          "Correct format should be of type: " \
                          "YYYY-MM-DD.".format(column["name"])
                    break

            if column["type"].upper() in ['DATETIME']:
                try:
                    if column["default"].lower() != "current":
                        date_val = datetime.datetime.strptime(
                            column["default"], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    valid = False
                    msg = "The format entered for column {} is not correct. " \
                          "Correct format should be of type: " \
                          "YYYY-MM-DD H:M:S.".format(column["name"])
                    break
                except TypeError:
                    valid = False
                    msg = "The format entered for column {} is not correct. " \
                          "Correct format should be of type: " \
                          "YYYY-MM-DD H:M:S.".format(column["name"])
                    break

            if column["type"].upper() == "BOOLEAN":
                if connection_name == "default":
                    valid = False
                    msg = "{} datatype for columns is not supported by " \
                        "default database connection.".format(column["type"])
                    break
                if column["default"] not in ['1', '0', 'true', 'false']:
                    valid = False
                    msg = "The default value entered for column {} is not of" \
                          " type {}.".format(column["name"], column["type"])
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
                                           data['connection_name'],
                                           table.columns)
            if valid is False:
                model_data = requests.get('http://{}:'.format(HOST) + PORT
                                          + '/' + data['table_name'])
                if len(json.loads(model_data.content)["result"]) != 0:
                    return True

                return False

    return False
