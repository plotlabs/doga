from flask import Blueprint, render_template, make_response, redirect, url_for, flash
from flask_restful import Api, Resource, marshal_with, fields

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from json import loads

from admin.utils import extract_database_name
from admin.export.utils import extract_engine_or_fail
from admin.models import Admin, JWT, RestrictedByJWT, Relationship, Deployments

from templates.models import metadata

from app.utils import verify_jwt

from dbs import DB_DICT

mod_dashboard = Blueprint("dashboard",
                          __name__,
                          template_folder="templates",
                          static_folder="static")

api_dashboard = Api()
api_dashboard.init_app(mod_dashboard)


class AdminDashboardStats(Resource):
    """
    Endpoint to return information that should be displayed to the Admin
    """
    @jwt_required
    def get(self):

        #make sure the dict in populated
        if not verify_jwt(get_jwt_identity(), Admin):
            flash("JWT authorization invalid, user does not exist.")
            return redirect(url_for('frontend.login'))

        else:
            app = {}
            for connection_name, connection_string in DB_DICT.items():
                db_name = extract_database_name(connection_name)
                engine = connection_string.split(":")[0]
                if db_name == "default":
                    app[db_name] = {"engine": engine}
                    pass
                else:
                    app[db_name] = {"engine": engine}

            tables = {}
            for table_ in metadata.sorted_tables:
                bind_key = table_.info["bind_key"]
                try:
                    tables[bind_key].append(table_)
                except KeyError:
                    tables[bind_key] = [table_]

            for filter_ in tables.keys():
                if connection_name in tables.keys():
                    app_info = {}
                    app_type = "basic"

                    jwt_base = JWT.query.filter_by(
                        connection_name=filter_).first()

                    if jwt_base is not None:
                        app_info["jwt_info"] = {
                            "base_table": jwt_base.table,
                            "filter_keys": jwt_base.filter_keys.split(","),
                        }
                        app_type = "JWT"
                    restricted_tables = RestrictedByJWT.query.filter_by(
                        connection_name=filter_).first()

                    if restricted_tables is not None:
                        restricted_tables = restricted_tables.restricted_tables. \
                            split(",")
                        app_info["jwt_info"][
                            "restricted_tables"] = restricted_tables
                        app_info["jwt_info"]["no_restricted_tables"] = len(
                            restricted_tables)

                    app_info["tables"] = []
                    for table_ in tables[filter_]:
                        table_d = {
                            "table_name": table_.name,
                            "no_fields": len(table_.columns),
                            "columns": table_.columns.keys()
                        }
                        app_info["tables"].append(table_d)

                    deployment_info = Deployments.query.filter_by(
                        app_name=filter_).first()

                    if deployment_info is not None:
                        timestamp = "{DD}-{M}-{YY} {HH}:{MM}:{SS}".format(
                            DD=deployment_info.create_dt.day,
                            M=deployment_info.create_dt.month,
                            YY=deployment_info.create_dt.year,
                            HH=deployment_info.create_dt.hour,
                            MM=deployment_info.create_dt.minute,
                            SS=deployment_info.create_dt.second,
                        )
                        app_info["deployment_info"] = {
                            "most_recent_deployment":
                            timestamp,
                            "platform":
                            deployment_info.platform.split(","),
                            "deployment_url":
                            deployment_info.deployment_url.split(","),
                            "total_no_exports":
                            deployment_info.exports,
                        }
                    else:
                        app_info["deployment_info"] = {
                            "most_recent_deployment": None,
                            "deployment_url": None,
                            "platform": None,
                            "total_no_exports": 0,
                        }

                    relation_ = Relationship.query.filter_by(
                        app_name=filter_).all()  # noqa 501

                    if relation_ is not None:
                        r = []
                        for rel in relation_:
                            relation = {
                                "relation_type": rel.relationship,
                                "relation_from": {
                                    "table_name":
                                    rel.table1_column.split(",")[0],
                                    "column_name":
                                    rel.table1_column.split(",")[1],
                                },
                                "relation_to": {
                                    "table_name":
                                    rel.table2_column.split(",")[0],
                                    "column_name":
                                    rel.table2_column.split(",")[1],
                                }
                            }
                            r.append(relation)
                        app_info["relationships"] = r
                    else:
                        app_info["relationships"] = None

                app_info["db_type"] = extract_engine_or_fail(filter_)
                app_info["number_of_tables"] = len(tables[filter_])
                app_info["type"] = app_type

                return render_template("dashboard.jinja2",
                                       template="dashboard-template",
                                       app=app_info,
                                       title="Dashbard")


api_dashboard.add_resource(AdminDashboardStats, "/dashboard/stats")


@api_dashboard.representation("text/html")
def out_html(data, code, headers):
    return make_response(data)
