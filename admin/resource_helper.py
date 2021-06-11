import requests
import jwt
import json

from datetime import datetime as dt

from admin.module_generator import *
from admin.models import Notifications
from admin.export.exportapp import (
    create_app_dir,
    write_to_deployments,
)
from admin.export.utils import *

from config import NOTIF_HOST, NOTIF_PORT, JWT_SECRET_KEY


def triggerSocketioNotif(admin_id, notification):

    token = jwt.encode({"email": admin_id}, JWT_SECRET_KEY, algorithm="HS256")

    try:
        requests.post(
            "http://{}:{}/relayMessage".format(NOTIF_HOST, NOTIF_PORT),
            json=json.dumps({"notif": notification}),
            headers={"Authorization": token},
        )
    except ConnectionError:
        print("ERROR: Please check the notification server!")


def create_contet_thread(
    data, admin_jwt, table_, base_jwt, restrict_by_jwt, notification
):

    dir_path = create_dir(table_.connection_name + "/" + table_.table_name)

    dir_exists = os.path.isfile(dir_path)

    if dir_exists:
        return {
            "result": "Content must be unique for databases with the"
            " same name."
        }

    if restrict_by_jwt:
        add_jwt_list(table_.connection_name, table_.table_name)

    create_model(dir_path, data)
    create_resources(
        table_.connection_name + "." + table_.table_name,
        table_.connection_name,
        dir_path,
        base_jwt,
        data.get("expiry", {}),
        restrict_by_jwt,
        data.get("filter_keys", []),
    )
    append_blueprint(table_.connection_name + "." + table_.table_name)
    remove_alembic_versions()
    move_migration_files()
    notification.action_status = "SUCCESS"
    notification.message = "Resources Created Successfully"
    notification.completed_action_at = dt.now()
    db.session.add(notification)
    db.session.commit()
    triggerSocketioNotif(admin_jwt["email"], notification.create_dict())


def create_aws_deployment_thread(
    user_credentials,
    config,
    app_name,
    json_request,
    notification,
    admin_jwt,
    platform="aws",
):

    while True:
        try:
            rds = create_rds(
                user_credentials,
                config,
                app_name,
                **json_request["rds_config"]
            )
        except RDSCreationError as error:
            notification.action_status = "ERROR"
            notification.message = str(error)
            notification.completed_action_at = dt.now()
            db.session.add(notification)
            db.session.commit()
            triggerSocketioNotif(
                admin_jwt["email"], notification.create_dict()
            )
            break

        notification = Notifications(
            user=admin_jwt["email"],
            app_name=json_request["app_name"],
            action_type="deploy-app",
            action_status="PROCESSING",
            message="RDS Created Successfully",
            completed_action_at=dt.now(),
        )
        db.session.add(notification)
        db.session.commit()
        triggerSocketioNotif(
            admin_jwt["email"], notification.create_dict()
        )

        try:
            key_pair, sg_name, ec2, vpc_sg, ec2_platform = create_ec2(
                user_credentials,
                config,
                rds["Endpoint"]["Port"],
                **json_request["ec2_config"]
            )

        except EC2CreationError as error:
            notification.action_status = "ERROR"
            notification.message = str(error)
            notification.completed_action_at = dt.now()
            db.session.add(notification)
            db.session.commit()
            triggerSocketioNotif(
                admin_jwt["email"], notification.create_dict()
            )
            break

        notification = Notifications(
            user=admin_jwt["email"],
            app_name=json_request["app_name"],
            action_status="PROCESSING",
            action_type="deploy-app",
            message="EC2 Created Successfully",
            completed_action_at=dt.now(),
        )
        db.session.add(notification)
        db.session.commit()
        triggerSocketioNotif(
            admin_jwt["email"], notification.create_dict()
        )

        try:
            rds["MasterUserPassword"] = json_request["rds_config"][
                "MasterUserPassword"
            ]
            create_app_dir(app_name, rds, user_credentials, config, platform)
        except DogaDirectoryCreationError as error:
            notification.action_status = "ERROR"
            notification.message = (
                "Could not create files for the exported" + str(error)
            )
            db.session.add(notification)
            db.session.commit()
            triggerSocketioNotif(
                admin_jwt["email"], notification.create_dict()
            )
            break

        ec2 = deploy_to_aws(
            user_credentials, config, ec2, key_pair, ec2_platform
        )

        notification = Notifications(
            user=admin_jwt["email"],
            app_name=json_request["app_name"],
            action_status="PROCESSING",
            action_type="deploy-app",
            message="App uploaded to EC2 instance successfully.",
            completed_action_at=dt.now(),
        )
        db.session.add(notification)
        db.session.commit()
        triggerSocketioNotif(
            admin_jwt["email"], notification.create_dict()
        )

        try:
            response = connect_rds_to_ec2(
                rds,
                ec2,
                user_credentials,
                config,
                sg_name,
                vpc_sg,
                ec2_platform,
                key_pair,
            )

        except DogaEC2toRDSconnectionError as error:
            notification = Notifications(
                message="Could not create a connection between "
                "EC2"
                + ec2.id
                + " and "
                + rds["DBInstanceIdentifier"]
                + str(error),
                app_name=app_name,
                action_status="ERROR",
                action_type="deploy-app",
                completed_action_at=dt.now(),
            )
            db.session.add(notification)
            db.session.commit()
            triggerSocketioNotif(
                admin_jwt["email"], notification.create_dict()
            )
            break

        notification = Notifications(
            user=admin_jwt["email"],
            app_name=json_request["app_name"],
            action_status="SUCCESSFUL",
            action_type="deploy-app",
            message="App deployed to EC2 " + ec2.id + " successfully.",
            completed_action_at=dt.now(),
        )
        db.session.add(notification)
        db.session.commit()
        triggerSocketioNotif(
            admin_jwt["email"], notification.create_dict()
        )

        write_to_deployments(app_name, "aws", ec2.public_dns_name)

        notification_f = Notifications(
            user=admin_jwt["email"],
            app_name=json_request["app_name"],
            action_status="COMPLETED",
            action_type="deploy-app",
            message="App at EC2 " + ec2.id + " is now Active.",
            completed_action_at=dt.now(),
        )
        db.session.add(notification_f)
        db.session.commit()
        triggerSocketioNotif(
            admin_jwt["email"], notification_f.create_dict()
        )
        return
