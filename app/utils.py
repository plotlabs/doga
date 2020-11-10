from datetime import datetime

import json
import os
import platform
import subprocess

from sqlalchemy.ext.declarative import DeclarativeMeta


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
                        fields[field] = str(data)
            return fields
        return json.JSONEncoder.default(self, obj)


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


"""
    if sys_platform in ['Linux', 'Darwin']:
        run_command = "sh restart.sh"
    else:
        run_command = "start "" /b restart.bat"
    if pid != '':
        os.system(migrate_command + " && " + upgrade_command + " && "
                  + run_command + " " + str(pid))
"""


def verify_jwt(jwt_identity, filter_key, model_name):

    query = model_name.query

    for key, value in jwt_identity.items():
        query = query.filter(getattr(model_name, key).like("%%%s%%" % value))

    final_result = query.all()
    if final_result is None:
        return False
    return True
