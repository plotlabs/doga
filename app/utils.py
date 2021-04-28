from datetime import datetime

import json
import os
import platform
import subprocess

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy import inspect


class AlchemyEncoder(json.JSONEncoder):
    """A JSON encoder that takes a sqlalchemy result object and converts it
    into a JSON encodable dict of the form 'column': 'value' using the model
    information.
    """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}

            for field in [x for x in dir(obj) if not x.startswith('_') and
                          x != 'metadata']:
                data = obj.__getattribute__(field)

                if field in ["password", "keys", "query", "query_class",
                             "two_fa_key"]:
                    pass
                else:
                    try:
                        json.dumps(data)
                        fields[field] = data
                    except TypeError:
                        if 'models' in str(type(data)):
                            relationship = inspect(data).mapper.relationship
                            relation_name = relation.direction.name.split("TO")
                            realted_table = data.__table__.name.title()
                            related_value = {c.key: str(getattr(data, c.key))
                                             for c in
                                             inspect(data).mapper.column_attrs}
                            rel["relation_name"] = relation_name
                            fields["related_value"] = related_value
                            fields["related_table"] = realted_table
                        elif isinstance(data, InstrumentedList):
                            relationships = inspect(data[0]).mapper.relationships
                            rel = {}
                            for relation in relationships:
                                relation_name = relation.direction.name.split("TO")
                                relation_name.insert(1, "TO")
                                if data[0].__table__.name in \
                                        str(relation._reverse_property) or \
                                        field in \
                                        str(relation._reverse_property):
                                    realted_table = data[0].__table__.name.title()
                                    realted_values = []
                                    for item in data:
                                        realted_values.append({
                                            c.key: str(getattr(item, c.key))
                                            for c in
                                            inspect(item).mapper.column_attrs
                                        })

                                    rel["relation_name"] = relation_name
                                    rel["realted_table"] = realted_table
                                    rel["realted_values"] = realted_values
                            try:
                                fields["related_content"].append(rel)
                            except KeyError:
                                fields["related_content"] = [rel]
                        else:
                            fields[field] = str(data)
            return fields
        return json.JSONEncoder.default(self, obj)


def verify_jwt(jwt_identity, model):

    query = model.query

    for key, value in jwt_identity.items():
        query = query.filter(getattr(model, key).like("%%%s%%" % value))

    final_result = query.all()
    if final_result is None:
        return False
    return True


def migrate():
    """Function to stop the app to migrate and then restart it."""
    migrate_folder = os.path.exists('migrations')
    if not migrate_folder:
        subprocess.check_output('flask db init --multidb', shell=True)
    pid = os.getpid()
    revision_id = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    migrate_command = "flask db migrate --rev-id " + revision_id
    upgrade_command = "flask db upgrade"
    sys_platform = platform.system()
