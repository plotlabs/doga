import datetime
import json
import keyword
import requests


from sqlalchemy import types
from sqlalchemy import create_engine, MetaData
from sqlalchemy.pool import StaticPool
from templates.models import metadata

from dbs import DB_DICT

from admin.module_generator import check_column
from admin.utils import extract_database_name
from admin.export.utils import extract_engine_or_fail

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
    column_name_list = [column["name"].lower() for column in schema_list]
    for column in schema_list:
        column["name"] = column["name"].lower()
        if len(set(column_name_list)) < len(column_name_list):
            valid = False
            msg = "Columns cannot have same name."
            break
        if column["type"].split("(")[0] not in column_types():
            valid = False
            msg = "Invalid column type for column {}.".format(
                column["name"])
            break
        try:
            if column["foreign_key"] != "":
                try:
                    table_name = column["foreign_key"].split(".")[0]
                    column_name = column["foreign_key"].split(".")[1]
                except IndexError:
                    valid = False
                    msg = "Please format the foreign key in the correct ' \
                          'format 'TableName.ColumnName' . "
                    break
                try:
                    if not check_column(table_name, column_name,
                                        column["type"].split("(")[0],
                                        connection_name):
                        valid = False
                        msg = "Foreign Key Module " + \
                            column["name"] + " does not" + " exist."
                        break
                except TypeError as err:
                    valid = False
                    msg = str(err.args)
        except KeyError:
            column["foreign_key"] = ""

        if column["type"].lower().startswith("string"):
            if "(" not in column["type"] and ")" not in column["type"]:
                valid = False
                msg = "String column requires size."
                break
        if column["type"].upper() in ['TEXT'] and \
            DB_DICT[connection_name].startswith("mysql") and \
                str(column["unique"]).upper() == 'TRUE':
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

            # engine specific issues:
            engine = extract_engine_or_fail(connection_name)

            if engine == 'mysql':
                # MySQLdb._exceptions.OperationalError 1101
                # BLOB, TEXT, GEOMETRY or JSON column can't have a default
                if column['type'].upper() in ['BLOB', 'TEXT', 'GEOMETRY',
                                              'JSON'] and \
                        column['default'] is not None:
                    valid = False
                    msg = "Cannot set a default value for column {} of" \
                          " type {}.".format(column["name"], column["type"])
                    break

        if table_columns:
            if column["name"] not in table_columns:
                if column["type"] in ["Date", "DATETIME"] \
                        and column["nullable"] == "False":
                    valid = False
                    break

    return valid, msg


def nullable_check(data):
    for table in metadata.sorted_tables:
        if table.name == data['table_name']:
            valid, msg = column_validation(data["columns"],
                                           data['app_name'],
                                           table.columns)
            if valid is False:
                model_data = requests.get('http://{}:'.format(HOST) + PORT
                                          + '/' + data['table_name'])
                if len(json.loads(model_data.content)["result"]) != 0:
                    return True

                return False

    return False


def foreign_key_options(app_name, _type):

    result = {}
    for table in metadata.sorted_tables:
        if app_name == extract_database_name(table.info['bind_key']):
            for column in table.columns:
                if _type in str(column.type) or \
                        str(column.type) in _type.upper():
                    try:
                        result[table.name].append(column.name)
                    except KeyError:
                        result[table.name] = [column.name]
    if result != {}:
        return result
    raise ValueError
