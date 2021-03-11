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
