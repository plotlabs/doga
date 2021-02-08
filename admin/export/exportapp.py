from admin.export.utils import *
from admin.export.errors import DogaHerokuDeploymentError, DogaAppNotFound

from admin.models import JWT

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
            'app/__init__.py',  # to ad db.create-all()
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
    is_jwt = JWT.query.filter_by(database_name=app_name).first()

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

        if db_engine != 'postgres' and deploy is True:
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
