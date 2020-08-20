import secrets
import string
import random

from dbs import DB_DICT


def generate_secret_key():
    """ generating secret key for jwt """
    length = random.randint(7, 15)
    # length of secret key in range [7,15]
    res = ''.join(secrets.choice(string.ascii_uppercase +
                                 string.ascii_lowercase + string.digits)
                  for i in range(length))
    return res


def set_jwt_secret_key():
    """ setting jwt in app config """
    jwt_secret_key = generate_secret_key()
    o = open("./config.py", "a")
    o.write("JWT_SECRET_KEY = ' " + jwt_secret_key + "'\n")
    o.close()


def extract_database_name(connection_name):
    """ extracting database name based on connection name """
    connection_string = DB_DICT[connection_name]
    start = connection_string.rfind('/')
    if connection_string.startswith("mysql"):
        end = connection_string.rfind('?')
    elif connection_string.startswith("postgresql"):
        end = len(connection_string)
    else:
        end = connection_string.rfind('.db')

    return connection_string[start+1:end]
