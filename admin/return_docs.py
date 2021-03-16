from collections import defaultdict
from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import verify_jwt

from admin.models import Admin, JWT, Restricted_by_JWT

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
            return {"result": "JWT authorization invalid, user does not"
                    " exist."}, 401

        app_type = 'Basic'

        jwt_configured = JWT.query.filter_by(
            connection_name=app_name
        ).first()

        restricted_tables = Restricted_by_JWT.query.filter_by(
            connection_name=app_name
        ).first()

        if jwt_configured is not None:
            app_type = 'JWT Authenticated'

        tables = defaultdict(dict)
        for table in metadata.sorted_tables:
            tables[table.info['bind_key']][table.name] = table

        tables = tables[app_name]

        result = {}
        result["app_name"] = app_name
        result["app_type"] = app_type
        result['unrestricted_tables'] = []
        result['locked_tables'] = []
        result['base_table'] = []

        if app_type == 'JWT Authenticated':
            base_table = jwt_configured.table
            obj = []
            for column in base_table.columns:
                obj.append({
                    "prop_name": column.name,
                    "prop_type": str(column.type),
                    "prop_default": str(column.default)
                })
            result['base_table'] = [
                {
                    "name": base_table.name,
                    "table_object": obj,
                    "end_points": [
                        {"request_type": "POST",
                         "request_body": "table_object",
                         "end_point": app_name + '/' +
                         base_table.name +
                         '/register',
                         "response_body": [
                             {"code": 200,
                              "body": {"result": "string",
                                       "id": "integer",
                                       "access_token": "string",
                                       "refresh_token": "string"}
                              },
                             {"code": 400,
                              "body": {"result": "Missing Field."}},
                             {"code": 500,
                              "body": {"result": "Server Error."}},
                         ],
                         },
                        {"request_type": "POST",
                         "request_body": "table_object",
                         "end_point": app_name + '/' + base_table.name + '/login',
                         "response_body": [{"code": 200,
                                            "body": {"result": "string",
                                                     "id": "integer",
                                                     "access_token": "string",
                                                     "refresh_token": "string"}},
                                           {"code": 400,
                                            "body": {"result": "Missing Field."
                                                     }},
                                           {"code": 500,
                                            "body": {"result": "Server Error."
                                                     }},
                                           ],
                         },
                        {"request_type": "GET",
                         "request_body": None,
                         "end_point": app_name + '/' + base_table.name + '/<id>',
                         "params": {"name": "id",
                                    "type": "Integer"},
                         "response_body": [{"code": 200,
                                            "body": [table_object]},
                                           {"code": 400,
                                            "body": {"result": "Missing Field."
                                                     }},
                                           {"code": 500,
                                            "body": {"result": "Server Error."
                                                     }},
                                           ],
                         },
                        {"request_type": "PUT",
                         "request_body": table_object,
                         "end_point": app_name + '/' + base_table.name + '/<id>',
                         "params": {"name": "id",
                                    "type": "Integer"},
                         "response_body": [{"code": 200,
                                            "body": "Successfully updated row."
                                            },
                                           {"code": 400,
                                            "body": {"result": "Missing Field."
                                                     }},
                                           {"code": 500,
                                            "body": {"result": "Server Error."
                                                     }},
                                           ],
                         },
                        {"request_type": "DELETE",
                         "request_body": None,
                         "end_point": app_name + '/' + base_table.name + '/<id>',
                         "params": {"name": "id",
                                    "type": "Integer"},
                         "response_body": [{"code": 200,
                                            "body": "Successfully updated row."
                                            },
                                           {"code": 400,
                                            "body": {"result": "Missing Field."
                                                     }},
                                           {"code": 500,
                                            "body": {"result": "Server Error."
                                                     }},
                                           ],
                         }]}]
            tables.remove(base_table)

            rest_tables = []
            if restricted_tables is not None:
                for table_name, info in locked_tables.items():
                    locked_tables = restricted_tables.restricted_tables.split(
                        ',')

                for table in locked_tables:
                    locked_table = tables[table]
                    table_object = []
                    for column in locked_table.columns:
                        table_object.append({
                            "prop_name": column.name,
                            "prop_type": str(column.type),
                            "prop_default": column.default
                        })

                    tables.remove(table)
                rest_tables.append({
                    "table_object": table_object,
                    "end_points": [
                        {
                            "request_type": "GET",
                            "request_body": table_object,
                            "end_point": app_name + '/' + table_name,
                            "response_body": [
                                {
                                            "code": 200,
                                            "body": [table_object]
                                },
                                {
                                    "code": 400,
                                    "body": {
                                        "result": "Missing Field."
                                    }
                                },
                                {
                                    "code": 500,
                                    "body": {
                                        "result": "Server Error."
                                    }
                                }],
                        },
                        {
                            "request_type": "POST",
                            "request_body": table_object,
                            "end_point": app_name + '/' + table_name,
                            "response_body": [
                                {
                                            "code": 200,
                                            "body": table_object
                                },
                                {
                                    "code": 400,
                                    "body": {
                                        "result": "Error"
                                    }
                                },
                                {
                                    "code": 500,
                                    "body": {
                                        "result": "Server Error."
                                    }
                                }],
                        },
                        {
                            "request_type": "PUT",
                            "request_body": table_object,
                            "end_point": app_name + '/' + table_name,
                            "response_body": [
                                {
                                            "code": 200,
                                            "body": table_object
                                },
                                {
                                    "code": 400,
                                    "body": {
                                        "result": "Error"
                                    }
                                },
                                {
                                    "code": 500,
                                    "body": {
                                        "result": "Server Error."
                                    }
                                }],
                        },
                        {
                            "request_type": "DELETE",
                            "request_body": table_object,
                            "end_point": app_name + '/' + table_name + '/<id>',
                            "response_body": [
                                {
                                            "code": 200,
                                            "body": "Successfully Deleted row"
                                },
                                {
                                    "code": 400,
                                    "body": {
                                        "result": "Error."
                                    }
                                },
                                {
                                    "code": 500,
                                    "body": {
                                        "result": "Server Error."
                                    }
                                }],
                        },
                    ]})
            result['locked_tables'].append(rest_tables)

        ur_tables = []
        for table_name, info in tables.items():
            table_object = []
            for column in info.columns:
                table_object.append({
                                    "prop_name": column.name,
                                    "prop_type": str(column.type),
                                    "prop_default": column.default
                                    })
            ur_tables.append({
                "table_object": table_object,
                "end_points": [
                    {
                        "request_type": "GET",
                        "request_body": table_object,
                        "end_point": app_name + '/' + table_name,
                        "response_body": [
                                        {
                                            "code": 200,
                                            "body": [table_object]
                                        },
                            {
                                            "code": 400,
                                            "body": {
                                                "result": "Missing Field."
                                            }
                                        },
                            {
                                            "code": 500,
                                            "body": {
                                                "result": "Server Error."
                                            }
                                        }],
                    },
                    {
                        "request_type": "POST",
                        "request_body": table_object,
                        "end_point": app_name + '/' + table_name,
                        "response_body": [
                                        {
                                            "code": 200,
                                            "body": table_object
                                        },
                            {
                                            "code": 400,
                                            "body": {
                                                "result": "Error"
                                            }
                                        },
                            {
                                            "code": 500,
                                            "body": {
                                                "result": "Server Error."
                                            }
                                        }],
                    },
                    {
                        "request_type": "PUT",
                        "request_body": table_object,
                        "end_point": app_name + '/' + table_name,
                        "response_body": [
                                        {
                                            "code": 200,
                                            "body": table_object
                                        },
                            {
                                            "code": 400,
                                            "body": {
                                                "result": "Error"
                                            }
                                        },
                            {
                                            "code": 500,
                                            "body": {
                                                "result": "Server Error."
                                            }
                                        }],
                    },
                    {
                        "request_type": "DELETE",
                        "request_body": table_object,
                        "end_point": app_name + '/' + table_name + '/<id>',
                        "response_body": [
                                        {
                                            "code": 200,
                                            "body": "Successfully Deleted row"
                                        },
                            {
                                            "code": 400,
                                            "body": {
                                                "result": "Error."
                                            }
                                        },
                            {
                                            "code": 500,
                                            "body": {
                                                "result": "Server Error."
                                            }
                                        }],
                    },
                ]})
        result['unrestricted_tables'].append(ur_tables)
        return result


api_utils.add_resource(ListDocs, '/<app_name>')


"""
{
    app_name: "",
    app_type: "",
    locked_tables: [
        {
            "table_object": {
                {

                },
                {

                }
                ....
            }
            "request_type":
            "end_points":
        },
        {}
    ],
    base_table: [
        {}
    ],
    unrestricted_tables: [
        {}
    ],

}
"""
