import requests
import jwt
import json

from datetime import datetime as dt

from admin.module_generator import *

from config import NOTIF_HOST, NOTIF_PORT, JWT_SECRET_KEY


def triggerSocketioNotif(admin_id, token, notification):

    token = jwt.encode({"email": admin_id}, JWT_SECRET_KEY,
                       algorithm='HS256')

    request = requests.post('http://{}:{}/relayMessage'.format(NOTIF_HOST,
                                                               NOTIF_PORT),
                            json=json.dumps({'notif': notification}),
                            headers={"Authorization": token})


def create_contet_thread(data, admin_jwt, Table, base_jwt, restrict_by_jwt, notification):

    dir_path = create_dir(Table.connection_name + "/" + Table.table_name)

    isExisting = os.path.isfile(dir_path)

    if isExisting:
        return {"result": "Content must be unique for databases with the"
                " same name."}

    if restrict_by_jwt:
        add_jwt_list(Table.connection_name,
                        Table.table_name)

    create_model(dir_path, data)
    create_resources(Table.connection_name + "." + Table.table_name,
                        Table.connection_name,
                        dir_path,
                        base_jwt,
                        data.get("expiry", {}),
                        restrict_by_jwt,
                        data.get("filter_keys", []))
    append_blueprint(Table.connection_name + "." + Table.table_name)
    remove_alembic_versions()
    move_migration_files()
    notification.action_status = 'SUCCESS'
    notification.message = 'Resources Created Successfully'
    notification.completed_action_at = dt.now()
    db.session.add(notification)
    db.session.commit()
    triggerSocketioNotif(admin_jwt['email'], "", notification.create_dict())
