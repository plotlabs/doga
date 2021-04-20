import os

from app import db

from admin.export.utils import *
from admin.export.errors import DogaHerokuDeploymentError, DogaAppNotFound

from admin.models import JWT, Deployments

from config import PORT

to_deploy = False
path = ''


def uppath(_path, n): return os.sep.join(_path.split(os.sep)[:-n])  # noqa 731


def check_if_exist(app_name):
    parent_dir = uppath(__file__, 3)
    extract_engine_or_fail(app_name)
    try:
        os.listdir(parent_dir + '/app/' + app_name)
    except FileNotFoundError as error:
        raise DogaAppNotFound(error)


def create_export_files(platform, parent_dir, dest_dir, app_name, deploy,
                        rds_engine, rds, user_credentials, config):
    to_copy = [
        'app/utils.py',
        'app/__init__.py',
        'runserver.py',
        'blueprints.py',
        'requirements.txt',
        'Dockerfile',
        'config.py',
        'dbs.py',
    ]

    if platform == 'heroku':
        try:
            db_engine = extract_engine_or_fail(app_name)
        except DogaAppNotFound:
            return

    # check if app has JWT hare if not remove JWT from runserver
    is_jwt = True
    is_jwt = JWT.query.filter_by(connection_name=app_name).first()

    if is_jwt is None:
        is_jwt is False

    if dest_dir is None:
        dest_dir = parent_dir

    # copy app endpoints and resources
    for file in os.listdir(parent_dir + '/app/' + app_name):
        s = os.path.join(parent_dir + '/app/' + app_name, file)
        d = os.path.join(
            dest_dir +
            '/exported_app/app/' +
            app_name,
            file)
        if os.path.isdir(s):
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copytree(s, d)
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)

    for file in to_copy:
        if file == 'requirements.txt':
            if platform == 'aws':
                create_requirements(
                    rds_engine,
                    parent_dir + '/templates/export/requirements',
                    dest_dir + '/exported_app'
                )
            else:
                create_requirements(
                    rds_engine,
                    parent_dir + '/templates/export/requirements',
                    dest_dir + '/exported_app'
                )
        elif file == 'Dockerfile':
            create_dockerfile(
                PORT,
                parent_dir + '/templates/export/Dockerfile',
                dest_dir + '/exported_app/Dockerfile'
            )
        elif file == 'blueprints.py':
            export_blueprints(
                app_name,
                parent_dir + '/app/blueprints.py',
                dest_dir + '/exported_app/app/blueprints.py'
            )
        elif file == 'config.py':
            s = parent_dir + '/' + file
            d = dest_dir + '/exported_app/' + file
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)

            if not is_jwt:
                f = open(d, 'r+')
                lines = f.readlines()
                f.truncate(0)
                f.seek(0)
                for line in lines:
                    if line.startswith('JWT'):
                        pass
                    else:
                        f.write(line)

        elif file == 'dbs.py':
            if platform == 'aws':
                create_dbs_file(
                    app_name,
                    parent_dir + '/exported_app/' + file,
                    rds,
                    user_credentials,
                    config
                )
            else:
                if deploy:
                    create_heroku_postgres(
                        app_name,
                        parent_dir + '/exported_app/' + file,
                    )
                else:
                    s = file
                    d = dest_dir + '/exported_app/' + file
                    os.makedirs(os.path.dirname(d), exist_ok=True)
                    contents = open(s, 'r').readlines()

                    for line in contents:
                        if app_name in line:
                            dbs = 'DB_DICT = {\n' + line + '}\n'
                        if 'AlembicVersion' + app_name.title() in line:
                            alembic_list = 'ALEMBIC_LIST = [\n' + line + ']\n'
                    open(d, 'w+').write(dbs + '\n' + alembic_list)

        elif file == 'runserver.py':
            s = file
            d = dest_dir + '/exported_app/' + file
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)

            with open(d, 'r+') as f:
                lines = f.readlines()
                f.truncate(0)
                f.seek(0)
                for line in lines:
                    line = line.replace(
                        'from admin.utils import set_jwt_secret_key', ''
                    )
                    line.replace(
                        'from admin.request_utils import AfterResponse', ''
                    )
                    line = line.replace(
                        'AfterResponse(app)', ''
                    )
                    line = line.replace(
                        'set_jwt_secret_key()', ''
                    )
                    f.write(line)

        elif file == 'app/__init__.py':
            s = file
            d = dest_dir + '/exported_app/' + file
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)

            with open(d, 'a+') as f:
                f.write("\ndb.create_all()\n")
        elif file == 'app/utils.py':
            s = file
            d = dest_dir + '/exported_app/' + file
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)

            f = open(d, 'r+')
            lines = f.readlines()
            f.truncate(0)
            f.seek(0)
            check_for_tab = False
            for line in lines:
                if line.startswith('def migrate():'):
                    check_for_tab = True
                elif check_for_tab:
                    if line.startswith('    ') or line.startswith('\n'):
                        pass
                    else:
                        check_for_tab = False
                else:
                    f.write(line)
        else:
            s = file
            d = dest_dir + '/exported_app/' + file
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)


