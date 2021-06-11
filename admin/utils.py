import datetime
import random
import secrets
import six
import string

from dbs import DB_DICT
from config import JWTSET


def generate_secret_key():
    """ generating secret key for jwt """
    length = random.randint(7, 15)
    # length of secret key in range [7,15]
    res = "".join(
        secrets.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for i in range(length)
    )
    return res


def set_jwt_secret_key():
    """ Sets JWT in app config file """
    if JWTSET:
        return
    jwt_secret_key = generate_secret_key()
    o = open("./config.py", "a")
    o.write("JWT_SECRET_KEY = '" + jwt_secret_key + "'\n")
    o.close()

    with open("./config.py", "r") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("JWTSET = False", "JWTSET = True")

    # Write the file out again
    with open("./config.py", "w") as file:
        file.write(filedata)


def extract_database_name(connection_name):
    """ extracting database name based on connection name """
    connection_string = DB_DICT[connection_name]
    start = connection_string.rfind("/")
    if connection_string.startswith("mysql"):
        end = len(connection_string)
    elif connection_string.startswith("postgresql"):
        end = len(connection_string)
    else:
        end = connection_string.rfind(".db")
    return connection_string[start + 1 : end]


def _deserialize_dict(data, boxed_type):
    """Deserializes a dict and its elements.

    :param data: dict to deserialize.
    :type data: dict
    :param boxed_type: class literal.

    :return: deserialized dict.
    :rtype: dict
    """
    return {k: _deserialize(v, boxed_type) for k, v in six.iteritems(data)}


def deserialize_model(data, klass):
    """Deserializes list or dict to model.

    Parameters:
    -----------
    - data:
      type: dict or list
    - klass:
      type: class literal.

    Returns:
    -------
    returns : model object.
    """
    instance = klass()
    if not instance.param_types:
        return data

    for attr, attr_type in six.iteritems(instance.param_types):
        if (
            data is not None
            and instance.attribute_map[attr] in data
            and isinstance(data, (list, dict))
        ):
            value = data[instance.attribute_map[attr]]
            setattr(instance, attr, _deserialize(value, attr_type))

    return instance


def _deserialize(data, klass):
    """Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None

    if klass in six.integer_types or klass in (float, str, bool):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return deserialize_date(data)
    elif klass == datetime.datetime:
        return deserialize_datetime(data)
    elif hasattr(klass, "__origin__"):
        if klass.__origin__ == list:
            return _deserialize_list(data, klass.__args__[0])
        if klass.__origin__ == dict:
            return _deserialize_dict(data, klass.__args__[1])
    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """Deserializes to primitive type.

    Parameters:
    -----------
    - data:
      description: data to deserialize.
    - klass: class literal.
      description: the class that the data is extracted from

    Returns:
    -------
    - int, long, float, str, bool.
      type: int | long | float | str | bool
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = six.u(data)
    except TypeError:
        value = data
    return value


def _deserialize_list(data, boxed_type):
    """Deserializes a list and its elements.

    Parameters:
    -----------
    - data:
      description: list to deserialize.
      type: list
    - boxed_type
      type: class literal.

    Returns:
    -------
    - deserialized list.
      type: list
    """
    return [_deserialize(sub_data, boxed_type) for sub_data in data]
