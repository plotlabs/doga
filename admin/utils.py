import secrets
import string
import random
from app import app


def generate_secret_key():
    N = random.randint(7, 15) #length of key in range [7,15]
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                  for i in range(N))
    return res


def set_jwt_secret_key():
    app.config['JWT_SECRET_KEY'] = generate_secret_key()