def create_app_dir(
        app_name,
        rds,
        user_credentials,
        config,
        platform,
        **kwargs):

    # create a dir to export the app
    parent_dir = uppath(__file__, 3)
    export_dir = os.path.join(parent_dir, 'exported_app')

    if os.path.exists(export_dir):
        os.system("rm -rf " + export_dir)

    os.mkdir(export_dir)
    if platform == 'heroku':
        deploy = kwargs.get('deploy_db', True)
        try:
            db_engine = extract_engine_or_fail(app_name)
        except DogaAppNotFound:
            return

        if 'postgres' not in db_engine and deploy is True:
            raise DogaHerokuDeploymentError("Only a managed postgres db can"
                                            " be provisioned")

        create_export_files(platform, parent_dir, None, app_name, deploy,
                            db_engine, None, None, None)

    elif platform == 'local':

        path = kwargs['path']
        try:
            db_engine = extract_engine_or_fail(app_name)
        except DogaAppNotFound:
            return

        create_export_files(platform, parent_dir, path, app_name, False,
                            db_engine, None, None, None)

    else:
        create_export_files(platform, parent_dir, None, app_name, False,
                            rds['Engine'].lower(), rds, user_credentials,
                            config)


def write_to_deployments(app_name, platform):
    old_entry = Deployments.query.filter_by(app_name=app_name).first()
    if old_entry is None:
        app_deployed = Deployments(
            app_name=app_name,
            platfrom=platform,
            status='Not Fetched Yet',
            exports=1
        )
        db.session.add(app_deployed)
    else:
        old_entry.exports = old_entry.exports + 1

    db.session.commit()


def create_docs(platform, parent_dir, dest_dir, app_name, deploy,
                rds_engine, rds, user_credentials, config):

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
        base_table = tables[jwt_configured.table]
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
                        "request_body": obj,
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
                        "request_body": obj,
                        "end_point": app_name + '/' + base_table.name + '/login',  # noqa E401
                        "response_body": [{"code": 200,
                                           "body": {"result": "string",
                                                    "id": "integer",
                                                    "access_token": "string",
                                                    "refresh_token": "string"}
                                                    },
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
                        "end_point": app_name + '/' + base_table.name + '/<id>',  # noqa E401
                        "params": {"name": "id",
                                "type": "Integer"},
                        "response_body": [{"code": 200,
                                        "body": [obj]},
                                        {"code": 400,
                                        "body": {"result": "Missing Field."
                                                    }},
                                        {"code": 500,
                                        "body": {"result": "Server Error."
                                                    }},
                                        ],
                        },
                    {"request_type": "PUT",
                        "request_body": obj,
                        "end_point": app_name + '/' + base_table.name + '/<id>',  # noqa E401
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
                        "end_point": app_name + '/' + base_table.name + '/<id>',  # noqa E401
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
        del tables[base_table.name]

        rest_tables = []
        if restricted_tables is not None:
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

                del tables[table]
                rest_tables.append({
                    "table_name": table,
                    "table_object": table_object,
                    "end_points": [
                        {
                            "request_type": "GET",
                            "request_body": table_object,
                            "end_point": app_name + '/' + table,
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
                            "end_point": app_name + '/' + table,
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
                            "end_point": app_name + '/' + table,
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
                            "end_point": app_name + '/' + table + '/<id>',
                            "response_body": [
                                {
                                            "code": 200,
                                            "body": "Successfully Deleted row."
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
            "table_name": table_name,
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

    if result['base_table'] != []:
        result['Authorization'] = {
            "in": "header",
            "type": "jwt",
            "name": "Authorization",
            "value": "Bearer {{jwt}}",
            "on": ["base_table", "restricted_tables"]
        }
    else:
        result['Authorization'] = None

    d = dest_dir + '/exported_app/app/api_docs.md'
    os.makedirs(os.path.dirname(d), exist_ok=True)
