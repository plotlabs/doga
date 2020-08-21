import os
import platform
import shutil
import subprocess
import datetime
from sqlalchemy.exc import OperationalError, ProgrammingError

from app import db
from admin.version_models import *
from dbs import ALEMBIC_LIST, DB_DICT
from admin.models import JWT


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
    o.write("    create_dt = Column(DateTime(), server_default=text("
            "'CURRENT_TIMESTAMP'))\n")

    for col in data["columns"]:
        if col["name"] == "id":
            pass
        line = "    " + col["name"] + " = Column(" + col["type"] \
               + ", nullable=" + str(col["nullable"]).title() \
               + ", unique=" + str(col["unique"]).title()
        if col["default"] == "":
            line = line + ")\n"
        else:
            if col["foreign_key"] == "":
                if isinstance(col["default"], str):
                    if col["default"].lower() == "current":
                        col["default"] = "CURRENT_TIMESTAMP"
                        line = line + ", server_default=text('" + str(
                            col["default"]) + "'))\n"
                    elif col["type"].upper() == "BOOLEAN":
                        line = line + ", server_default=text('" + str(
                            col["default"]) + "'))\n"
                    else:
                        line = line + ", server_default='" + str(
                            col["default"]) + "')\n"
                else:
                    line = line + ", server_default=text('" + str(
                        col["default"]) + "'))\n"
        if col["foreign_key"] != "":
            line = line + "\n    " + col["foreign_key"].lower() + \
                " = relationship('" + col["foreign_key"] + "')\n"
        o.write(line)
    o.close()


def create_resources(model_name, dir_path, jwt_required,
                     expiry, jwt_restricted, filter_keys):
    """Function to create the CRUD Restful APIs for the module"""
    o = open(dir_path + "/resources.py", "w")

    if jwt_required is True:

        for line in open("templates/jwt_resource.py"):
            line = line.replace("modulename", model_name.lower())
            line = line.replace("modelname", model_name.title())
            line = line.replace("bname", '"' + model_name.lower() + '"')
            line = line.replace("jwt_key", str(filter_keys))
            line = line.replace("expiry_unit", expiry['unit'])
            line = line.replace("expiry_value", str(expiry['value']))
            line = line.replace("endpoint", '"/"')
            line = line.replace("param", '"/<int:id>"')
            o.write(line)

    else:
        for line in open("templates/resources.py"):

            if jwt_restricted is True:
                line = line.replace("def post", "@jwt_required\n    def post")
                line = line.replace("def get", "@jwt_required\n    def get")
                line = line.replace("def put", "@jwt_required\n    def put")
                line = line.replace(
                    "def delete", "@jwt_required\n    def delete")

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


def check_table(table_name, connection_name=''):
    """Checks if the table exists or not"""
    exist = False
    for table in metadata.sorted_tables:
        if table.name == table_name.lower():
            if connection_name != '':
                if table.info['bind_key'] == connection_name:
                    exist = True
            else:
                exist = True

    return exist


def migrate():
    """Function to stop the app to migrate and then restart it."""

    migrate_folder = os.path.exists('migrations')
    if not migrate_folder:
        subprocess.check_output('flask db init --multidb', shell=True)
    pid = os.getpid()
    revision_id = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    migrate_command = "flask db migrate --rev-id " + revision_id
    upgrade_command = "flask db upgrade"
    sys_platform = platform.system()
    if sys_platform in ['Linux', 'Darwin']:
        run_command = "sh restart.sh"
    else:
        run_command = "start "" /b restart.bat"
    if pid != '':
        os.system(migrate_command + " && " + upgrade_command + " && "
                  + run_command + " " + str(pid))


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
        except ProgrammingError:
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


def check_jwt_present(connection_name, database_name):
    # check if JWT is already linked to the given database and connection
    jwt_obj = JWT.query.filter_by(
        connection_name=connection_name, database_name=database_name).first()
    return jwt_obj


def validate_filter_keys_names(filter_keys, columns):
    # check if filter keys given are are valid columns
    if "id" in filter_keys:
        return True
    column_names = [col['name'] for col in columns]
    return (set(filter_keys).issubset(set(column_names)))


def validate_filter_keys_jwt(filter_keys, columns):
    # check if filter keys given generate a unique set
    if "id" in filter_keys:
        return True
    for col in columns:
        if col["name"] in filter_keys:
            if col["unique"] == 'True' and col["nullable"] == 'False':
                return True
    return False


def set_expiry(expiry):
    msg = ''
    valid = True
    units = ['days', 'seconds', 'microseconds',
             'milliseconds', 'minutes', 'hours', 'weeks']
    try:
        if bool(expiry):
            if expiry["unit"] == "":
                expiry["unit"] = 'hours'
            elif expiry['unit'] not in units:
                msg = "Unit of expiry time for JWT token is not" \
                    " a valid one."
                valid = False
                return msg, valid, expiry
            if expiry["value"] == "":
                expiry["value"] = 4
            if type(expiry["value"]) not in [int, float]:
                msg = 'Value of expiry time for JWT token should' \
                    ' be an integer.'
                valid = False
                return msg, valid, expiry
        else:
            expiry = {
                "unit": 'hours',
                "value": 4
            }
        valid = True
        return msg, valid, expiry
    except KeyError as e:
        return {"result": "Key error", "error": str(e)}, 500


def set_jwt_flag(connection_name, database_name, table_name):

    try:
        jwt_obj = JWT(jwt_flag=True,
                      connection_name=connection_name,
                      database_name=database_name,
                      table=table_name)
        db.session.add(jwt_obj)
        db.session.commit()
    except Exception as e:
        return {"result": e}, 500
