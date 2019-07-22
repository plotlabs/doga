import os
import shutil
import subprocess

from admin.version_models import *
from dbs import ALEMBIC_LIST


def create_dir(model_name):
    """Function to create an empty directory for the module"""
    dir_path = 'app/' + model_name

    if not os.path.exists(dir_path):
        os.makedirs(dir_path, mode=0o777)

    return dir_path


def create_model(dir_path, data):
    shutil.copy2('templates/models.py', dir_path)

    if "connection_name" in data:
        conn_name = data["connection_name"]
    else:
        conn_name = "default"

    o = open(dir_path + "/models.py", "a")
    o.write("class " + data["table_name"].title() + "(Base):\n")
    o.write("    __tablename__ = '" + data["table_name"].lower() + "'\n")
    o.write("    __bind_key__ = '" + conn_name + "'\n\n")
    o.write("    id = Column(BigInteger, primary_key=True)\n")
    for column in data["columns"]:
        if column["name"] == "id":
            pass
        line = "    " + column["name"] + " = Column(" + column["type"] \
               + ", nullable=" + column["nullable"] \
               + ", unique=" + column["unique"] + ")\n"
        if column["foreign_key"] != "":
            line = line + "\n    " + column["foreign_key"].lower() + \
                   " = relationship('" + column["foreign_key"] + "')\n"
        o.write(line)
    o.close()


def create_resources(model_name, dir_path):
    """Function to create the CRUD Restful APIs for the module"""
    o = open(dir_path + "/resources.py", "w")
    for line in open("templates/resources.py"):
        line = line.replace("modulename", model_name.lower())
        line = line.replace("modelname", model_name.title())
        line = line.replace("bname", '"' + model_name.lower() + '"')
        line = line.replace("endpoint", '"/"')
        line = line.replace("param", '"/<int:id>"')
        o.write(line)
    o.close()


def append_blueprint(model_name):
    """Function to register the blueprint for the new module in the app"""
    o = open("app/blueprints.py", "a")
    o.write("from app." + model_name + ".resources import mod_model\n")
    o.write(
        "app.register_blueprint(mod_model, url_prefix='/" + model_name +
        "')\n\n")
    o.close()


def migrate():
    """Function to stop the app to migrate and then restart it."""

    migrate_folder = os.path.exists('migrations')
    if not migrate_folder:
        subprocess.check_output('flask db init --multidb', shell=True)

    command = "ps -eaf | grep 'python runserver.py' | grep -v grep | awk '{" \
              "print $2}'"
    process = subprocess.check_output(command, shell=True)
    pid = process.decode("utf-8").split('\n')[0]

    if pid != '':
        subprocess.Popen('kill -9 ' + str(pid), shell=True)
        os.system('flask db migrate && flask db upgrade && python '
                  'runserver.py')


def remove_alembic_versions():
    """Remove all alembic versions from existing databases"""

    for version in ALEMBIC_LIST:
        eval(version).query.delete()
    db.session.commit()


def add_alembic_model(conn_name):
    """Add alembic version table model for new database connection"""
    o = open("admin/version_models.py", "a")
    o.write("class AlembicVersion" + conn_name.title() + "(Base):\n")
    o.write("    __tablename__ = 'alembic_version'\n")
    o.write("    __bind_key__ = '" + str(conn_name) + "'\n")
    o.write("    __table_args__ = {'extend_existing': True}\n")
    o.write("    version_num = Column(String(32), primary_key=True)\n\n\n")
    o.close()

    with open('dbs.py', 'r') as f:
        lines = f.readlines()

    with open('dbs.py', 'w') as f:
        for i, line in enumerate(lines):
            if line.startswith(']'):
                line = '    "AlembicVersion' + str(conn_name).title() + \
                       '",\n' + line
            f.write(line)


def add_new_db(conn_name):
    """Save old migrations in another folder, delete current migration folder
    and initialize migrations again"""
    remove_alembic_versions()
    add_alembic_model(conn_name)
    dir_migration_versions = "migrations/versions/"
    version_files = os.listdir(dir_migration_versions)
    for file_name in version_files:
        full_file_name = os.path.join(dir_migration_versions, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, 'old_migrations/')
    shutil.rmtree('migrations')
    migrate()

