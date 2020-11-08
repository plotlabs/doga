import os
import json
import re

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from passlib.handlers.sha2_crypt import sha512_crypt

from admin.module_generator import *

from admin.models import Admin
from admin.models.admin_model import Admin as AdminObject
from admin.models.table_model import Table as TableModel
from admin.models.column_model import Column as ColumnObject
from admin.models.database_model import Database as DatabaseObject


from admin.utils import *
from admin.validators import column_types, column_validation, nullable_check

from app.utils import AlchemyEncoder
from templates.models import metadata

from config import DEFAULT_PORTS
from dbs import DB_DICT

ALGORITHM = sha512_crypt

mod_admin = Blueprint("admin", __name__)
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
            Defines responses for the `/admin/admin_adminprofile/<email-id>`
            endpoint

        post(self):
            Defines responses for the `/admin/admin_adminprofile endpoint

    """

    def get(self, email=None) -> dict:
        """
        Defines responses for the `/admin/admin_adminprofile/<email-id>`
        endpoint

        Returns:
        -------
            json serializeable dict
            integer response code
        """
        if email is None:
            return {"result": "Please add admin`email` parameter to path"}, 404

        # access the Admin db defined for the app instance
        admin = Admin.query.filter_by(email=email).first()
        if admin is not None:
            user_obj = json.dumps(admin, cls=AlchemyEncoder)
            return {"result": json.loads(user_obj)}

        return {"result": "Admin does not exist."}, 404

    def post(self):
        """
        Defines responses for the `/admin/admin_adminprofile/<email-id>`
        endpoint
        It creates a Admin object from the request body it receives,
        checking if all values satisfy the model constraints and then writing
        data to the `amin` database.

        Returns:
        -------
            json serializeable dict
            integer response code
        """

        data = request.get_json()

        try:
            admin = AdminObject.from_dict(request.get_json())
        except ValueError as err:
            return {"result": "Error: ".join(err.args)}

        admin_exists = Admin.query.filter_by(email=admin._email.lower(
        )).first()
        if admin_exists is None:
            password_hash = ALGORITHM.hash(admin._password)
            admin = Admin(email=admin._email.lower(),
                          password=password_hash, name=admin._name,
                          create_dt=datetime.datetime.utcnow())
            db.session.add(admin)
            db.session.commit()
            return {"result": "Admin created successfully.",
                    "id": admin.id, "email": admin.email}

        else:
            return {"result": "Admin already exists."}, 403


class Login(Resource):
    """API to login admin."""
    """
    TODO: generate jwt & return
    """
    def post(self):
        data = request.get_json()
        try:
            admin = Admin.query.filter_by(email=data["email"]).first()
            if admin is None:
                return {"result": "Admin does not exist."}, 404
            else:
                match = ALGORITHM.verify(data["password"], admin.password)
                if not match:
                    return {"result": "Invalid password."}, 401
                else:
                    return {"result": "Successfully logged in", "email":
                            admin.email, "name": admin.name}
        except KeyError as e:
            return {"result": "Key error", "error": str(e)}, 500


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
            Defines responses for the `/admin/cintent

        delete

    """

    def get(self, db_name=None, content_type=None):
        """
        Defines responses for the `/admin/content/types` &
        `/admin/content/types/db_name/content endpoint used to list all
        content or content that matches the parameters given in path

        Returns:
            json serializeable dict
            integer response code
        """
        table_list = []
        # Iterate though the tables stored using FlaskSqlAlchemy
        for table in metadata.sorted_tables:
            # if content is not specified then return a list of all tables in
            # if content_type has not been specified in the URL path
            current_db = extract_database_name(table.info['bind_key'])

            if content_type is None:
                if table.name in ["alembic_version"]:
                    continue

                if table.name in ["jwt", "admin", "restricted_by_jwt"] and \
                        table.info['bind_key'] == "default":
                    continue

                column_list = []

                if db_name is not None and db_name != current_db:
                    continue

                for column in table.columns:
                    if column.name in ['id', 'create_dt']:
                        continue
                    default = str(column.default)
                    if column.default is not None:
                        default = default[
                            default.find("(") + 1:default.find(")")
                        ].replace("'", "")
                    column_type = str(column.type)
                    foreign_key = str(column.foreign_keys)
                    if column.foreign_keys != "":
                        foreign_key = foreign_key[
                            foreign_key.find("(") + 1:foreign_key.find(")")
                        ].replace("'", "")
                        if foreign_key != "":
                            foreign_key = foreign_key.split(".")[0].title()
                    if foreign_key != "":
                        column_type = str(column.foreign_keys).split("}")[0][1:]  # noqa 501
                    # TODO: use Column Model here & write to TableModel
                    col = {
                        "name": column.name,
                        "type": column_type,
                        "nullable": str(bool(column.nullable)).lower(),
                        "unique": str(bool(column.unique)).lower(),
                        "default": default,
                        "foreign_key": foreign_key
                    }
                    column_list.append(col)
                table_list.append({'table_name': table.name,
                                   'connection_name': table.info[
                                       'bind_key'], 'columns': column_list})
            else:
                if table.name in ["alembic_version"]:
                    continue

                current_db = extract_database_name(table.info['bind_key'])

                if table.name == content_type and db_name == current_db:
                    column_list = []
                    for column in table.columns:
                        if column.name in ['id', 'create_dt']:
                            continue
                        default = str(column.default)
                        if column.default is not None:
                            default = default[
                                default.find("(") + 1:default.find(")")
                            ].replace("'", "")
                        column_type = str(column.type)
                        foreign_key = str(column.foreign_keys)
                        if column.foreign_keys != "":
                            foreign_key = foreign_key[
                                foreign_key.find(
                                    "(") + 1:foreign_key.find(")")
                            ].replace("'", "")
                            if foreign_key != "":
                                foreign_key = foreign_key.split(".")[0].title()
                        if foreign_key != "":
                            column_type = str(column.foreign_keys).split("}")[0][1:]  # noqa 501
                        obj = {
                            "name": column.name,
                            "type": column_type,
                            "nullable": str(bool(column.nullable)).lower(),
                            "unique": str(bool(column.unique)).lower(),
                            "default": default,
                            "foreign_key": foreign_key
                        }
                        column_list.append(obj)
                    table_list.append({'table_name': table.name,
                                       'connection_name': table.info[
                                           'bind_key'], 'columns': column_lists
                                       })

        if table_list == []:
            return {"result": "No matching content found."}, 404

        return jsonify(table_list)
        # return {"result": table_list}

    def post(self):
        """
        Defines responses for the POST `/admin/content/types` that adds content
        to the app.

        Returns:
            json serializeable dict
            integer response code

        """
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
        try:
            Table = TableModel.from_dict(request.get_json())
        except ValueError as err:
            return {"result": "Error: " + "".join(err.args)}, 400

        database_name = extract_database_name(data["connection_name"])

        base_jwt = data.get("base_jwt", False)
        restrict_by_jwt = data.get("restrict_by_jwt", False)

        if check_table(Table.table_name):
            return {"result": "Module with this name is already present."}, 400

        if Table.table_name in ["admin", "jwt", "restricted_by_jwt"] and \
                Table.connection_name == "default":
            return {"result": "Table with name {} is not allowed since it "
                              "is used to manage admin login internally."
                              .format(Table.table_name)}, 400

        # TODO: ask if this should be checked too, seems unlikely
        # if Table.table_name == "alembic_version":

        valid, msg = column_validation(data["columns"], Table.connection_name)
        if valid is False:
            return {"result": msg}, 400

        if base_jwt and restrict_by_jwt:
            return {
                "response": "Table cannot be both jwt_base and restricted by "
                "jwt."
            }, 400

        if base_jwt is True:

            if check_jwt_present(Table.connection_name, database_name):
                return {"result": "Only one table is allowed to set jwt per"
                                  "database connection."}, 400

            # TODO: check if the filter keys are valid in TableModel & set
            if (data.get("filter_keys") is None or
                    len(data.get("filter_keys", [])) == 0):
                data["filter_keys"] = ["id"]

            if validate_filter_keys_names(
                    data["filter_keys"], data["columns"]) is False:
                return {"result": "Only column names are allowed"
                                  " in filter keys."}, 400

            if validate_filter_keys_jwt(
                    data["filter_keys"], data["columns"]) is False:
                return {"result": "Atleast one of the filter_keys"
                                  " should be unique and not null."}, 400

            msg, valid, data["expiry"] = set_expiry(data.get("expiry", {}))

            if valid is False:
                return {"result": msg}, 400

            set_jwt_flag(Table.connection_name, database_name, Table.table_name,  # noqa 501
                         ",".join(data["filter_keys"]))
            set_jwt_secret_key()

        if restrict_by_jwt and check_jwt_present(Table.connection_name, database_name) is None:  # noqa 501, 701
            return {"result": "JWT is not configured."}, 400

        dir_path = create_dir(database_name+"/"+Table.table_name)

        isExisting = os.path.isfile(dir_path)

        if isExisting:
            return {"result": "Content must be unique for databases with the"
                    " same name."}

        if restrict_by_jwt:
            add_jwt_list(Table.connection_name, database_name,
                         Table.table_name)

        create_model(dir_path, data)
        create_resources(database_name+"."+Table.table_name,
                         dir_path,
                         base_jwt,
                         data.get("expiry", {}),
                         restrict_by_jwt,
                         data.get("filter_keys", []))
        append_blueprint(database_name+"."+Table.table_name)
        remove_alembic_versions()
        move_migration_files()
        return {"result": "Successfully created module."}

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

        try:
            Table = TableModel.from_dict(request.get_json())
        except ValueError as err:
            return {"result": "Error: " + "".join(err.args)}, 400

        database_name = extract_database_name(Table.connection_name)
        base_jwt = data.get("base_jwt", False)
        restrict_by_jwt = data.get("restrict_by_jwt", False)

        if base_jwt and restrict_by_jwt:
            return {"result:" "Module cannot be both base_jwt and"
                    " restricted_by_jwt."}

        if not check_table(Table.table_name, Table._connection_name):
            return {
                "result": "Module with this name not present. Please choose a"
                " an existing one to edit."
            }, 400

        valid, msg = column_validation(data["columns"],
                                       Table.connection_name)
        if valid is False:
            return {"result": msg}, 400

        # check if the table that will be edited is the JWT restricted table
        isJWT = JWT.query.filter_by(connection_name=Table.connection_name,
                                    database_name=database_name,
                                    table=Table.table_name).first()

        if isJWT is None and base_jwt is True:
            return {"result": "Only one table is allowed to set jwt per"
                              "database connection."}, 400

        associatedTables = Restricted_by_JWT.query.filter_by(
                                connection_name=Table.connection_name)

        if isJWT != None and base_jwt == False:  # noqa 711
            associatedTables = Restricted_by_JWT.query.filter_by(
                                connection_name=Table.connection_name).first()
            # regenerate all the endpoints that previously required JWT
            for table in associatedTables.restricted_tables.split(","):
                dir_path = "app/"+database_name+"/"+Table.table_name
                create_resources(database_name+"."+table,
                                 dir_path,
                                 False,
                                 data.get("expiry", {}),
                                 False,
                                 data.get("filter_keys", []))

            # delete this entry from the jwt table
                delete_jwt(Table.connection_name)
                delete_restricted_by_jwt(Table.connection_name)

        # TODO:
        # add a check for filter keys for jwt & add a function to change the
        # JWT key function

        check = nullable_check(data)
        if check:
            return {"result": "Since data is already present in the table, "
                              "new datetime column should be nullable."}, 400

        if restrict_by_jwt:
            add_jwt_list(Table.connection_name, database_name,
                         Table.table_name)

        if base_jwt:

            if (data.get("filter_keys") is None or
                    len(data.get("filter_keys", [])) == 0):
                data["filter_keys"] = ["id"]

            if validate_filter_keys_names(
                    data["filter_keys"], data["columns"]) is False:
                return {"result": "Only column names are allowed"
                                  " in filter keys."}, 400

            if validate_filter_keys_jwt(
                    data["filter_keys"], data["columns"]) is False:
                return {"result": "Atleast one of the filter_keys"
                                  " should be unique and not null."}, 400

            msg, valid, data["expiry"] = set_expiry(data.get("expiry", {}))

            if valid is False:
                return {"result": msg}, 400

            delete_jwt(Table.connection_name)
            set_jwt_flag(Table.connection_name, database_name, Table.table_name,  # noqa 501
                         ",".join(data["filter_keys"]))
            set_jwt_secret_key()

        if restrict_by_jwt and check_jwt_present(Table.connection_name, database_name) is None:  # noqa 501, 701
            return {"result": "JWT is not configured."}, 400

        dir_path = 'app/' + database_name+"/"+Table.table_name
        create_model(dir_path, data)
        create_resources(database_name+"."+Table.table_name,
                         dir_path,
                         base_jwt,
                         data.get("expiry", {}),
                         restrict_by_jwt,
                         data.get("filter_keys", []))

        remove_alembic_versions()
        move_migration_files()
        # migrate()
        return {"result": "Successfully edited model."}

    def delete(self, db_name, content_type):
        """Delete a content type"""
        tables_list = []
        for table in metadata.sorted_tables:
            f = (table.__dict__['foreign_keys'])
            db = extract_database_name(table.info['bind_key'])
            for s in f:
                table_name = s.column.table
                if str(table_name) == content_type.lower() and db_name == db:
                    tables_list.append(table.name)

        if len(tables_list) > 0:
            return {
                "result": "The table {} is linked to another table(s). "
                          "Delete table(s) {} first.".format(
                              content_type, ', '.join(tables_list))
            }, 400

        try:
            shutil.rmtree('app/'+db_name.lower()+'/'+content_type.lower())
        except FileNotFoundError:
            return {"result": "Module does not exist."}, 400

        with open("app/blueprints.py", "r") as f:
            lines = f.readlines()
        with open("app/blueprints.py", "w") as f:
            for line in lines:
                if line.strip("\n") != "from app."+db_name+"." + content_type \
                        + ".resources import mod_model" and line.strip("\n") \
                        != "app.register_blueprint(mod_model, url_prefix='/" \
                        + db_name.lower()+"/" + content_type.lower() + "')":
                    f.write(line)
        remove_alembic_versions()
        move_migration_files()
        # migrate()
        return {"result": "Successfully deleted module."}


class DatabaseInit(Resource):

    def get(self):
        """Get properties of all connections"""
        connection_list = []
        for key, value in DB_DICT.items():
            if value.startswith("sqlite"):
                database_name = value.split("/")[-1]
                database_type = "sqlite"
                host = ""
                port = ""
                username = ""
                password = ""
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
                "password": password
            })

        return connection_list

    def post(self):
        """Create a database connection string"""
        # sample data
        # data = {
        #     "type": "mysql/mongo/postgresql",
        #     "connection_name": "db1",
        #     "username": "user",
        #     "password": "pass",
        #     "host": "localhost",
        #     "port": "port_number"
        #     "database_name": "database_name",
        # }
        try:
            database = DatabaseObject.from_dict(request.get_json())
        except ValueError as err:
            return {"result": "Error: " + "".join(err.args)}, 400

        string = database.db_string()

        try:
            engine = create_engine(string)
            conn = engine.connect()
            conn.invalidate()
            engine.dispose()
            db_created = ""
        except OperationalError as err:
            if "unknown database" or database.database_name + "does not exist"\
                   in str(err).lower():
                try:
                    string = re.split(database.database_name, string)[0]
                    engine = create_engine(string)
                    conn = engine.connect()
                    conn.execute("commit")
                    conn.execute("CREATE DATABASE " + database.database_name)
                    conn.invalidate()
                    engine.dispose()
                    db_created = " New database " + database.database_name +\
                        " created."
                except OperationalError:
                    return {
                        "result": "Could not create database,"
                        " connection not valid."}, 400
            else:
                return {
                    "result": "The database credentials are not valid."
                    }, 400

        with open('dbs.py', 'r') as f:
            lines = f.readlines()
            f.close()

        with open('dbs.py', 'w+') as f:
            for i, line in enumerate(lines):
                if line.startswith('}'):
                    line = '    "' + database.connection_name + '": "' + \
                        string + '",\n' + line
                f.write(line)
            f.close()

        add_new_db(database.connection_name)

        return {
            "result": "Successfully created database connection string." +
            db_created
        }

    def put(self):
        """Edit a database connection string"""
        data = request.get_json()
        # sample data
        # data = {
        #     "type": "mysql/mongo/postgresql",
        #     "connection_name": "db1",
        #     "username": "user",
        #     "password": "pass",
        #     "host": "localhost",
        #     "database_name": "database_name",
        # }
        if data['connection_name'] not in DB_DICT:
            return {
                "result": "No connection with name: {} is present.".format(
                    data['connection_name'])}, 400

        db_type = DB_DICT[data['connection_name']].split(':')[0]
        try:
            db_type = db_type.split('+')[0]
        except KeyError:
            pass

        if db_type != data['type']:
            return {
                "result": "The type of database string cannot be "
                          "changed. Create a new connection or choose the "
                          "correct type."}, 400

        # check if content exists in old or new database:
        old_db = extract_database_name(data['connection_name'])
        new_db = data['database_name']

        path = 'app/' + old_db
        if len(os.listdir(path)) != 0:
            # str(len(os.listdir(path))/2)
            return {"result": "Found  content in the old database connection"
                    " please remove them first."}

        string = ''
        if data['type'] == 'mysql':
            string = 'mysql://{}:{}@{}:3306/{}?charset=utf8mb4'.format(
                data['username'], data['password'], data['host'],
                data['database_name'])

        if data['type'] == 'postgresql':
            string = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
                data['username'], data['password'], data['host'],
                data['database_name'])

        try:
            engine = create_engine(string)
            conn = engine.connect()
            conn.invalidate()
            engine.dispose()
        except OperationalError:
            return {"result": "The database credentials are not valid."}, 400

        with open('dbs.py', 'r') as f:
            lines = f.readlines()

        with open('dbs.py', 'w') as f:
            for i, line in enumerate(lines):
                if line.startswith('    "' + data['connection_name']):
                    line = line.replace(line, '    "' + data[
                        'connection_name'] + '": "' + string + '",\n')
                f.write(line)

        remove_alembic_versions()
        move_migration_files()
        # migrate()
        return {
            "result": "Successfully edited database connection string."
        }


class ColumnType(Resource):

    def get(self):
        """Get a list of all valid column types available."""
        return {
            "result": column_types()
        }


api_admin.add_resource(AdminApi, '/admin_profile',
                       '/admin_profile/<string:email>')
api_admin.add_resource(Login, '/login')

api_admin.add_resource(ContentType, '/content/types',
                       '/content/types/<string:db_name>/<string:content_type>')
api_admin.add_resource(DatabaseInit, '/dbinit',
                       '/dbinit/types/<string:content_type>')

api_admin.add_resource(ColumnType, '/columntypes')
