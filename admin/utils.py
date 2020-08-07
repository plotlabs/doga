import secrets
import string
import random
from app import app
from dbs import DB_DICT


def generate_secret_key():
    N = random.randint(7, 15)
    # length of key in range [7,15]
    res = ''.join(secrets.choice(string.ascii_uppercase +
                                 string.ascii_lowercase + string.digits)
                  for i in range(N))
    return res


def set_jwt_secret_key():
    JWT_SECRET_KEY = generate_secret_key()
    o = open("./config.py", "a")
    o.write("JWT_SECRET_KEY = " + str(JWT_SECRET_KEY) + "\n")
    o.close()


def extract_database_name(connection_name):
    connection_string = DB_DICT[connection_name]
    start = connection_string.rfind('/')
    if connection_string.startswith("mysql"):
        end = connection_string.rfind('?')
    elif connection_string.startswith("postgresql"):
        end = len(connection_string)
    else:
        end = connection_string.rfind('.db')

    return connection_string[start+1:end]
