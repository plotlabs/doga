from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import verify_jwt

from admin.models import Admin, Notifications
from admin.utils import *

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
            return {"result": "JWT authorization invalid, user does not"
                    " exist."}, 401

        notifications = Notifications.query.filter_by(user=admin['email'],
                                                      mark_read="False")
        if notifications != []:
            obj = []
            for notif in notifications:
                obj.extend([notif.create_dict()])
            return obj, 200
        else:
            return ['No unread Notifications! '], 200


class MarkRead(Resource):
    """
    Endpoint to list all queries and their statuses
    """
    @jwt_required
    def post(self, section):

        admin = get_jwt_identity()

        if not verify_jwt(admin, Admin):
            return {"result": "JWT authorization invalid, user does not"
                    " exist."}, 401

        try:
            notif = int(section)
            notification = Notifications.query.filter_by(user=admin['email'],
                                                         id=notif)
            notification.mark_read()
            db.session.add(notification)
            db.session.commit()
            return {"response": "Marked " + str(notif) + " read"}, 200

        except ValueError:
            if section == 'all':
                notifications = Notifications.query.filter_by(
                                                        user=admin['email'])
                for notif in notifications:
                    notif.mark_read()
                    db.session.add(notif)
                    db.session.commit()
                return {"response": "Marked All Read"}, 200
            else:
                return {"response": "Invalid <section> check url parameters."}, 400
        return


api_utils.add_resource(ListAllNotifs, '/allrequests/')
api_utils.add_resource(MarkRead, '/markread/<section>')
