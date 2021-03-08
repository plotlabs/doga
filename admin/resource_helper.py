import socketio
import jwt

from config import JWT_SECRET_KEY

@sio.event
def connect():
    print('connection established')


def triggerSocketioNotif(admin_id, token):
    sio = socketio.Client()

    token = jwt.encode({"id": admin_id}, JWT_SECRET_KEY,
                       algorithm='HS512')
    sio.connect('http://localhost:8008/', headers={
                "Authorization": token})
    sio.wait()
    sio.emit('message', {'admin_id': admin_id})
