from collections import defaultdict
from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import verify_jwt

from admin.models import Admin, JWT, RestrictedByJWT

from app import db

docs = Blueprint("docs", __name__)
api_utils = Api()
api_utils.init_app(docs)

metadata = db.metadata


class ListDocs(Resource):
    """
    Endpoint to return docs
    """

    @jwt_required
    def get(self, app_name):
        admin = get_jwt_identity()

        if not verify_jwt(admin, Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )

        app_type = "Basic"

        jwt_configured = JWT.query.filter_by(connection_name=app_name).first()

        restricted_tables = RestrictedByJWT.query.filter_by(
            connection_name=app_name
        ).first()

        if jwt_configured is not None:
            app_type = "JWT Authenticated"

        tables = defaultdict(dict)
        for table in metadata.sorted_tables:
            tables[table.info["bind_key"]][table.name] = table

        tables = tables[app_name]

        result = {"app_name": app_name, "app_type": app_type,
                  "unrestricted_tables": [], "locked_tables": [],
                  "base_table": []}

        if app_type == "JWT Authenticated":
            base_table = tables[jwt_configured.table]
            obj = []
            for column in base_table.columns:
                obj.append(
                    {
                        "prop_name": column.name,
                        "prop_type": str(column.type),
                        "prop_default": str(column.default),
                    }
                )
            result["base_table"] = [
                {
                    "name": base_table.name,
                    "table_object": obj,
                    "end_points": [
                        {
                            "request_type": "POST",
                            "request_body": obj,
                            "end_point": app_name
                            + "/"
                            + base_table.name
                            + "/register",
                            "response_body": [
                                {
                                    "code": 200,
                                    "body": {
                                        "result": "string",
                                        "id": "integer",
                                        "access_token": "string",
                                        "refresh_token": "string",
                                    },
                                },
                                {
                                    "code": 400,
                                    "body": {"result": "Missing Field."},
                                },
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                        {
                            "request_type": "POST",
                            "request_body": obj,
                            "end_point": app_name
                            + "/"
                            + base_table.name
                            + "/login",  # noqa E401
                            "response_body": [
                                {
                                    "code": 200,
                                    "body": {
                                        "result": "string",
                                        "id": "integer",
                                        "access_token": "string",
                                        "refresh_token": "string",
                                    },
                                },
                                {
                                    "code": 400,
                                    "body": {"result": "Missing Field."},
                                },
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                        {
                            "request_type": "GET",
                            "request_body": None,
                            "end_point": app_name
                            + "/"
                            + base_table.name
                            + "/<id>",  # noqa E401
                            "params": {"name": "id", "type": "Integer"},
                            "response_body": [
                                {"code": 200, "body": [obj]},
                                {
                                    "code": 400,
                                    "body": {"result": "Missing Field."},
                                },
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                        {
                            "request_type": "PUT",
                            "request_body": obj,
                            "end_point": app_name
                            + "/"
                            + base_table.name
                            + "/<id>",  # noqa E401
                            "params": {"name": "id", "type": "Integer"},
                            "response_body": [
                                {
                                    "code": 200,
                                    "body": "Successfully updated row.",
                                },
                                {
                                    "code": 400,
                                    "body": {"result": "Missing Field."},
                                },
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                        {
                            "request_type": "DELETE",
                            "request_body": None,
                            "end_point": app_name
                            + "/"
                            + base_table.name
                            + "/<id>",  # noqa E401
                            "params": {"name": "id", "type": "Integer"},
                            "response_body": [
                                {
                                    "code": 200,
                                    "body": "Successfully updated row.",
                                },
                                {
                                    "code": 400,
                                    "body": {"result": "Missing Field."},
                                },
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                    ],
                }
            ]
            del tables[base_table.name]

            rest_tables = []
            if restricted_tables is not None:
                locked_tables = restricted_tables.restricted_tables.split(",")
                for table in locked_tables:
                    locked_table = tables[table]
                    table_object = []
                    for column in locked_table.columns:
                        table_object.append(
                            {
                                "prop_name": column.name,
                                "prop_type": str(column.type),
                                "prop_default": column.default,
                            }
                        )

                    del tables[table]
                    rest_tables.append(
                        {
                            "table_name": table,
                            "table_object": table_object,
                            "end_points": [
                                {
                                    "request_type": "GET",
                                    "request_body": table_object,
                                    "end_point": app_name + "/" + table,
                                    "response_body": [
                                        {"code": 200, "body": [table_object]},
                                        {
                                            "code": 400,
                                            "body": {
                                                "result": "Missing Field."
                                            },
                                        },
                                        {
                                            "code": 500,
                                            "body": {
                                                "result": "Server Error."
                                            },
                                        },
                                    ],
                                },
                                {
                                    "request_type": "POST",
                                    "request_body": table_object,
                                    "end_point": app_name + "/" + table,
                                    "response_body": [
                                        {"code": 200, "body": table_object},
                                        {
                                            "code": 400,
                                            "body": {"result": "Error"},
                                        },
                                        {
                                            "code": 500,
                                            "body": {
                                                "result": "Server Error."
                                            },
                                        },
                                    ],
                                },
                                {
                                    "request_type": "PUT",
                                    "request_body": table_object,
                                    "end_point": app_name + "/" + table,
                                    "response_body": [
                                        {"code": 200, "body": table_object},
                                        {
                                            "code": 400,
                                            "body": {"result": "Error"},
                                        },
                                        {
                                            "code": 500,
                                            "body": {
                                                "result": "Server Error."
                                            },
                                        },
                                    ],
                                },
                                {
                                    "request_type": "DELETE",
                                    "request_body": table_object,
                                    "end_point": app_name
                                    + "/"
                                    + table
                                    + "/<id>",
                                    "response_body": [
                                        {
                                            "code": 200,
                                            "body": "Successfully Deleted row.",  # noqa E401
                                        },
                                        {
                                            "code": 400,
                                            "body": {"result": "Error."},
                                        },
                                        {
                                            "code": 500,
                                            "body": {
                                                "result": "Server Error."
                                            },
                                        },
                                    ],
                                },
                            ],
                        }
                    )
            result["locked_tables"].append(rest_tables)

        ur_tables = []
        for table_name, info in tables.items():
            table_object = []
            for column in info.columns:
                default = str(column.default)
                if column.default is not None:
                    default = default[
                        default.find("(") + 1: default.find(")")
                    ].replace("'", "")
                table_object.append(
                    {
                        "prop_name": column.name,
                        "prop_type": str(column.type),
                        "prop_default": default,
                    }
                )
            ur_tables.append(
                {
                    "table_name": table_name,
                    "table_object": table_object,
                    "end_points": [
                        {
                            "request_type": "GET",
                            "request_body": table_object,
                            "end_point": app_name + "/" + table_name,
                            "response_body": [
                                {"code": 200, "body": [table_object]},
                                {
                                    "code": 400,
                                    "body": {"result": "Missing Field."},
                                },
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                        {
                            "request_type": "POST",
                            "request_body": table_object,
                            "end_point": app_name + "/" + table_name,
                            "response_body": [
                                {"code": 200, "body": table_object},
                                {"code": 400, "body": {"result": "Error"}},
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                        {
                            "request_type": "PUT",
                            "request_body": table_object,
                            "end_point": app_name + "/" + table_name,
                            "response_body": [
                                {"code": 200, "body": table_object},
                                {"code": 400, "body": {"result": "Error"}},
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                        {
                            "request_type": "DELETE",
                            "request_body": table_object,
                            "end_point": app_name + "/" + table_name + "/<id>",
                            "response_body": [
                                {
                                    "code": 200,
                                    "body": "Successfully Deleted row",
                                },
                                {"code": 400, "body": {"result": "Error."}},
                                {
                                    "code": 500,
                                    "body": {"result": "Server Error."},
                                },
                            ],
                        },
                    ],
                }
            )
        result["unrestricted_tables"].append(ur_tables)

        if result["base_table"]:
            result["Authorization"] = {
                "in": "header",
                "type": "jwt",
                "name": "Authorization",
                "value": "Bearer {{jwt}}",
                "on": ["base_table", "restricted_tables"],
            }
        else:
            result["Authorization"] = None
        return result


api_utils.add_resource(ListDocs, "/<app_name>")
