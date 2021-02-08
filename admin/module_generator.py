import os
import shutil

from sqlalchemy.exc import OperationalError, ProgrammingError

from admin.version_models import *
from dbs import ALEMBIC_LIST, DB_DICT
from admin.models import JWT, Restricted_by_JWT, Relationship
from admin.utils import extract_database_name
from admin.errors import *


def create_dir(model_name):
    """Function to create an empty directory for the module"""
    dir_path = 'app/' + model_name

    if not os.path.exists(dir_path):
        os.makedirs(dir_path, mode=0o777)

    return dir_path


def create_model(dir_path, data):
    """Function used while creating tables for the user to add their content.
    This creates a /app_name/models.py file using contents of the
    /templates/models.py
    It add all columns, connections, and relationships associated.
    """

    shutil.copy2('templates/models.py', dir_path)

    if "connection_name" in data:
        conn_name = data["connection_name"]
    else:
        conn_name = "default"

    app_name = extract_database_name(conn_name)
    relationships = ""

    o = open(dir_path + "/models.py", "a")
    o.write("\n\n")
    o.write("class " + data["table_name"].title() + "(Base):\n")
    o.write("    __tablename__ = '" + data["table_name"].lower() + "'\n")
    o.write("    __bind_key__ = '" + conn_name + "'\n\n")

    if DB_DICT[conn_name].startswith("sqlite"):
        o.write("    id = Column(Integer, primary_key=True)\n")
    else:
        o.write("    id = Column(BigInteger, primary_key=True)\n")
    o.write("    create_dt = Column(DateTime(), server_default=text("
            "'CURRENT_TIMESTAMP'))\n")

    for col in data['columns']:
        if col["name"] == "id":
            pass
        try:
            relation = col['relationship']
            relation_type = relation['relationship_type']
            relations = ['one-one', 'many-one', 'many-many', 'one-many']
            if relation_type not in relations:
                return {"result": "Relation type for column" +
                                  col["name"] +
                                  "must be of type " +
                                  ','.join(relations)}
            if relation_type in ['one-one', 'one-many']:
                # TODO: what if user has their own foreign key too
                # deal with a list of foreign keys
                col["foreign_key"] = relation['related_table'].lower() + "." +\
                    relation['related_field'].lower()
            try:
                relationships = Relationship.query.all()
                if relationships is None:
                    relation = Relationship(
                            app_name=app_name,
                            table1_column=relation['related_table'],
                            relationship=relation['related_field'],
                            table2_column=col["name"]
                            )
                    db.session.add(relation)
                relationships = create_relationsips(app_name,
                                                    relation_type,
                                                    relation['related_table'],
                                                    relation['related_field'],
                                                    data['table_name'],
                                                    col["name"],
                                                    col['type'],
                                                    relationships
                                                    )

            except RelatedContentNotFound as err:
                pass

        except KeyError as error:
            relation_type = None

        try:
            line = "    " + col["name"] + " = Column(" + col["type"] \
                   + ", nullable=" + str(col["nullable"]).title() \
                   + ", unique=" + str(col["unique"]).title()
            if col["foreign_key"] != "":
                line = "    " + col["name"] + " = Column(" + col["type"] \
                    + ", ForeignKey('" + col["foreign_key"].lower() + "')" \
                    + ", nullable=" + str(col["nullable"]).title() \
                    + ", unique=" + str(col["unique"]).title()
        except KeyError as error:
            return {
                "result": "Missing parameters for columns",
                "parameters": error.args
            }, 500

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
        o.write(line)
    o.write(relationships)
    o.close()


