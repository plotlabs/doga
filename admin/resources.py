import os
import shutil

from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from templates.models import metadata


def get_admin_bp():
    """
    Returns auth blueprint and resources
    """
    mod = Blueprint(
        "admin",
        __name__,
        url_prefix="/admin"
    )
    api = Api(mod)
    # Definition of API urls in the blueprint
    api.add_resource(ContentType, '/content/types',
                     '/content/types/<string:content_type>')
    return api


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
        # data = request.get_json()
        # sample data
        data = {
            "content_name": "user",
            "table_name": "user",
            "columns": [
                {
                    "name": "id",
                    "type": "BigInteger",
                    "primary_key": "True",
                    "nullable": "False",
                    "unique": "True"
                },
                {
                    "name": "name",
                    "type": "String(32, 'utf8mb4_unicode_ci')",
                    "primary_key": "False",
                    "nullable": "False",
                    "unique": "True"
                },
                {
                    "name": "desc",
                    "type": "String(1024, 'utf8mb4_unicode_ci')",
                    "primary_key": "False",
                    "nullable": "False",
                    "unique": "False"
                }
            ]
        }
        dir_path = 'app/' + data["content_name"]
        o = open("app/bprints.py", "a")
        o.write("from app." + data["content_name"] + " import models\n")
        o.close()

        if not os.path.exists(dir_path):
            os.makedirs(dir_path, mode=0o777)
        shutil.copy2('templates/models.py', dir_path)

        o = open(dir_path + "/models.py", "a")
        o.write("class " + data["content_name"].title() + "(Base):\n")
        o.write("    __tablename__ = '" + data["table_name"].lower() + "'\n")
        for column in data["columns"]:
            line = "    " + column["name"] + " = Column(" + column["type"]\
                   + ", primary_key=" + column["primary_key"] \
                   + ", nullable=" + column["nullable"] \
                   + ", unique=" + column["unique"] + ")\n"
            o.write(line)
        o.close()

    def delete(self, content_type):
        """Delete a content type"""
        shutil.rmtree('app/' + content_type)
        with open("app/bprints.py", "r") as f:
            lines = f.readlines()
        with open("app/bprints.py", "w") as f:
            for line in lines:
                if line.strip("\n") != "from app." + content_type \
                        + " import models":
                    f.write(line)

