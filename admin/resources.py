import re

from datetime import datetime as dt

import subprocess
from threading import Thread

from typing import Dict, Tuple

from flask import Blueprint, request, jsonify, redirect, url_for
from flask_restful import Api, Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from sqlalchemy.exc import UnsupportedCompilationError

from admin.models import Admin, Deployments
from admin.models.table_model import Table as TableModel
from admin.models.database_model import Database as DatabaseObject
from admin.models.email_notifications import EmailNotify
from admin.models.sms_notifications import SmsNotify

from admin.utils import *
from admin.validators import (
    column_types,
    column_validation,
    nullable_check,
    foreign_key_options,
    relationship_validation,
)

from admin.resource_forms import *

from admin.export.exportapp import (
    check_if_exist, )
from admin.admin_forms import *
from admin.resource_helper import *

from app.utils import AlchemyEncoder, verify_jwt

from templates.models import metadata

mod_admin = Blueprint(
    "admin",
    __name__,
)
api_admin = Api()
api_admin.init_app(mod_admin)


class AdminApi(Resource):
    """
    Defines the responses for the API's to create, verify and retrieve a admin
    information

    ...
    Methods
    -------
        get(self,email):
            Defines responses for the `/admin/admin_profile/<email-id>`
            endpoint

        post(self):
            Defines responses for the `/admin/admin_profile endpoint

    """
    @jwt_required
    def get(self, email=None) -> Tuple[Dict[str, str], int]:
        """
        Defines responses for the `/admin/admin_profile/<email-id>`
        endpoint

        Parameters:
        ----------
        - name:
          in: path
          type: string
          format: email
          required: true
          description: e-mail address corresponding to the admin user, of
                       which data is being retrieved.

        Returns:
        -------
            json serializable dict, integer response code

            responses:
                - 200
                  description: Admin successfully found.
                  body:
                    type: json
                  schema:
                    - name:
                      type: string
                      description: Name registered against the e-mail.
                    - email:
                      type: string
                      format: email
                      description: email passed in the url parameter
                    - id
                      type: integer
                    - create_dt
                      type: string
                      format: datetime YYYY-MM-DD HH:MM:SS.SSS
                - 400
                  description: Error occurred
                  schema:
                    - result:
                      type: string
                - 401
                  description: Invalid JWT token.
                - 500:
                  description: Server Error
        """
        if not verify_jwt(get_jwt_identity(), Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )

        if email is None:
            return {"result": "Please add admin`email` parameter to path"}, 400

        # access the Admin db defined for the app instance
        admin = Admin.query.filter_by(email=email).first()
        if admin is not None:
            user_obj = json.dumps(admin, cls=AlchemyEncoder)
            return {"result": json.loads(user_obj)}, 200

        return {"result": "Admin does not exist."}, 400


