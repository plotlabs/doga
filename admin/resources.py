import json

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from templates.models import metadata
from app.utils import AlchemyEncoder
from admin.module_generator import *
from admin.models import Admin
from admin.validators import column_types, column_validation, nullable_check
from dbs import DB_DICT
from passlib.handlers.sha2_crypt import sha512_crypt
from admin.utils import *

ALGORITHM = sha512_crypt

mod_admin = Blueprint("admin", __name__)
api_admin = Api()
api_admin.init_app(mod_admin)


class AdminApi(Resource):
    """APIs to create a admin and return admin info if a admin exists"""

    def get(self, email):
        admin = Admin.query.filter_by(email=email).first()
        if admin is not None:
            user_obj = json.dumps(admin, cls=AlchemyEncoder)
            return {"result": json.loads(user_obj)}
        else:
            return {"result": "Admin does not exist."}, 404

    def post(self):
        data = request.get_json()
        admin_exists = Admin.query.filter_by(email=data["email"].lower(
        )).first()
        if admin_exists is None:
            try:
                password_hash = ALGORITHM.hash(data["password"])
                admin = Admin(email=data["email"].lower(),
                              password=password_hash, name=data["name"],
                              create_dt=datetime.datetime.utcnow())
                db.session.add(admin)
                db.session.commit()
                return {"result": "Admin created successfully.",
                        "id": admin.id, "email": admin.email}
            except KeyError as e:
                return {"result": "Key error", "error": str(e)}, 500
        else:
            return {"result": "Admin already exists."}, 500


class Login(Resource):
    """API to login admin."""

    def post(self):
        data = request.get_json()
        try:
            admin = Admin.query.filter_by(email=data["email"]).first()
            if admin is None:
                return {"result": "Admin does not exist."}, 401
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

    def get(self, content_type=None):
        """Get a list of all the content types"""
        table_list = []
        for table in metadata.sorted_tables:
            if content_type is None:
                if table.name in ["alembic_version", "admin"]:
                    continue

                objs = []
                for c in table.columns:
                    if c.name in ['id', 'create_dt']:
                        continue
                    default = str(c.default)
                    if c.default is not None:
                        default = default[
                            default.find("(") + 1:default.find(")")
                        ].replace("'", "")
                    c_type = str(c.type)
                    foreign_key = str(c.foreign_keys)
                    if c.foreign_keys != "":
                        foreign_key = foreign_key[
                            foreign_key.find("(") + 1:foreign_key.find(")")
                        ].replace("'", "")
                        if foreign_key != "":
                            foreign_key = foreign_key.split(".")[0].title()
                    if foreign_key != "":
                        c_type = str(c.foreign_keys).split("}")[0][1:]
                    obj = {
                        "name": c.name,
                        "type": c_type,
                        "nullable": str(bool(c.nullable)).lower(),
                        "unique": str(bool(c.unique)).lower(),
                        "default": default,
                        "foreign_key": foreign_key
                    }
                    objs.append(obj)
                table_list.append({'table_name': table.name,
                                   'connection_name': table.info[
                                       'bind_key'], 'columns': objs})
            else:
                if table.name in ["alembic_version", "admin"]:
                    continue

                if table.name == content_type:
                    objs = []
                    for c in table.columns:
                        if c.name in ['id', 'create_dt']:
                            continue
                        default = str(c.default)
                        if c.default is not None:
                            default = default[
                                default.find("(") + 1:default.find(")")
                            ].replace("'", "")
                        c_type = str(c.type)
                        foreign_key = str(c.foreign_keys)
                        if c.foreign_keys != "":
                            foreign_key = foreign_key[
                                foreign_key.find(
                                    "(") + 1:foreign_key.find(")")
                            ].replace("'", "")
                            if foreign_key != "":
                                foreign_key = foreign_key.split(".")[0].title()
                        if foreign_key != "":
                            c_type = str(c.foreign_keys).split("}")[0][1:]
                        obj = {
                            "name": c.name,
                            "type": c_type,
                            "nullable": str(bool(c.nullable)).lower(),
                            "unique": str(bool(c.unique)).lower(),
                            "default": default,
                            "foreign_key": foreign_key
                        }
                        objs.append(obj)
                    table_list.append({'table_name': table.name,
                                       'connection_name': table.info[
                                           'bind_key'], 'columns': objs})

        return jsonify(table_list)
        # return {"result": table_list}

    def post(self):
        """Create a content type"""
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
        if "connection_name" in data:
            if data['connection_name'] not in DB_DICT:
                return {
                    "result": "The database connection given does not exist."
                }, 400

        data["table_name"] = data["table_name"].lower()

        if len(data["columns"]) == 0:
            return {"result": "At least one column is required"}, 400

        if check_table(data["table_name"]):
            return {"result": "Module with this name is already present."}, 400

        if data["table_name"] == "admin":
            return {"result": "Table with name Admin not allowed since it is "
                              "used to manage admin login internally"}, 400

        valid, msg = column_validation(data["columns"],
                                       data['connection_name'])
        if valid is False:
            return {"result": msg}, 400

        data["database_name"] = extract_database_name(data["connection_name"])

        data["jwt_required"] = data.get("jwt_required", False)
        if data["jwt_required"] is True:

            if check_jwt_present(
                    data["connection_name"], data["database_name"]):
                return {"result": "Only one table is allowed to set jwt per"
                        "database connection"}, 400

            if (data.get("filter_keys") is None or
                    len(data.get("filter_keys", [])) == 0):
                data["filter_keys"] = ["id"]

            if validate_filter_keys_names(
                    data["filter_keys"], data["columns"]) is False:
                return {"result": "Only column names are allowed"
                        " in filter keys"}, 400

            if validate_filter_keys_jwt(
                    data["filter_keys"], data["columns"]) is False:
                return {"result": "Atleast one of the filter_keys"
                        " should be unique and not null"}, 400

            msg, valid, data["expiry"] = set_expiry(data.get("expiry", {}))

            if valid is False:
                return {"result": msg}, 400

            set_jwt_flag(data["connection_name"],
                         data["database_name"], data["table_name"])
            set_jwt_secret_key()

        data["jwt_restricted"] = data.get("jwt_restricted", False)
        if (data["jwt_restricted"] is True and
                (check_jwt_present(data["connection_name"],
                                   data["database_name"]) is None)):
            return {"result": "Jwt not configured"}, 400

        dir_path = create_dir(data["table_name"])
        create_model(dir_path, data)
        create_resources(data["table_name"], dir_path,
                         data["jwt_required"],
                         data.get("expiry", {}),
                         data["jwt_restricted"],
                         data.get("filter_keys", []))
        append_blueprint(data["table_name"])
        remove_alembic_versions()
        move_migration_files()
        migrate()
        return {"result": "Successfully created module"}

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
        if "connection_name" in data:
            if data['connection_name'] not in DB_DICT:
                return {
                    "result": "The database connection given does not exist."
                }, 400

        if len(data["columns"]) == 0:
            return {"result": "At least one column is required"}, 400

        data["table_name"] = data["table_name"].lower()

        if not check_table(data["table_name"]):
            return {
                "result": "Module with this name is already present."
            }, 400

        valid, msg = column_validation(data["columns"],
                                       data['connection_name'])
        if valid is False:
            return {"result": msg}, 400

        check = nullable_check(data)
        if check:
            return {"result": "Since data is already present in the table, "
                              "new datetime column should be nullable."}, 400

        dir_path = 'app/' + data["table_name"]
        create_model(dir_path, data)
        remove_alembic_versions()
        move_migration_files()
        migrate()
        return {"result": "Successfully edited model"}

    def delete(self, content_type):
        """Delete a content type"""
        tables_list = []
        for table in metadata.sorted_tables:
            f = (table.__dict__['foreign_keys'])
            for s in f:
                table_name = s.column.table
                if str(table_name) == content_type.lower():
                    tables_list.append(table.name)

        if len(tables_list) > 0:
            return {
                "result": "The table {} is linked to another table(s). "
                          "Delete table(s) {} first.".format(
                              content_type, ', '.join(tables_list))
            }, 400

        try:
            shutil.rmtree('app/' + content_type.lower())
        except FileNotFoundError:
            return {"result": "Module does not exist."}, 400

        with open("app/blueprints.py", "r") as f:
            lines = f.readlines()
        with open("app/blueprints.py", "w") as f:
            for line in lines:
                if line.strip("\n") != "from app." + content_type \
                        + ".resources import mod_model" and line.strip("\n") \
                        != "app.register_blueprint(mod_model, url_prefix='/" \
                        + content_type.lower() + "')":
                    f.write(line)
        remove_alembic_versions()
        move_migration_files()
        migrate()
        return {"result": "Successfully deleted module"}


