# -*- coding:utf-8 -*-
import eventlet
eventlet.monkey_patch()  # noqa E402

from flask import Flask, send_from_directory, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import SocketIO, send, emit, join_room
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy

from admin.models import Notifications, Admin
from config import NOTIF_HOST, NOTIF_PORT, JWT_SECRET_KEY

from threading import Thread, Event
import jwt

from dbs import DB_DICT

app = Flask(__name__, static_url_path='/static')
async_mode = "eventlet"

app.config['SQLALCHEMY_BINDS'] = DB_DICT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')


def ack():
    print('message was received!')


@socketio.on('connect')
def conn_event():
    token = request.args.get('Authorization')
    if token is None:
        disconnect()
    else:
        try:
            admin = jwt.decode(token, JWT_SECRET_KEY, algorithm='HS256')
            join_room(admin['identity']['email'])
        except Exception as error:
            disconnect()


@socketio.on('message')
def handleNotidications(admin_id, methods=['POST']):
    notifs_to_send = Notifications.query.filter_by(user=admin_id)
    if notifs_to_send is not None:
        for notification in notifs_to_send:
            print(notification.create_dict())
            emit('broadcast message', notification.create_dict(),
                 room=admin_id)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    socketio.run(app, host=NOTIF_HOST, port=NOTIF_PORT, debug=False)
