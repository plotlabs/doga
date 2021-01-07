from admin.export.utils import *
from admin.export.errors import DogaHerokuDeploymentError, DogaAppNotFound

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


def create_export_files(platform, parent_dir, app_name, deploy, rds_engine,
                        rds, user_credentials, config):
    to_copy = [
            'app/utils.py',
            'app/__init__.py',  # to ad db.create-all()
            'runserver.py',
            'blueprints.py',
            'requirements.txt',
            'Dockerfile',
            'config.py',
            'dbs.py',
            'jwt_dict.py',
        ]

    if platform == 'heroku':
        try:
            db_engine = extract_engine_or_fail(app_name)
        except DogaAppNotFound:
            return

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
            if platform == 'aws':
                create_requirements(
                    rds_engine,
                    parent_dir + '/templates/export/requirements',
                    parent_dir + '/exported_app'
                )
            else:
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
                    d = parent_dir + '/exported_app/' + file
                    os.makedirs(os.path.dirname(d), exist_ok=True)
                    shutil.copy2(s, d)
        elif file == 'jwt_dict.py':
            create_jwt_dict(
                app_name,
                parent_dir + '/exported_app/' + file,
            )
        else:
            s = file
            d = parent_dir + '/exported_app/' + file
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

        if db_engine != 'postgres' and deploy is True:
            raise DogaHerokuDeploymentError("Only a managed postgres db can"
                                            " be provisioned")

        create_export_files(platform, parent_dir, app_name, deploy, db_engine,
                            None, None, None)
    else:
        create_export_files(platform, parent_dir, app_name, False,
                            rds['Engine'].lower(), rds, user_credentials,
                            config)
