import os
import shutil
import boto3

from admin.aws_config import *
from amdin.export.db_utils import *
from admin.utils import extract_database_name
from admin.export.utils import *

from config import HOST, PORT


app_name = "test"
to_deploy = False
path = ''


def uppath(_path, n): return os.sep.join(_path.split(os.sep)[:-n])  # noqa 731


def create_app_dir(app_name, rds, user_credentails, config):
    # create a dir to export the app
    parent_dir = uppath(__file__, 3)
    export_dir = os.path.join(parent_dir, 'exported_app')

    if os.path.exists(export_dir):
        os.system("rm -rf "+export_dir)

    os.mkdir(export_dir)

    db_engine = extract_engine_or_fail(app_name)
    # copy app endpoints and resources
    for file in os.listdir(parent_dir + '/app/' + app_name):
        s = os.path.join(parent_dir + '/app/' + app_name, file)
        d = os.path.join(parent_dir + '/exported_app/app/' + app_name, file)
        if os.path.isdir(s):
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copytree(s, d)
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)

    to_copy = [
        'app/utils.py',
        'app/__init__.py',
        'runserver.py',
        'blueprints.py',
        'requirements.txt',
        'Dockerfile',
        'config.py',
        'dbs.py',
        'test.db'
    ]

    for file in to_copy:
        if file == 'requirements.txt':
            create_requirements(
                rds['DBInstance']['Engine'].lower(),
                parent_dir + '/templates/export/requirements',
                parent_dir + '/exported_app'
            )
        elif file == 'Dockerfile':
            create_dockerfile(
                PORT,
                parent_dir + '/templates/export/Dockerfile',
                parent_dir + '/exported_app/app/Dockerfile'
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
        elif file == 'test.db':
            delete_admin()
            drop_all_jwt()
            s = parent_dir + '/' + file
            d = parent_dir + '/exported_app/' + file
            os.makedirs(os.path.dirname(d), exists_ok=True)
            shutil.copy2(s, d)
        elif file == 'dbs.py':
            create_dbs_file(
                app_name,
                parent_dir + '/exported_app/' + file,
                rds,
                user_credentails,
                config
            )
        else:
            s = file
            d = parent_dir + '/exported_app/' + file
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