class ContentType(Resource):
    """
    Defines the responses for the API's to create, verify and retrieve a admin
    information

    ...
    Methods
    -------
        get(self,email):
            Defines responses for the `/admin/content/types` &
            `/admin/content/types/db_name/content endpoint used to list all
            content or content that matches the parameters given in path

        post(self):
            Defines responses for the `/admin/content/types` endpoint used to
            add content to the app

        put(self):
            Defines responses for the `/admin/content

        delete

    """
    @jwt_required
    def get(self, db_name=None, content_type=None):
        """
        Defines responses for the `/admin/content/types` &
        `/admin/content/types/db_name/content endpoint used to list all
        content or content that matches the parameters given in path

        Returns:
            json serializable dict
            integer response code
        """
        if not verify_jwt(get_jwt_identity(), Admin):
            return {
                "result": "JWT authorization invalid, user does not exist."
            }
        table_list = []
        app_table_columns = {}
        # Iterate though the tables stored using FlaskSqlAlchemy
        for table_ in metadata.sorted_tables:
            # if content is not specified then return a list of all tables in
            # if content_type has not been specified in the URL path
            current_db = extract_database_name(table_.info["bind_key"])

            if content_type is None:
                if table_.name in ["alembic_version"]:
                    continue

                if (table_.name in [
                        "jwt", "admin", "restricted_by_jwt", "deployments",
                        "relationships", "assets_table", "notifications"
                ] and table_.info["bind_key"] == "default"):
                    continue

                if "generatedAssociation" in table_.name:
                    continue

                column_list = []

                if db_name is not None and db_name != current_db:
                    continue

                for column_ in table_.columns:
                    foreign_col = ""
                    if column_.name in ["id", "create_dt"]:
                        continue
                    default = str(column_.default)
                    if column_.server_default is not None:
                        default = column_.server_default.arg
                    try:
                        column_type = str(column_.type)
                    except UnsupportedCompilationError as error:
                        if "JSON" in "".join(error.args).upper():
                            column_type = "JSON"
                        else:
                            raise ValueError("Cannot infer column type.")
                    foreign_key = str(column_.foreign_keys)
                    if foreign_key != set():
                        foreign_key = foreign_key[foreign_key.find("(") +
                                                  1:foreign_key.
                                                  find(")")].replace("'", "")
                    try:
                        default = int(str(default))
                    except ValueError:
                        pass
                    if column_type == "BOOLEAN":
                        default = str(default)

                    if column_type == "BLOB":
                        model_path = ("/".join(
                            os.path.dirname(__file__).split("/")[:-1]) +
                                      "/app/" + table_.info["bind_key"] + "/" +
                                      table_.name + "/models.py")
                        models = open(model_path, "r").read()
                        if "ImageType" in models:
                            column_type = "ImageType"

                    if "ColumnDefault" in str(default):
                        default = default[default.find("(") +
                                          1:default.find(")")].replace(
                                              "'", "")

                    col = {
                        "name": column_.name,
                        "type": column_type,
                        "nullable": str(bool(column_.nullable)).lower(),
                        "unique": str(bool(column_.unique)).lower(),
                        "default": default,
                        "foreign_key": foreign_key,
                    }
                    column_list.append(col)

                app_name = table_.info["bind_key"]
                try:
                    app_table_columns[app_name][table_.name] = column_list
                except KeyError:
                    app_table_columns[app_name] = {table_.name: column_list}

                table_list = app_table_columns

            else:
                if table_.name in ["alembic_version"]:
                    continue

                current_db = extract_database_name(table_.info["bind_key"])

                if table_.name == content_type and db_name == current_db:
                    column_list = []
                    for column_ in table_.columns:
                        if column_.name in ["id", "create_dt"]:
                            continue
                        default = str(column_.default)
                        if column_.default is not None:
                            default = default[default.find("(") +
                                              1:default.find(")")].replace(
                                                  "'", "")
                        try:
                            column_type = str(column_.type)
                        except UnsupportedCompilationError as error:
                            if "JSON" in "".join(error.args).upper():
                                column_type = "JSON"
                            else:
                                raise ValueError("Cannot infer column type.")
                        foreign_key = str(column_.foreign_keys)
                        if column_.foreign_keys != "":
                            foreign_key = foreign_key[foreign_key.find("(") +
                                                      1:foreign_key.
                                                      find(")")].replace(
                                                          "'", "")
                            if foreign_key != "":
                                foreign_key = foreign_key.split(".")[0].title()
                        if foreign_key != "":
                            column_type = str(column_.foreign_keys).split(
                                "}")[0][1:]  # noqa 501

                        if column_type == "BLOB":
                            model_path = ("/".join(
                                os.path.dirname(__file__).split("/")[:-1]) +
                                          " /app/" + table_.info["bind_key"] +
                                          "/" + table_.name + "/models.py")
                            models = open(model_path, "rb").read()
                            if "ImageType" in models:
                                column_type = "ImageType"

                        obj = {
                            "name": column_.name,
                            "type": column_type,
                            "nullable": str(bool(column_.nullable)).lower(),
                            "unique": str(bool(column_.unique)).lower(),
                            "default": default,
                            "foreign_key": foreign_key,
                        }
                        column_list.append(obj)
                    table_list.append({
                        "table_name":
                        table_.name,
                        "connection_name":
                        table_.info["bind_key"],
                        "columns":
                        column_list,
                    })

        if not table_list:
            empty_apps = set(DB_DICT.keys())
            empty_apps = empty_apps - {"default"}
            if empty_apps != {}:
                table_list = {}
                for application in list(empty_apps):
                    table_list[application] = {}
            if not table_list:
                return {"result": "No apps and content created yet."}, 200

        for bind_key, _ in table_list.items():
            jwt_base = JWT.query.filter_by(connection_name=bind_key).first()
            if jwt_base is not None:
                table_list[bind_key]["jwt_info"] = {
                    "base_table": jwt_base.table,
                    "filter_keys": jwt_base.filter_keys.split(","),
                }

                restricted_tables = RestrictedByJWT.query.filter_by(
                    connection_name=bind_key).first()

                if restricted_tables is not None:
                    table_list[bind_key]["jwt_info"][
                        "restricted_tables"] = restricted_tables.restricted_tables.split(
                            ",")

        empty_apps = set(DB_DICT.keys()) - set(table_list.keys())
        empty_apps = empty_apps - {"default"}
        if empty_apps != {}:
            for application in list(empty_apps):
                table_list[application] = {}
        return jsonify(table_list)
        # return {"result": table_list}

    @jwt_required
    def post(self):
        """
        Defines responses for the POST `/admin/content/types` that adds content
        to the app.

        Returns:
            json serializable dict
            integer response code

        """
        admin_jwt = get_jwt_identity()
        if not verify_jwt(admin_jwt, Admin):
            return {
                "result": "JWT authorization invalid, user does not exist."
            }
        data = request.get_json()
        # sample data
        # data = {
        #     "table_name": "user",
        #     "connection_name": "default",
        #     "columns": [
        #         {
        #             "name": "name",
        #             "type": "String(32, 'utf8mb4_unicode_ci')",
        #             "nullable": "False",
        #             "unique": "True",
        #             "default": "value",
        #             "foreign_key": ""
        #         },
        #         {
        #             "name": "desc",
        #             "type": "String(1024, 'utf8mb4_unicode_ci')",
        #             "nullable": "False",
        #             "unique": "False",
        #             "default": "value",
        #             "foreign_key": ""
        #         },
        #         {
        #             "name": "teacher_id",
        #             "type": "ForeignKey('teacher.id)",
        #             "nullable": "False",
        #             "unique": "False",
        #             "default": "", (For no value)
        #             "foreign_key": "Teacher"
        #         },
        #     ]
        # }

        if data is None:
            return {"response": "JSON body cannot be empty."}, 500

        required_keys = {"table_name", "app_name", "columns"}

        ColumnForm(request.form)

        notification = Notifications(
            user=admin_jwt["email"],
            app_name=data["app_name"],
            action_status="INITIATED",
            action_type="create-content-tables",
            message="Request Processing",
        )

        missed_keys = required_keys.difference(data)
        if len(missed_keys) != 0:
            notification.action_status = "ERROR"
            notification.completed_action_at = dt.now()
            db.session.add(notification)
            db.session.commit()
            triggerSocketioNotif(admin_jwt["email"],
                                 notification.create_dict())
            return (
                {
                    "result": "Values for fields cannot be null.",
                    "required values": list(missed_keys),
                },
                500,
            )

        data["connection_name"] = data["app_name"].lower()
        try:
            table_ = TableModel.from_dict(request.get_json())
        except ValueError as err:
            return {"result": "Error: " + "".join(err.args)}, 400

        base_jwt = data.get("base_jwt", False)
        restrict_by_jwt = data.get("restrict_by_jwt", False)

        if check_table(table_.table_name):
            db.session.add(notification)
            db.session.commit()
            return {"result": "Module with this name is already present."}, 400
        if (table_.table_name in ["admin", "jwt", "restricted_by_jwt"]
                and table_.connection_name == "default"):
            return (
                {
                    "result":
                    "table_ with name {} is not allowed since it "
                    "is used to manage admin login"
                    " internally.".format(table_.table_name)
                },
                400,
            )

        try:
            valid, msg, data["columns"] = relationship_validation(
                data["columns"], table_.connection_name)
        except KeyError as err:
            return (
                {
                    "result": "Error, relationship definition incomplete." +
                    " Please add required property.",
                    "property": err.args,
                },
                500,
            )

        if valid is False:
            return {"result": msg}, 400

        try:
            valid, msg = column_validation(data["columns"],
                                           table_.connection_name)
        except KeyError as err:
            return (
                {
                    "result": "Error, column is missing required property.",
                    "property": err.args,
                },
                500,
            )
        if valid is False:
            return {"result": msg}, 400

        if base_jwt and restrict_by_jwt:
            return (
                {
                    "response":
                    "Table_cannot be both jwt_base and "
                    "restricted by jwt."
                },
                400,
            )

        if base_jwt is True:

            if check_jwt_present(table_.connection_name):
                return (
                    {
                        "result":
                        "Only one table_ is allowed to set jwt per"
                        "database connection."
                    },
                    400,
                )

            if (data.get("filter_keys") is None
                    or len(data.get("filter_keys", [])) == 0):
                data["filter_keys"] = ["id"]

            if (validate_filter_keys_names(data["filter_keys"],
                                           data["columns"]) is False):
                return (
                    {
                        "result":
                        "Only column names are allowed"
                        " in filter keys."
                    },
                    400,
                )

            if (validate_filter_keys_jwt(data["filter_keys"], data["columns"])
                    is False):
                return (
                    {
                        "result":
                        "At least one of the filter_keys"
                        " should be unique and not null."
                    },
                    400,
                )

            msg, valid, data["expiry"] = set_expiry(data.get("expiry", {}))

            if valid is False:
                return {"result": msg}, 400

            set_jwt_flag(
                table_.connection_name,
                table_.table_name,
                ",".join(data["filter_keys"]),
            )

        if (restrict_by_jwt
                and check_jwt_present(table_.connection_name) is None):
            return {"result": "JWT is not configured."}, 400

        Thread(target=create_contet_thread(data, admin_jwt, table_, base_jwt,
                                           restrict_by_jwt,
                                           notification)).start()
        return {"result": "Successfully created module."}, 200

    @jwt_required
    def put(self):
        """Edit a content type"""
        data = request.get_json()
        # sample data
        # data = {
        #     "table_name": "user",
        #     "connection_name": "default",
        #     "columns": [
        #         {
        #             "name": "name",
        #             "type": "String(32, 'utf8mb4_unicode_ci')",
        #             "nullable": "False",
        #             "unique": "True",
        #             "default": "value",
        #             "foreign_key": ""
        #         },
        #         {
        #             "name": "desc",
        #             "type": "String(1024, 'utf8mb4_unicode_ci')",
        #             "nullable": "False",
        #             "unique": "False",
        #             "default": "", (For no value)
        #             "foreign_key": ""
        #         }
        #     ]
        # }

        if data is None:
            return {"result": "JSON body cannot be empty."}

        if not verify_jwt(get_jwt_identity(), Admin):
            return {
                "result": "JWT authorization invalid, user does not exist."
            }
        try:
            data["connection_name"] = data["app_name"]
            table_ = TableModel.from_dict(data)

        except ValueError as err:
            return {"result": "Error: " + "".join(err.args)}, 400
        except KeyError as err:
            return {"result": "Error: " + "".join(err.args)}, 400

        database_name = extract_database_name(table_.connection_name)
        base_jwt = data.get("base_jwt", False)
        restrict_by_jwt = data.get("restrict_by_jwt", False)

        if base_jwt and restrict_by_jwt:
            return (
                {
                    "result:"
                    "Module cannot be both base_jwt and"
                    " restricted_by_jwt."
                },
                400,
            )

        if not check_table(table_.table_name, table_.connection_name):
            return (
                {
                    "result":
                    "Module with this name not present. Please "
                    "choose an existing one to edit."
                },
                400,
            )

        valid, msg = column_validation(data["columns"], table_.connection_name)
        if valid is False:
            return {"result": msg}, 400

        # check if the table that will be edited is the JWT restricted table
        is_jwt = JWT.query.filter_by(connection_name=table_.connection_name,
                                     table=table_.table_name).first()

        if is_jwt is None and base_jwt is True:
            return (
                {
                    "result":
                    "Only one table is allowed to set jwt per"
                    "database connection."
                },
                400,
            )

        associated_tables = RestrictedByJWT.query.filter_by(
            connection_name=table_.connection_name).first()

        if is_jwt is not None and base_jwt == False:  # noqa 711
            # regenerate all the endpoints that previously required JWT
            for table_assoc in associated_tables.restricted_tables.split(","):
                dir_path = "app/" + database_name + "/" + \
                           table_assoc.table_name
                create_model(dir_path, data)
                create_resources(
                    database_name + "." + table_assoc.table_name,
                    table.connection_name,
                    dir_path,
                    base_jwt,
                    data.get("expiry", {}),
                    restrict_by_jwt,
                    data.get("filter_keys", []),
                )

                # delete this entry from the jwt table
                delete_jwt(table_.connection_name)
                delete_restricted_by_jwt(table_.connection_name)

        check = nullable_check(data)
        if check:
            return (
                {
                    "result":
                    "Since data is already present in the table, "
                    "new datetime column should be nullable."
                },
                400,
            )

        if restrict_by_jwt:
            add_jwt_list(table_.connection_name, table_.table_name)

        if base_jwt:

            if (data.get("filter_keys") is None
                    or len(data.get("filter_keys", [])) == 0):
                data["filter_keys"] = ["id"]

            if (validate_filter_keys_names(data["filter_keys"],
                                           data["columns"]) is False):
                return (
                    {
                        "result":
                        "Only column names are allowed"
                        " in filter keys."
                    },
                    400,
                )

            if (validate_filter_keys_jwt(data["filter_keys"], data["columns"])
                    is False):
                return (
                    {
                        "result":
                        "At least one of the filter_keys"
                        " should be unique and not null."
                    },
                    400,
                )

            msg, valid, data["expiry"] = set_expiry(data.get("expiry", {}))

            if valid is False:
                return {"result": msg}, 400

            delete_jwt(table_.connection_name)
            set_jwt_flag(
                table_.connection_name,
                table_.table_name,
                ",".join(data["filter_keys"]),
            )

        if (restrict_by_jwt
                and check_jwt_present(table_.connection_name) is None):
            return {"result": "JWT is not configured."}, 400

        dir_path = "app/" + database_name + "/" + table_.table_name
        create_model(dir_path, data)
        create_resources(
            database_name + "." + table_.table_name,
            table_.connection_name,
            dir_path,
            base_jwt,
            data.get("expiry", {}),
            restrict_by_jwt,
            data.get("filter_keys", []),
        )

        remove_alembic_versions()
        move_migration_files()
        return {"result": "Successfully edited model."}, 200

    @jwt_required
    def delete(self, db_name, content_type):
        """Delete a content type"""
        if not verify_jwt(get_jwt_identity(), Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )
        tables_list = []
        for table_ in metadata.sorted_tables:
            f = table_.__dict__["foreign_keys"]
            db_ = extract_database_name(table_.info["bind_key"])
            for s in f:
                table_name = s.column.table
                if str(table_name) == content_type.lower() and db_name == db_:
                    tables_list.append(table_.name)

        if len(tables_list) > 0:
            return (
                {
                    "result":
                    "The table {} is linked to another table(s). "
                    "Delete table(s) {} "
                    "first.".format(content_type, ", ".join(tables_list))
                },
                400,
            )

        try:
            shutil.rmtree("app/" + db_name.lower() + "/" +
                          content_type.lower())
        except FileNotFoundError:
            return {"result": "Module does not exist."}, 400

        with open("app/blueprints.py", "r") as f:
            lines = f.readlines()
        with open("app/blueprints.py", "w") as f:
            for line in lines:
                if (line.strip("\n") != "from app." + db_name + "." +
                        content_type + ".resources import mod_model"
                        and line.strip("\n") !=
                        "app.register_blueprint(mod_model, url_prefix='/" +
                        db_name.lower() + "/" + content_type.lower() + "')"):
                    f.write(line)
        remove_alembic_versions()
        move_migration_files()
        return {"result": "Successfully deleted module."}, 200