def create_resources(model_name, connection_name, dir_path, base_jwt,
                     expiry, restrict_by_jwt, filter_keys=""):
    """Function to create the CRUD Restful APIs for the module"""
    o = open(dir_path + "/resources.py", "w")

    if base_jwt in [True, "True", "true"]:
        for line in open("templates/jwt_resource.py"):
            line = line.replace("modulename", model_name)
            line = line.replace("module_endp", model_name.title().split('.')[0])  # noqa E401
            line = line.replace("modelname", model_name.title().split('.')[1])
            line = line.replace("bname", '"' + model_name.lower() + '"')
            line = line.replace("jwt_key", str(filter_keys))
            line = line.replace("expiry_unit", expiry['unit'])
            line = line.replace("expiry_value", str(expiry['value']))
            line = line.replace("endpoint", '"/"')
            line = line.replace("param", '"/<int:id>"')
            line = line.replace("param", '"/<int:id>"')
            line = line.replace("REPLACE_IF_JWT", '')
            o.write(line)

    else:
        for line in open("templates/resources.py"):

            if restrict_by_jwt in [True, "True"]:

                base_jwt = JWT.query.filter_by(
                    connection_name=connection_name).first()
                base_table = base_jwt.table
                db_name = base_jwt.database_name

                # fix import statements

                if line == 'from flask_jwt_extended import jwt_required\n':
                    line = 'from flask_jwt_extended import (jwt_required, create_access_token, create_refresh_token, get_jwt_identity)\n'  # noqa 501

                if line == 'from app.utils import AlchemyEncoder\n':
                    line = 'from app.utils import AlchemyEncoder, verify_jwt\n'

                verify_jwt = '        if not verify_jwt(get_jwt_identity(), ' \
                             + base_table.title() + '):\n'
                condn = '            return {"result": "JWT authorization invalid, entry does not exist."}  # noqa E401'

                line = line.replace(
                    "def post(self):",
                    "@jwt_required\n    def post(self):\n" +
                    verify_jwt +
                    condn)
                line = line.replace(
                    "def get(self, id=None):",
                    "@jwt_required\n    def get(self, id=None):\n" + verify_jwt
                    + condn)
                line = line.replace(
                    "def put(self, id):",
                    "@jwt_required\n    def put(self, id):\n" + verify_jwt
                    + condn)
                line = line.replace(
                    "def delete(self, id):",
                    "@jwt_required\n    def delete(self, id):\n" + verify_jwt
                    + condn)
                line = line.replace("param", '"/<int:id>"')
                line = line.replace(
                    "REPLACE_IF_JWT",
                    'from app.' +
                    db_name +
                    '.' +
                    base_table +
                    '.models import ' +
                    base_table.title())

            else:
                line = line.replace("\nREPLACE_IF_JWT", '')
                line = line.replace("REPLACE_IF_JWT", '')
            line = line.replace("modulename", model_name)
            line = line.replace("module_endp", model_name.title().split('.')[0])  # noqa E401
            line = line.replace("modelname", model_name.title().split('.')[1])
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
        "app.register_blueprint(mod_model, url_prefix='/" +
        model_name.replace('.', '/') + "')\n\n")
    o.close()


def check_table(table_name, connection_name=''):
    """Checks if the table exists or not"""
    exist = False
    for sorted_table in metadata.sorted_tables:
        if sorted_table.name == table_name.lower():
            if connection_name != '':
                if sorted_table.info['bind_key'] == connection_name:
                    exist = True
            else:
                exist = True
    return exist


def check_column(table_name, column_name, column_type, connection_name=''):
    """Checks if the table exists or not"""
    allowed_foreign_keys = [
        "BIGINT",
        "BINARY",
        "BOOLEAN",
        "BigInteger",
        "Binary",
        "CHAR",
        "Concatenable",
        "Enum",
        "INT",
        "INTEGER",
        "Indexable",
        "Integer",
        "Interval",
        "LargeBinary",
        "NCHAR",
        "NUMERIC",
        "NVARCHAR",
        "Numeric",
        "REAL",
        "SMALLINT",
        "SmallInteger",
    ]
    exist = False
    for sorted_table in metadata.sorted_tables:
        if sorted_table.name.lower() == table_name.lower():
            for column_ in sorted_table.columns:
                if column_name.lower() == column_.name.lower():
                    if str(column_.type) not in allowed_foreign_keys:
                        raise TypeError("Foreign key can only be allowed"
                                        " types", allowed_foreign_keys)
                    if column_type != str(column_.type):
                        raise TypeError("Foreign key and column must have "
                                        "same type.")
                    exist = True
    return exist


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

    o = open("admin/version_models.py", "a+")
    conn_name = str(conn_name).lower()
    base = "Base_" + conn_name
    column_name = "Column" + conn_name
    to_write = "\n"
    to_write = to_write + conn_name + " = SQLAlchemy(app)\n"
    to_write = to_write + base + " = " + conn_name + ".Model\n"
    to_write = to_write + column_name + " = " + conn_name + ".Column\n\n\n"
    to_write = to_write + "class AlembicVersion" + \
        conn_name.title() + "(" + base + "):\n"
    to_write = to_write + "    __tablename__ = 'alembic_version'\n"
    to_write = to_write + "    __bind_key__ = '" + conn_name + "'\n"
    to_write = to_write + "    version_num = " + \
        column_name + "(String(32), primary_key=True)\n\n"

    f = open('dbs.py', 'r+')
    lines = f.readlines()
    lines_to_write = ""
    for i, line in enumerate(lines):
        if line.startswith(']'):
            line = '    "AlembicVersion' + str(conn_name).title() + \
                '",\n' + line
        lines_to_write = lines_to_write + line

    f.seek(0)
    f.write(lines_to_write)
    o.write(to_write)


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
    add_alembic_model(conn_name)
    remove_alembic_versions()
    move_migration_files()


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
    return set(filter_keys).issubset(set(column_names))


