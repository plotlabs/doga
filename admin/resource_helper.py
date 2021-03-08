import socketio
import jwt

from config import JWT_SECRET_KEY


def triggerSocketioNotif(admin_id, token):
    sio = socketio.Client()

    token = jwt.encode({"id": admin_id}, JWT_SECRET_KEY,
                       algorithm='HS256')
    sio.connect('http://localhost:8008/', headers={
                "Authorization": token})
    sio.wait()
    sio.emit('message', {'admin_id': admin_id})
