import requests
import jwt
import json

from config import NOTIF_HOST, NOTIF_PORT, JWT_SECRET_KEY


def triggerSocketioNotif(admin_id, token, notification):

    token = jwt.encode({"email": admin_id}, JWT_SECRET_KEY,
                       algorithm='HS256')

    request = requests.post('http://{}:{}/relayMessage'.format(NOTIF_HOST,
                                                               NOTIF_PORT),
                            json=json.dumps({'notif': notification}),
                            headers={"Authorization": token})

    """
    sio.connect('http://localhost:8008', headers={
                "Authorization": token})

    @sio.on('message')
    async def message(data, admin_id=admin_id):
        await sio.emit('message', {'admin_id': admin_id, 'data': data})
    """

    print(request)


    # message(notification, admin_id)