def validate_filter_keys_jwt(filter_keys, columns):
    # check if filter keys given generate a unique set
    if "id" in filter_keys:
        return True
    for col in columns:
        if col["name"] in filter_keys:
            if str(col["unique"]).lower() == 'true' and \
                 str(col["nullable"]).lower() == 'false':
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
        return msg, valid, expiry
    except KeyError as e:
        return {"result": "Key error", "error": str(e)}, 500


def set_jwt_flag(connection_name, database_name, table_name, filter_keys):
    """Function to add the base_jwt for a connection to JWT table in default db
    """
    try:
        jwt_obj = JWT(jwt_flag=True,
                      connection_name=connection_name,
                      database_name=database_name,
                      table=table_name,
                      filter_keys=filter_keys)
        db.session.add(jwt_obj)
        db.session.commit()
    except Exception as e:
        return {"result": e}, 500


def delete_jwt(connection_name):
    try:
        db.session.query(JWT).filter(JWT.connection_name == connection_name).delete()  # noqa 501
        db.session.commit()
    except Exception as e:
        return {"result": e}, 500


def delete_restricted_by_jwt(connection_name):
    """Delete the from the jwt database if the datavase jwt is removed
    """
    try:
        db.session.query(Restricted_by_JWT).filter(Restricted_by_JWT.connection_name == connection_name).delete()  # noqa 501
        db.session.commit()
    except Exception as e:
        return {"result": e}, 500


def add_jwt_list(connection_name, database_name, table_name):
    """Function to add the restricted by JWT content(table) to the
    restrict_by_JWT table in the dafault connection
    """
    restricted_tables = Restricted_by_JWT.query.filter_by(
        connection_name=connection_name).first()
    if restricted_tables is None:
        try:
            restricted_jwt = Restricted_by_JWT(connection_name=connection_name,
                                               db_name=database_name,
                                               restricted_tables=table_name)
            db.session.add(restricted_jwt)
            db.session.commit()
        except Exception as error:
            return {"result": error}, 500

    # if the table was already in the database
    try:
        if table_name in restricted_tables.restricted_tables:
            return

        restricted_tables.restricted_tables = restricted_tables.restricted_tables + "," + table_name  # noqa E401
        try:
            db.session.commit()
        except Exception as error:
            return {"result": error}

    except AttributeError:
        pass


def create_relationsips(app_name, relation_type, related_table, related_field,
                        current_table, current_field, col_type,
                        present_relationships=""):

    directory = '/'.join(__file__.split('/')[:-2])

    try:
        if relation_type == 'one-many':
            present_relationships = present_relationships + '    ' + \
                'parent = relationship("' + \
                related_table.title() + \
                '" , backref="' + \
                current_table.lower() + \
                '")\n'

        if relation_type == 'many-many':
            class_name = related_table.title() + \
                current_table.title() + \
                related_field.title()

            right_id = related_table + "." + related_field.lower()
            left_id = current_table.lower() + "." + current_field.lower()

            assoc_string = '\n\nclass GeneratedAssociation' + class_name + \
                '(Base):\n' + \
                '    __tablename__ = "generatedAssociation' + \
                class_name + \
                '"\n' + \
                '    __bind_key__ = "' + app_name + '"\n\n' + \
                '    id = Column(Integer, primary_key=True)\n' + \
                '    left_id = Column(Text, ForeignKey("' + \
                right_id + '"))\n' + \
                '    right_id = Column(Text, ForeignKey("' + \
                left_id + '"))\n'

            f = open(directory + '/app/' + app_name + '/' +
                     current_table.lower() +
                     '/models.py', 'a')
            f.write(assoc_string)

        if relation_type == 'one-one':

            f = open(directory + '/app/' + app_name + '/' + related_table +
                     '/models.py', "r+")
            f.seek(0)
            contents = f.readlines()
            contents[-1] = present_relationships + '    ' + \
                'relation_' + related_field + ' = relationship("' + \
                related_table.title() + \
                '" ,secondary="' + \
                current_table.lower() + \
                '" , backref="' + \
                current_table.lower() + \
                '")\n'

            f.seek(0)
            f.write(''.join(contents))

        if relation_type == 'many-one':

            f = open(directory + '/app/' + app_name + '/' +
                     related_table + '/models.py', 'r+')

            f.seek(0)
            lines = f.readlines()
            f.seek(0)

            related_key = related_table.lower() + "." + related_field
            current_key = current_table.lower() + "." + current_field

            for line in lines:
                if related_field in line:
                    line = ','.join(line.split(',').insert(2, " ForeignKey('" +
                                                           current_key +
                                                           "'" + ')\n'))
                f.write(line)
            # create back_populates on the child
            present_relationships = present_relationships + '    ' + \
                'relation_' + current_filed.lower() + ' = relationship("' + \
                related_table.title() + \
                '", backref =' + '"' + \
                current_table.lower() + '")\n'
    except KeyError as err:
        raise RelatedContentNotFound("The table " +
                                     str(list(err.args)[0]) +
                                     " was not found.")

    return present_relationships
