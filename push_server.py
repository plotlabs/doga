# -*- coding:utf-8 -*-
import eventlet
eventlet.monkey_patch()  # noqa E402

from flask import Flask, send_from_directory, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy

from admin.models import Notifications, Admin
from config import NOTIF_HOST, NOTIF_PORT

from dbs import DB_DICT

app = Flask(__name__, static_url_path='/static')
async_mode = "eventlet"

app.config['SQLALCHEMY_BINDS'] = DB_DICT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')


@socketio.on('message')
def handleNotidications(admin_id):
    notifs_to_send = Notifications.query.filter_by(user=admin_id)
    notifs = []
    if notifs is not None:
        for notification in notifs_to_send:
            print(here)
            notifs = notifs.append(notification.foramt_notification())
            notification.mark_read(True)
        send(notifs)
    send(['No Notifications'])
    db.session.commit()


@socketio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    socketio.run(app, host=NOTIF_HOST, port=NOTIF_PORT, debug=True)