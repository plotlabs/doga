import os
import shutil
import boto3

from admin.aws_config import *
from admin.utils import extract_database_name
from admin.export.utils import *
from admin.export.errors import DogaHerokuDeploymentError, DogaAppNotFound

from config import HOST, PORT


app_name = "test"
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


def create_app_dir(
        app_name,
        rds,
        user_credentails,
        config,
        platform,
        **kwargs):

    # create a dir to export the app
    parent_dir = uppath(__file__, 3)
    export_dir = os.path.join(parent_dir, 'exported_app')

    if os.path.exists(export_dir):
        os.system("rm -rf " + export_dir)

    os.mkdir(export_dir)

    to_copy = [
            'app/utils.py',
            'app/__init__.py',  # to ad db.createall()
            'runserver.py',
            'blueprints.py',
            'requirements.txt',
            'Dockerfile',
            'config.py',
            'dbs.py',
            'jwt_dict.py',
        ]

    if platform == 'aws':

        db_engine = extract_engine_or_fail(app_name)
        # copy app endpoints and resources
        for file in os.listdir(parent_dir + '/app/' + app_name):
            s = os.path.join(parent_dir + '/app/' + app_name, file)
            d = os.path.join(
                parent_dir +
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
                create_requirements(
                    rds['Engine'].lower(),
                    parent_dir + '/templates/export/requirements',
                    parent_dir + '/exported_app'
                )
            elif file == 'Dockerfile':
                create_dockerfile(
                    PORT,
                    parent_dir + '/templates/export/Dockerfile',
                    parent_dir + '/exported_app/Dockerfile'
                )
            elif file == 'blueprints.py':
                export_blueprints(
                    app_name,
                    parent_dir + '/app/blueprints.py',
                    parent_dir + '/exported_app/app/blueprints.py'
                )
            elif file == 'config.py':
                s = parent_dir + '/' + file
                d = parent_dir + '/exported_app/' + file
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
            elif file == 'dbs.py':
                create_dbs_file(
                    app_name,
                    parent_dir + '/exported_app/' + file,
                    rds,
                    user_credentails,
                    config
                )
            elif file == 'jwt_dict.py':
                has_jwt = create_jwt_dict(
                    app_name,
                    parent_dir + '/exported_app/' + file,
                )
                # if has_jwt:
                #    file = open(parent_dir + '/exported_app/app/' + app_name + '/resources.py')  # noqa 401
                #    all_lines = file.readlines()
                #       all_lines[32] = 'verify_jwt(get_jwt_identity())\n'
                #       all_lines[50] = 'verify_jwt(get_jwt_identity())\n'
                #       all_lines[145] = 'verify_jwt(get_jwt_identity())\n'
            else:
                s = file
                d = parent_dir + '/exported_app/' + file
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)

    elif platform == 'heroku':

        try:
            db_engine = extract_engine_or_fail(app_name)
        except DogaAppNotFound as error:
            return

        deploy = kwargs.get('deploy_db', True)
        if db_engine != 'postgres' and deploy is True:
            raise DogaHerokuDeploymentError("Only a managed postgres db can be"
                                            " provisioned")

        # copy app endpoints and resources
        for file in os.listdir(parent_dir + '/app/' + app_name):
            s = os.path.join(parent_dir + '/app/' + app_name, file)
            d = os.path.join(
                parent_dir +
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
                create_requirements(
                    db_engine.lower(),
                    parent_dir + '/templates/export/requirements',
                    parent_dir + '/exported_app'
                )
            elif file == 'Dockerfile':
                create_dockerfile(
                    PORT,
                    parent_dir + '/templates/export/Dockerfile',
                    parent_dir + '/exported_app/Dockerfile'
                )
            elif file == 'blueprints.py':
                export_blueprints(
                    app_name,
                    parent_dir + '/app/blueprints.py',
                    parent_dir + '/exported_app/app/blueprints.py'
                )
            elif file == 'config.py':
                s = parent_dir + '/' + file
                d = parent_dir + '/exported_app/' + file
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)

            elif file == 'dbs.py':
                if deploy:
                    create_heroku_postgres(
                        app_name,
                        parent_dir + '/exported_app/' + file,
                    )
                else:
                    s = file
                    d = parent_dir + '/exported_app/' + file
                    os.makedirs(os.path.dirname(d), exist_ok=True)
                    shutil.copy2(s, d)
            elif file == 'jwt_dict.py':
                has_jwt = create_jwt_dict(
                    app_name,
                    parent_dir + '/exported_app/' + file,
                )
            else:
                s = file
                d = parent_dir + '/exported_app/' + file
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
