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

from threading import Thread, Event

from dbs import DB_DICT

app = Flask(__name__, static_url_path='/static')
async_mode = "eventlet"

app.config['SQLALCHEMY_BINDS'] = DB_DICT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')


thread = Thread()
thread_stop_event = Event()


def NotificationThread(admin_id):
    print("looking for admin notifs ...")
    while not thread_stop_event.is_set():
        notifs_to_send = Notifications.query.filter_by(user=admin_id,
                                                       mark_read=False)
        if notifs_to_send is not None:
            for notification in notifs_to_send:
                socket.emit('message', notification.create_dict())
                socketio.sleep(2)


def ack():
    print('message was received!')


@socketio.on('connect')
def conn_event():
    send('ack', callback=ack)


@socketio.on('message')
def handleNotidications(admin_id):
    global thread

    if not thread.is_alive():
        print('Starting a Thread')
        thread = socketio.start_background_task(NotificationThread(admin_id))


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host=NOTIF_HOST, port=NOTIF_PORT, debug=True)
