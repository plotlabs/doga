from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from templates.models import metadata
from admin.module_generator import *

mod_admin = Blueprint("admin", __name__)
api_admin = Api()
api_admin.init_app(mod_admin)


class ContentType(Resource):

    def get(self):
        """Get a list of all the content types"""
        table_list = {}
        for table in metadata.sorted_tables:
            objs = []
            for c in table.columns:
                obj = {
                    "name": c.name,
                    "type": str(c.type),
                    "nullable": c.nullable
                }
                objs.append(obj)
            table_list[table.name] = objs

        return jsonify(table_list)

    def post(self):
        """Create a content type"""
        data = request.get_json()
        # sample data
        # data = {
        #     "content_name": "user",
        #     "table_name": "user",
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
        dir_path = create_dir(data["content_name"])
        create_model(dir_path, data)
        create_resources(data["content_name"], dir_path)
        append_blueprint(data["content_name"])
        migrate()
        return jsonify({"message": "Successfully created module"})

    def put(self):
        """Edit a content type"""
        data = request.get_json()
        # sample data
        # data = {
        #     "content_name": "user",
        #     "table_name": "user",
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
        dir_path = 'app/' + data["content_name"]
        create_model(dir_path, data)
        migrate()
        return jsonify({"message": "Successfully edited model"})

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
            return jsonify({"message": "The table {} is linked to "
                                       "another table(s). Delete table(s) "
                                       "{} first.".format(
                content_type, ', '.join(tables_list))})

        try:
            shutil.rmtree('app/' + content_type)
        except FileNotFoundError:
            return jsonify({"message": "Module does not exist."})

        with open("app/blueprints.py", "r") as f:
            lines = f.readlines()
        with open("app/blueprints.py", "w") as f:
            for line in lines:
                if line.strip("\n") != "from app." + content_type \
                        + ".resources import mod_model" and line.strip("\n") \
                        != "app.register_blueprint(mod_model, url_prefix='/" + \
                        content_type + "')":
                    f.write(line)
        migrate()
        return jsonify({"message": "Successfully deleted module"})


class DatabaseInit(Resource):

    def post(self):
        """Create a database connection string"""
        data = request.get_json()
        # sample data
        # data = {
        #     "type": "mysql/mongo/postgres",
        #     "connection_name": "db1",
        #     "username": "user",
        #     "password": "pass",
        #     "host": "localhost",
        #     "database_name": "database_name",
        # }

        string = ''
        if data['type'] == 'mysql':
            string = '"mysql://{}:{}@{}:3306/{}?charset=utf8mb4"'.format(
                data['username'], data['password'], data['host'],
                data['database_name'])

        if data['type'] == 'postgres':
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

        migrate()

        return jsonify(
            {"message": "Successfully created database connection string"})


api_admin.add_resource(ContentType, '/content/types',
                       '/content/types/<string:content_type>')
api_admin.add_resource(DatabaseInit, '/dbinit/',
                       '/dbinit/types/<string:content_type>')