class ColumnRelations(Resource):
    """
    Defines the responses to identify tables to create relationships with
    """
    @jwt_required
    def post(self):
        if not verify_jwt(get_jwt_identity(), Admin):
            return {
                "result": "JWT authorization invalid, user does not exist."
            }

        data = request.get_json()

        if data is None:
            return {"response": "JSON body cannot be empty."}, 500

        required_keys = {"app_name", "type"}

        missed_keys = required_keys.difference(data)
        if len(missed_keys) != 0:
            return (
                {
                    "result": "Values for fields cannot be null.",
                    "required values": list(missed_keys),
                },
                500,
            )

        try:
            result = foreign_key_options(data["app_name"], data["type"])

        except ValueError:
            return (
                {
                    "result":
                    "Error while fetching app data, make sure there"
                    "is a connection for the app."
                },
                500,
            )

        return result, 200


class DatabaseInit(Resource):
    @jwt_required
    def get(self):
        """Get properties of all connections"""
        if not verify_jwt(get_jwt_identity(), Admin):
            return {
                "result": "JWT authorization invalid, user does not exist."
            }
        connection_list = []
        for key, value in DB_DICT.items():
            if value.startswith("sqlite"):
                database_name = value.split("/")[-1].rstrip(".db")
                database_type = "sqlite"
                host = "local"
                port = None
                username = None
                password = None
            elif value.startswith("mysql"):
                database_name = value.split("/")[-1].split("?")[0]
                database_type = "mysql"
                host = value.split("@")[-1].split("/")[0].split(":")[0]
                port = value.split("@")[-1].split("/")[0].split(":")[1]
                username = value.split("@")[0].split("/")[-1].split(":")[0]
                password = value.split("@")[0].split("/")[-1].split(":")[1]
            elif value.startswith("postgresql"):
                database_name = value.split("/")[-1]
                database_type = "postgresql"
                host = value.split("@")[-1].split("/")[0].split(":")[0]
                port = value.split("@")[-1].split("/")[0].split(":")[1]
                username = value.split("@")[0].split("/")[-1].split(":")[0]
                password = value.split("@")[0].split("/")[-1].split(":")[1]

            connection_list.append({
                "connection_name": key,
                "database_type": database_type,
                "database_name": database_name,
                "host": host,
                "port": port,
                "username": username,
                "password": password,
            })

        return connection_list, 200

    @jwt_required
    def post(self):
        """Create a database connection string"""
        # sample data
        # data = {
        #     "database_type": "mysql/sqlite/postgresql",
        #     "connection_name": "db1",
        #     "username": "user",
        #     "password": "pass",
        #     "host": "localhost",
        #     "port": "port_number"
        #     "database_name": "database_name",
        # }
        if not verify_jwt(get_jwt_identity(), Admin):
            return {
                "result": "JWT authorization invalid, user does not exist."
            }

        form = DatabaseCreation(request.form)

        required_keys = {
            "database_type",
            "username",
            "password",
            "database_name",
        }

        try:
            database = DatabaseObject.from_dict({
                "database_name":
                form.app_name.data,
                "connection_name":
                form.app_name.data,
                "database_type":
                form.database_type.data,
                "host":
                form.host.data,
                "port":
                form.port.data,
                "username":
                form.username.data,
                "password":
                form.password.data,
            })

        except ValueError as err:
            return {"result": "Error: " + "".join(err.args)}, 400

        database_string = database.db_string()

        if database_string == "":
            return (
                {
                    "result":
                    "Please provide all parameters to connect/create"
                    " db instance."
                },
                500,
            )

        try:
            engine = create_engine(database_string)
            conn = engine.connect()
            conn.invalidate()
            engine.dispose()
            db_created = ""
        except OperationalError as err:
            if ("unknown database" or database.database_name + "does not exist"
                    in str(err).lower()):
                try:
                    database_string = re.split(database.database_name,
                                               database_string)[0]
                    engine = create_engine(database_string)
                    conn = engine.connect()
                    conn.execute("commit")
                    conn.execute("CREATE DATABASE " + database.database_name)
                    conn.invalidate()
                    engine.dispose()
                    db_created = (" New database " + database.database_name +
                                  " created.")
                except OperationalError:
                    return (
                        {
                            "result":
                            "Could not create database,"
                            " connection not valid."
                        },
                        400,
                    )
            else:
                return (
                    {
                        "result": "The database credentials are not valid."
                    },
                    400,
                )

        with open("dbs.py", "r") as f:
            lines = f.readlines()

        with open("dbs.py", "w+") as f:
            for i, line in enumerate(lines):
                if line.startswith("}"):
                    line = ('    "' + database.connection_name + '": "' +
                            database.db_string() + '",\n' + line)
                f.write(line)

        add_new_db(database.database_name)

        return redirect(url_for("admin.contenttypes", app=database.name))

    @jwt_required
    def put(self):
        """Edit a database connection string"""
        data = request.get_json()
        # sample data
        # data = {
        #     "type": "mysql/mongo/postgresql",
        #     "username": "user",
        #     "password": "pass",
        #     "host": "localhost",
        #     "database_name": "database_name",
        # }

        if not verify_jwt(get_jwt_identity(), Admin):
            return {
                "result": "JWT authorization invalid, user does not exist."
            }

        data["connection_name"] = data["database_name"].lower()

        if data["connection_name"] not in DB_DICT:
            return (
                {
                    "result":
                    "No connection with name: {} is present.".format(
                        data["connection_name"])
                },
                400,
            )

        db_type = DB_DICT[data["connection_name"]].split(":")[0]
        try:
            db_type = db_type.split("+")[0]
        except KeyError:
            pass

        if db_type != data["database_type"]:
            return (
                {
                    "result":
                    "The type of database string cannot be "
                    "changed. Create a new connection or choose the "
                    "correct type."
                },
                400,
            )

        # check if content exists in old or new database:
        old_db = extract_database_name(data["connection_name"].lower())
        new_db = data["database_name"]

        path = "app/" + old_db

        try:
            if len(os.listdir(path)) != 0:
                # str(len(os.listdir(path))/2)
                return (
                    {
                        "result":
                        "Found  content in the old database"
                        " connection"
                        " please remove them first."
                    },
                    400,
                )

        except FileNotFoundError:
            pass

        database_string = ""
        if data["database_type"] == "mysql":
            database_string = \
                "mysql://{}:{}@{}:3306/{}?charset=utf8mb4".format(
                data["username"],
                data["password"],
                data["host"],
                data["database_name"],
            )

        if data["database_type"] == "postgresql":
            database_string = "postgresql+psycopg2://{}:{}@{}/{}".format(
                data["username"],
                data["password"],
                data["host"],
                data["database_name"],
            )

        if data["database_type"] == "sqlite":
            database_string = "sqlite:////tmp/{}.db".format(
                data["database_name"])

        try:
            engine = create_engine(database_string)
            conn = engine.connect()
            conn.invalidate()
            engine.dispose()
        except OperationalError:
            return {"result": "The database credentials are not valid."}, 400

        with open("dbs.py", "r") as f:
            lines = f.readlines()

        with open("dbs.py", "w") as f:
            for i, line in enumerate(lines):
                if line.startswith('    "' + data["connection_name"].lower()):
                    line = line.replace(
                        line,
                        '    "' + data["connection_name"] + '": "' +
                        database_string + '",\n',
                    )
                f.write(line)

        remove_alembic_versions()
        move_migration_files()
        return (
            {
                "result": "Successfully edited database connection string."
            },
            200,
        )


