from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import verify_jwt

from admin.models import Notifications
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
        notifications = {}
        return


class MarkRead(Resource):
    """
    Endpoint to list all queries and their statuses
    """
    @jwt_required
    def post(self, notif):
        return


api_utils.add_resource(ListAllNotifs, '/allrequests/')
api_utils.add_resource(MarkRead, '/markread/<section>')
