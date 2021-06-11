from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import verify_jwt

from admin.models import Admin, Notifications, Deployments

from app import db

info = Blueprint("info", __name__)
api_utils = Api()
api_utils.init_app(info)


class ListAllNotifs(Resource):
    """
    Endpoint to list all queries and their statuses
    """

    @jwt_required
    def get(self):

        admin = get_jwt_identity()

        if not verify_jwt(admin, Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )

        notifications = Notifications.query.filter_by(user=admin["email"])
        if notifications != []:
            obj = []
            for notif in notifications:
                obj.extend([notif.create_dict()])
            return obj, 200
        else:
            return ["No unread Notifications! "], 200


class MarkRead(Resource):
    """
    Endpoint to list all queries and their statuses
    """

    @jwt_required
    def post(self, section):

        admin = get_jwt_identity()

        if not verify_jwt(admin, Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )

        try:
            notif = int(section)
            notification = Notifications.query.filter_by(
                user=admin["email"], id=notif
            )
            notification.mark_read = True
            db.session.add(notification)
            db.session.commit()
            return {"response": "Marked " + str(notif) + " read"}, 200

        except ValueError:
            if section == "all":
                notifications = Notifications.query.filter_by(
                    user=admin["email"]
                )
                for notif in notifications:
                    notif.mark_read = True
                    db.session.add(notif)
                    db.session.commit()
                return {"response": "Marked All Read"}, 200

            return (
                    {
                        "response": "Invalid notification id {section} check"
                        + " url parameters.".format(section)
                    },
                    400,
            )


class DeploymentInfo(Resource):
    """Deployment information
    """

    @jwt_required
    def post(self, app_name):
        admin = get_jwt_identity()

        if not verify_jwt(admin, Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )

        deployments = Deployments.query.filter_by(app_name=app_name).all()

        result = []
        if deployments is None:
            return result

        for dep in deployments:
            i = dep.__dict__
            del i["_sa_instance_state"]
            result.append(dep.__dict__)

        print(result)
        return jsonify(result)


api_utils.add_resource(DeploymentInfo, "/deployment_info/<app_name>")
api_utils.add_resource(ListAllNotifs, "/allrequests")
api_utils.add_resource(MarkRead, "/markread/<section>")
