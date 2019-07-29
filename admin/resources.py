from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from templates.models import metadata
from admin.module_generator import *
from admin.validators import column_types, column_validation
from dbs import DB_DICT

mod_admin = Blueprint("admin", __name__)
api_admin = Api()
api_admin.init_app(mod_admin)


class ContentType(Resource):

    def get(self, content_type=None):
        """Get a list of all the content types"""
        table_list = []
        for table in metadata.sorted_tables:
            if content_type is None:
                if table.name == "alembic_version":
                    continue

                objs = []
                for c in table.columns:
                    obj = {
                        "name": c.name,
                        "type": str(c.type),
                        "nullable": c.nullable,
                        "unique": c.unique
                    }
                    objs.append(obj)
                table_list.append({'table_name': table.name,
                                   'connection_name': table.info[
                                       'bind_key'], 'columns': objs})
            else:
                if table.name == content_type:
                    objs = []
                    for c in table.columns:
                        obj = {
                            "name": c.name,
                            "type": str(c.type),
                            "nullable": c.nullable,
                            "unique": c.unique
                        }
                        objs.append(obj)
                    table_list.append({'table_name': table.name,
                                       'connection_name': table.info[
                                           'bind_key'], 'columns': objs})

        return jsonify(table_list)

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
        #             "foreign_key": ""
        #         },
        #         {
        #             "name": "desc",
        #             "type": "String(1024, 'utf8mb4_unicode_ci')",
        #             "nullable": "False",
        #             "unique": "False",
        #             "foreign_key": ""
        #         },
        #         {
        #             "name": "teacher_id",
        #             "type": "ForeignKey('teacher.id)",
        #             "nullable": "False",
        #             "unique": "False",
        #             "foreign_key": "Teacher"
        #         },
        #     ]
        # }
        if "connection_name" in data:
            if data['connection_name'] not in DB_DICT:
                return jsonify({
                    "result": "The database connection given does not exist."
                }, 400)

        if check_table(data["table_name"]):
            return jsonify({
                "result": "Module with this name is already present."
            }, 400)

        valid, msg = column_validation(data["columns"], data['connection_name'])
        if valid is False:
            return jsonify({"result": msg}, 400)

        dir_path = create_dir(data["table_name"])
        create_model(dir_path, data)
        create_resources(data["table_name"], dir_path)
        append_blueprint(data["table_name"])
        remove_alembic_versions()
        move_migration_files()
        migrate()
        return jsonify({"result": "Successfully created module"})

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
        #             "foreign_key": ""
        #         },
        #         {
        #             "name": "desc",
        #             "type": "String(1024, 'utf8mb4_unicode_ci')",
        #             "nullable": "False",
        #             "unique": "False",
        #             "foreign_key": ""
        #         }
        #     ]
        # }
        if "connection_name" in data:
            if data['connection_name'] not in DB_DICT:
                return jsonify({
                    "result": "The database connection given does not exist."
                }, 400)

        if not check_table(data["table_name"]):
            return jsonify({
                "result": "Module with this name is already present."
            }, 400)

        valid, msg = column_validation(data["columns"], data['connection_name'])
        if valid is False:
            return jsonify({"result": msg}, 400)

        dir_path = 'app/' + data["table_name"]
        create_model(dir_path, data)
        remove_alembic_versions()
        move_migration_files()
        migrate()
        return jsonify({"result": "Successfully edited model"})

    def delete(self, content_type):
        """Delete a content type"""
        tables_list = []
        for table in metadata.sorted_tables:
            f = (table.__dict__['foreign_keys'])
            for s in f:
                table_name = s.column.table
                if str(table_name) == content_type:
                    tables_list.append(table.name)

        if len(tables_list) > 0:
            return jsonify({
                "result": "The table {} is linked to another table(s). "
                          "Delete table(s) {} first.".format(
                    content_type, ', '.join(tables_list))
            }, 400)

        try:
            shutil.rmtree('app/' + content_type)
        except FileNotFoundError:
            return jsonify({"result": "Module does not exist."}, 400)

        with open("app/blueprints.py", "r") as f:
            lines = f.readlines()
        with open("app/blueprints.py", "w") as f:
            for line in lines:
                if line.strip("\n") != "from app." + content_type \
                        + ".resources import mod_model" and line.strip("\n") \
                        != "app.register_blueprint(mod_model, url_prefix='/" + \
                        content_type + "')":
                    f.write(line)
        remove_alembic_versions()
        move_migration_files()
        migrate()
        return jsonify({"result": "Successfully deleted module"})


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
            return jsonify({
                "result": "Connection with name: {} is already present. Use "
                          "a different name.".format(data['connection_name'])
            }, 400)

        string = ''
        if data['type'] == 'mysql':
            string = '"mysql://{}:{}@{}:3306/{}?charset=utf8mb4"'.format(
                data['username'], data['password'], data['host'],
                data['database_name'])

        if data['type'] == 'postgresql':
            string = '"postgresql+psycopg2://{}:{}@{}/{}"'.format(
                data['username'], data['password'], data['host'],
                data['database_name'])

        with open('dbs.py', 'r') as f:
            lines = f.readlines()

        with open('dbs.py', 'w') as f:
            for i, line in enumerate(lines):
                if line.startswith('}'):
                    line = '    "' + data['connection_name'] + '": ' + string\
                           + ',\n' + line
                f.write(line)

        add_new_db(data['connection_name'])

        return jsonify({
            "result": "Successfully created database connection string"
        })

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
            return jsonify({
                "result": "No connection with name: {} is present.".format(
                    data['connection_name'])}, 400)

        db_type = DB_DICT[data['connection_name']].split(':')[0]
        try:
            db_type = db_type.split('+')[0]
        except KeyError:
            pass

        if db_type != data['type']:
            return jsonify({
                "result": "The type of database string cannot be "
                          "changed. Create a new connection or choose the "
                          "correct type."}, 400)

        string = ''
        if data['type'] == 'mysql':
            string = '"mysql://{}:{}@{}:3306/{}?charset=utf8mb4"'.format(
                data['username'], data['password'], data['host'],
                data['database_name'])

        if data['type'] == 'postgresql':
            string = '"postgresql+psycopg2://{}:{}@{}/{}"'.format(
                data['username'], data['password'], data['host'],
                data['database_name'])

        with open('dbs.py', 'r') as f:
            lines = f.readlines()

        with open('dbs.py', 'w') as f:
            for i, line in enumerate(lines):
                if line.startswith('    "' + data['connection_name']):
                    line = line.replace(line, '    "' + data[
                        'connection_name'] + '": ' + string + ',\n')
                f.write(line)

        remove_alembic_versions()
        move_migration_files()
        migrate()
        return jsonify({
            "result": "Successfully edited database connection string."
        })


class ColumnType(Resource):

    def get(self):
        """Get a list of all valid column types available."""
        return jsonify({
            "result": column_types()
        })


api_admin.add_resource(ContentType, '/content/types',
                       '/content/types/<string:content_type>')
api_admin.add_resource(DatabaseInit, '/dbinit/',
                       '/dbinit/types/<string:content_type>')
api_admin.add_resource(ColumnType, '/columntypes')