class DatabaseInit(Resource):

    def get(self):
        """Get properties of all connections"""
        connection_list = []
        for key, value in DB_DICT.items():
            if value.startswith("sqlite"):
                database_name = value.split("/")[-1]
                database_type = "sqlite"
                host = ""
                username = ""
                password = ""
            elif value.startswith("mysql"):
                database_name = value.split("/")[-1].split("?")[0]
                database_type = "mysql"
                host = value.split("@")[1].split(":")[0]
                username = value.split("@")[0].split("/")[-1].split(":")[0]
                password = value.split("@")[0].split("/")[-1].split(":")[1]
            elif value.startswith("postgresql"):
                database_name = value.split("/")[-1]
                database_type = "postgresql"
                host = value.split("@")[-1].split("/")[0]
                username = value.split("@")[0].split("/")[-1].split(":")[0]
                password = value.split("@")[0].split("/")[-1].split(":")[1]

            connection_list.append({
                "connection_name": key,
                "database_type": database_type,
                "database_name": database_name,
                "host": host,
                "username": username,
                "password": password
            })

        return connection_list

    def post(self):
        """Create a database connection string"""
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
        if data['connection_name'] in DB_DICT:
            return {
                "result": "Connection with name: {} is already present. Use "
                          "a different name.".format(data['connection_name'])
            }, 400

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
                if line.startswith('}'):
                    line = '    "' + data['connection_name'] + '": "' + string\
                        + '",\n' + line
                f.write(line)

        add_new_db(data['connection_name'])

        return {
            "result": "Successfully created database connection string"
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
        migrate()
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
                       '/content/types/<string:content_type>')
api_admin.add_resource(DatabaseInit, '/dbinit/',
                       '/dbinit/types/<string:content_type>')
api_admin.add_resource(ColumnType, '/columntypes')
