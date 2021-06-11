import eventlet

eventlet.monkey_patch()   # noqa E402

import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)   # noqa E402

from flask import Flask, request
from flask_socketio import SocketIO, join_room

from config import NOTIF_HOST, NOTIF_PORT, JWT_SECRET_KEY

import jwt
import json


app = Flask(__name__, static_url_path="/static")
async_mode = "eventlet"


socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")


def ack():
    print("message was received!")


@socketio.on("connect")
def conn_event():
    token = request.args.get("Authorization")

    if token is None:
        token = request.headers.get("Authorization")
    if token is None:
        disconnect()
    else:
        try:
            admin = jwt.decode(token, JWT_SECRET_KEY, algorithm="HS256")
            join_room(admin["identity"]["email"])
        except Exception:
            disconnect()


@socketio.on("message")
def handleNotifications(data):
    socketio.emit("broadcast message", data["notif"], room=data["admin_id"])


@app.route("/relayMessage", methods=["POST"])
def relayMessage():
    data = json.loads(request.get_json())
    message = data["notif"]
    token = request.headers.get("Authorization")
    admin = jwt.decode(token, JWT_SECRET_KEY, algorithm="HS256")

    if token is None:
        return {"result": "Invalid admin"}, 500

    handleNotifications({"notif": message, "admin_id": admin["email"]})

    return {"result": "Successfully created notification"}, 200


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    socketio.run(app, host=NOTIF_HOST, port=NOTIF_PORT, debug=True)
