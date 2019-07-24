import os
import shutil
import subprocess
import datetime

from sqlalchemy.exc import OperationalError

from admin.version_models import *
from dbs import ALEMBIC_LIST, DB_DICT


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
    if DB_DICT[conn_name].startswith("sqlite"):
        o.write("    id = Column(Integer, primary_key=True)\n")
    else:
        o.write("    id = Column(BigInteger, primary_key=True)\n")
    for col in data["columns"]:
        if col["name"] == "id":
            pass
        line = "    " + col["name"] + " = Column(" + col["type"] \
               + ", nullable=" + col["nullable"] \
               + ", unique=" + col["unique"] + ")\n"
        if col["foreign_key"] != "":
            line = line + "\n    " + col["foreign_key"].lower() + \
                   " = relationship('" + col["foreign_key"] + "')\n"
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


def check_table(table_name):
    """Checks if the table exists or not"""
    exists = False
    for table in metadata.sorted_tables:
        if table.name == table_name:
            exists = True

    return exists


def migrate():
    """Function to stop the app to migrate and then restart it."""

    migrate_folder = os.path.exists('migrations')
    if not migrate_folder:
        subprocess.check_output('flask db init --multidb', shell=True)

    command = "ps -eaf | grep 'python runserver.py' | grep -v grep | awk '{" \
              "print $2}'"
    process = subprocess.check_output(command, shell=True)
    pid = process.decode("utf-8").split('\n')[0]

    revision_id = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    migrate_command = "flask db migrate --rev-id " + revision_id
    upgrade_command = "flask db upgrade"
    run_command = "python runserver.py"
    if pid != '':
        subprocess.Popen('kill -9 ' + str(pid), shell=True)
        os.system(migrate_command + " && " + upgrade_command + " && "
                  + run_command)


def remove_alembic_versions():
    """Remove all alembic versions from existing databases"""

    for version in ALEMBIC_LIST:
        try:
            conn_name = version.split("AlembicVersion")[1].lower()
            if conn_name == "default":
                session_stm = "db.session.commit()"
            else:
                session_stm = conn_name + ".session.commit()"
            eval(version).query.delete()
            eval(session_stm)
        except OperationalError:
            pass


def add_alembic_model(conn_name):
    """Add alembic version table model for new database connection"""
    o = open("admin/version_models.py", "a")
    conn_name = str(conn_name).lower()
    base = "Base_" + conn_name
    column_name = "Column" + conn_name
    o.write(conn_name + " = SQLAlchemy(app)\n")
    o.write(base + " = " + conn_name + ".Model\n")
    o.write(column_name + " = " + conn_name + ".Column\n\n\n")
    o.write("class AlembicVersion" + conn_name.title() + "(" + base + "):\n")
    o.write("    __tablename__ = 'alembic_version'\n")
    o.write("    __bind_key__ = '" + conn_name + "'\n")
    o.write("    version_num = " + column_name + "(String(32), "
                                                 "primary_key=True)\n\n\n")
    o.close()

    with open('dbs.py', 'r') as f:
        lines = f.readlines()

    with open('dbs.py', 'w') as f:
        for i, line in enumerate(lines):
            if line.startswith(']'):
                line = '    "AlembicVersion' + str(conn_name).title() + \
                       '",\n' + line
            f.write(line)


def move_migration_files():
    """Move migration files to the old migrations folder"""
    if os.path.exists("migrations"):
        dir_migration_versions = "migrations/versions/"
        version_files = os.listdir(dir_migration_versions)

        # check if old_migration folder exists, if not, create one
        if not os.path.exists("old_migrations"):
            os.makedirs("old_migrations", mode=0o777)

        for file_name in version_files:
            full_file_name = os.path.join(dir_migration_versions, file_name)
            if os.path.isfile(full_file_name):
                shutil.move(full_file_name, 'old_migrations/')


def add_new_db(conn_name):
    """Save old migrations in another folder, delete current migration folder
    and initialize migrations again"""
    remove_alembic_versions()
    add_alembic_model(conn_name)
    move_migration_files()
    if os.path.exists("migrations"):
        shutil.rmtree('migrations')
    migrate()

