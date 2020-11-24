import os
import shutil
import subprocess
import boto3

from admin.aws_config import *
from admin.utils import extract_database_name
from admin.export.utils import *

from dbs import DB_DICT
from config import HOST, PORT


app_name = "test"
to_deploy = False
path = ''


def uppath(_path, n): return os.sep.join(_path.split(os.sep)[:-n])  # noqa 731


# create a dir to export the app
parent_dir = uppath(__file__, 2)
export_dir = os.path.join(parent_dir, 'exported_app')
os.mkdir(export_dir)

# create an RDS using users credentials
db_engine = ''
for bind_key, db_url in DB_DICT.items():
    if app_name == extract_database_name(bind_key):
        db_engine = db_url.split(':')[0]
        break
    else:
        continue

if db_engine == '':
    raise 'No App found ' + "Could not find app: " + app_name + '.'

# TODO: remove once we take from the user
rds_params = {
    'DBInstanceIdentifier': "testDB",
    'DBInstanceClass': "db.t2.micro",
    'Engine': db_engine,
    'DBName': app_name,
    'MasterUsername': "admin",
    'MasterUserPassword': "password",
    'AllocatedStorage': 20
}

rds = create_RDS({}, rds_params)
print(rds)

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
    'config.py'
]

for file in to_copy:
    if file == 'requirements.txt':
        create_requirements(
            db_engine,
            parent_dir + '/templates/export/requirements',
            parent_dir + '/exported_app'
        )
    if file == 'Dockerfile':
        create_dockerfile(
            PORT,
            parent_dir + '/templates/export/Dockerfile',
            parent_dir + '/exported_app/app/Dockerfile'
        )
    if file == 'blueprints.py':
        export_blueprints(
            app_name,
            parent_dir + '/app/blueprints.py',
            parent_dir + '/exported_app/app/blueprints.py'
        )
    if file == 'config.py':
        s = parent_dir + '/' + file
        d = parent_dir + '/exported_app/' + file
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
    else:
        s = file
        d = parent_dir + '/exported_app/' + file
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