class ExportApp(Resource):
    """
    Endpoint that deals with deployment of the app to different platforms
    """
    @jwt_required
    def post(self, platform):

        if not verify_jwt(get_jwt_identity(), Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                400,
            )

        json_request = request.get_json()
        if json_request is None:
            return {"result": "Request body cannot be empty"}, 400
        missing_keys = {}

        try:
            app_name = json_request["app_name"]
        except KeyError as error:
            missing_keys["app_name"] = list(error.args)[0]

        try:
            check_if_exist(app_name)
        except DogaAppNotFound as error:
            return (
                {
                    "result": "Given app " + app_name + " doesn't exit.",
                    "request": request.get_json(),
                },
                500,
            )

        if platform == "aws":
            admin_jwt = get_jwt_identity()
            notification = Notifications(
                user=admin_jwt["email"],
                app_name=json_request["app_name"],
                action_type="deploy-app",
                action_status="INITIATED",
                message="AWS Export",
            )
            db.session.add(notification)
            db.session.commit()
            triggerSocketioNotif(admin_jwt["email"],
                                 notification.create_dict())
            try:
                user_credentials = create_user_credentials(
                    **json_request["user_credentials"])
                missing_keys["user_credentials"] = []
            except KeyError as error:
                missing_keys["user_credentials"] = list(error.args)[0]

            required_rds_keys = {
                "MasterUsername",
                "MasterUserPassword",
                "DBInstanceIdentifier",
                "MaxAllocatedStorage",
                "AllocatedStorage",
            }
            required_ec2_keys = {
                "BlockDeviceMappings",
                "ImageId",
                "InstanceType",
            }

            missing_keys["ec2_config"] = list(
                required_ec2_keys.difference(
                    json_request["ec2_config"].keys()))
            missing_keys["rds_config"] = list(
                required_rds_keys.difference(
                    json_request["rds_config"].keys()))

            if (missing_keys["user_credentials"] != []
                    or missing_keys["ec2_config"] != []
                    or missing_keys["rds_config"] != []):

                notification.action_status = "ERROR"
                notification.completed_action_at = dt.now()
                notification.message = ("Cannot process export missing "
                                        "parameters: " + missing_keys)
                db.session.add(notification)
                db.session.commit()
                triggerSocketioNotif(admin_jwt["email"],
                                     notification.create_dict())

                return (
                    {
                        "result": "Please Provide the following details: ",
                        "required fields": missing_keys,
                        "request": json_request,
                    },
                    500,
                )

            try:
                config = create_aws_config(**json_request["config"])
            except ValueError as error:
                notification.action_status = "ERROR"
                notification.completed_action_at = dt.now()
                notification.message = str(error)
                db.session.add(notification)
                db.session.commit()
                triggerSocketioNotif(admin_jwt["email"],
                                     notification.create_dict())
                return (
                    {
                        "result": "Error creating config",
                        "error": str(error),
                        "request": request.get_json(),
                    },
                    400,
                )

            Thread(
                target=create_aws_deployment_thread,
                kwargs={
                    "user_credentials": user_credentials,
                    "config": config,
                    "app_name": app_name,
                    "json_request": json_request,
                    "notification": notification,
                    "admin_jwt": admin_jwt,
                    "platform": platform,
                },
            ).start()
            return (
                {
                    "result": "Registered export request to " + platform + "."
                },
                200,
            )
        elif platform == "heroku":

            try:
                provision_db = json_request["provision_db"]
            except KeyError as error:
                missing_keys["provision_db"] = list(error.args)[0]

            deploy = json_request.get("provision_db", True)

            if deploy is True:
                try:
                    tier = json_request["tier"]
                except KeyError as error:
                    missing_keys["tier"] = list(error.args)[0]

            if len(missing_keys) != 0:
                return (
                    {
                        "result": "Please Provide the following details: ",
                        "required fields": missing_keys,
                        "request": json_request,
                    },
                    400,
                )

            # TO create the app json file for heroku
            app_json = {
                "name": "DOGA created deployment for " + app_name,
                "description": "App: " + app_name + " with in Python"
                " using Flask",
                "repository": "",
                "keywords": ["python", "flask", "DOGA"],
            }

            try:
                create_app_dir(app_name,
                               rds=None,
                               user_credentials=None,
                               config=None,
                               platform=platform,
                               **{"deploy_db": deploy})
            except DogaHerokuDeploymentError as error:
                return (
                    {
                        "response": "Could not create app for Heroku.",
                        "error": str(error),
                        "request": json_request,
                    },
                    400,
                )

            file_location = os.sep.join(__file__.split(os.sep)[:-1])

            random_string = create_random_string(4)
            app_deployed = app_name + "-" + random_string
            # needs to start with a letter, end with a letter or digit and can
            # only contain lowercase letters, digits and dashes.
            app_deployed = app_deployed.replace("_", "-")

            if deploy:
                db_name = "pgsql" + app_name + random_string
                subprocess.call([
                    "sh",
                    file_location + "/export/heroku_postgres.sh",
                    app_deployed.lower(),
                    db_name.lower(),
                    tier,
                ])

            else:
                subprocess.call([
                    "sh",
                    file_location + "/export/heroku_deploy.sh",
                    app_deployed.lower(),
                ])

            app_info = subprocess.Popen(
                ["heroku", "apps:info", "-a",
                 app_deployed.lower()],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            out, err = app_info.communicate()

            url_regex = "(https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9" "-]+[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9]+\\.[^\\s]{2,}|www\\.[a-zA-Z0-9]+\\.[^\\s]{2,})"  # noqa 401
            deployment_url = re.findall(url_regex, str(out))[1]
            deployment_url = deployment_url.split(".com")[0] + '.com/'
            write_to_deployments(app_name, platform, deployment_url)
            return {"response": "heroku app deployed."}, 200

        elif platform == "local":
            if len(missing_keys) != 0:
                return (
                    {
                        "result": "Please Provide the following details: ",
                        "required fields": missing_keys,
                        "request": json_request,
                    },
                    400,
                )

            try:
                check_if_exist(app_name)
            except DogaAppNotFound as error:
                return (
                    {
                        "result": "Given app " + app_name + " doesn't exit.",
                        "request": request.get_json(),
                    },
                    400,
                )

            try:
                path = json_request["path"]
            except KeyError as err:
                path = None

            create_app_dir(app_name,
                           rds=None,
                           user_credentials="none",
                           config=None,
                           platform="local",
                           **{"path": path})

        if platform == "local":
            if path is None:
                path = "/".join(__file__.split("/")[:-2]) + "/exported_app/"

            write_to_deployments(app_name, platform, None)
            return (
                {
                    "result":
                    "App exported & to " + platform + " at " + path + "."
                },
                200,
            )

        return (
            {
                "result": "Registered export request to " + platform + "."
            },
            200,
        )


class CreateNotifications(Resource):
    """
    Endpoint that Creates a script to send notifications
    """
    @jwt_required
    def post(self, platform):

        if not verify_jwt(get_jwt_identity(), Admin):
            return {
                "result": "JWT authorization invalid, user does not exist."
            }

        json_request = request.get_json()
        if json_request is None:
            return {"result": "Request body cannot be empty"}

        if platform.lower() == "email":
            email_obj = EmailNotify.from_dict(json_request)

            result, code = email_obj.return_result()

            return dict(result, **{"request": json_request}), code

        elif platform.lower() == "sms":
            sms_obj = SmsNotify.from_dict(json_request)

            result, code = sms_obj.return_result()

            return dict(result, **{"request": json_request}), code

        else:
            return (
                {
                    "response":
                    "Currently we only create scripts for SMS "
                    "notifications though Twilio and E-mail though"
                    " SendGrid."
                },
                400,
            )


api_admin.add_resource(AdminApi, "/admin_profile",
                       "/admin_profile/<string:email>")
api_admin.add_resource(DatabaseInit, "/dbinit",
                       "/dbinit/types/<string:content_type>")
api_admin.add_resource(
    ContentType,
    "/content/types",
    "/content/types/<string:db_name>/<string:content_type>",
)
api_admin.add_resource(ColumnRelations, "/content/relations")
api_admin.add_resource(ExportApp, "/export/<string:platform>")
api_admin.add_resource(CreateNotifications, "/notify/<string:platform>")
