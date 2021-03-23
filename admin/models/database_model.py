from __future__ import absolute_import
from datetime import date, datetime

from typing import List, Dict

import re

from admin import utils
from admin.models.base_model_ import Model

from dbs import DB_DICT
from admin.default_values import DEFAULT_PORTS


class Database(Model):

    def __init__(self,
                 database_name: str = None,
                 connection_name: str = None,
                 database_type: str = None,
                 host: str = None,
                 port: str = None,
                 username: str = None,
                 password: str = None):
        """Database - a model defined to wrap incoming db connections

        :database_name: The database_name that we would like to create
        :type database_name: str

        :param connection_name: The connection_name of this Database.
        :type connection_name: str

        :param database_type: The database_type of this Database.
        :type database_type: str

        :param host: The host of this Database.
        :type host: str

        :param port: The port of this Database.
        :type port: str

        :param username: The username of this Database.
        :type username: str

        :param password: The password of this Database.
        :type password: str
        """
        self.param_types = {
            'database_name': str,
            'connection_name': str,
            'database_type': str,
            'host': str,
            'port': str,
            'username': str,
            'password': str
        }

        self.attribute_map = {
            'database_name': 'database_name',
            'connection_name': 'connection_name',
            'database_type': 'database_type',
            'host': 'host',
            'port': 'port',
            'username': 'username',
            'password': 'password'
        }

        self._database_name = database_name
        self._connection_name = connection_name
        self._database_type = database_type
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'Database':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict

        :return: The Database of this Database.
        :rtype: Database
        """
        return utils.deserialize_model(dikt, cls)

    @property
    def database_name(self) -> str:
        """Gets the database_name for the object

        :return: The database_name associateed with the object
        :rtype: str
        """
        return self._database_name

    @database_name.setter
    def database_name(self, database_name: str):
        """Sets the database_name

        :param database_name:
        :rtype: str
        """
        if database_name in [None, ""]:
            raise ValueError("Invalid value for `database_name`, must not be"
                             " `None`")
        self._database_name = database_name

    @property
    def connection_name(self) -> str:
        """Gets the connection_name of this Database.


        :return: The connection_name of this Database.
        :rtype: str
        """
        return self._connection_name

    @connection_name.setter
    def connection_name(self, connection_name: str):
        """Sets the connection_name of this Database.


        :param connection_name: The connection_name of this Database.
        :type connection_name: str
        """
        if connection_name is None or "":
            raise ValueError("Invalid value for `connection_name`, must not be"
                             " `None`")
        if connection_name in DB_DICT:
            raise ValueError("Connection with name: {} is already present. Use"
                             " a different name.".format(connection_name))
        if not re.match("^([a-z]+[0-9_]*)*$", connection_name):
            raise ValueError("Connection with name: {} cannot be created. Use"
                             "lowercase alphabet, numbers and '-' only")

        self._connection_name = connection_name

    @property
    def database_type(self) -> str:
        """Gets the database_type of this Database.


        :return: The database_type of this Database.
        :rtype: str
        """
        return self._database_type

    @database_type.setter
    def database_type(self, database_type: str):
        """Sets the database_type of this Database.


        :param database_type: The database_type of this Database.
        :type database_type: str
        """
        allowed_values = ["mysql", "sqlite", "postgres"]
        if (database_type not in allowed_values) or (database_type == "None"):
            raise ValueError(
                "Invalid value for `database_type` ({0}), must be one of {1}"
                .format(database_type, allowed_values)
            )

        self._database_type = database_type

    @property
    def host(self) -> str:
        """Gets the host of this Database.


        :return: The host of this Database.
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host: str):
        """Sets the host of this Database.


        :param host: The host of this Database.
        :type host: str
        """
        if host in [None, 'None', ""]:
            host = "localhost"

        self._host = host

    @property
    def port(self) -> str:
        """Gets the port of this Database.


        :return: The port of this Database.
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port: str):
        """Sets the port of this Database.


        :param port: The port of this Database.
        :type port: str
        """
        if port in [None, '', 'None']:
            port = DEFAULT_PORTS[self.database_type]
            """
            except KeyError:
                raise ValueError("No default port value for `database_type`"
                                 " {0}, please specity in request.".format(
                                  self.database_type))
            """
        self._port = port

    @property
    def username(self) -> str:
        """Gets the username of this Database.


        :return: The username of this Database.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this Database.


        :param username: The username of this Database.
        :type username: str
        """
        if username is None:
            username = ""

        self._username = username

    @property
    def password(self) -> str:
        """Gets the password of this Database.


        :return: The password of this Database.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this Database.


        :param password: The password of this Database.
        :type password: str
        """
        if password is None:
            password = ""

        self._password = password

    def db_string(self) -> str:
        string = ''
        if self.database_type == 'mysql':
            string = 'mysql://{}:{}@{}:{}/{}'.format(
                self.username, self.password, self.host,
                self.port, self.database_name)

        if self.database_type == 'postgres':
            string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
                self.username, self.password, self.host,
                self.port, self.database_name.lower())

        if self.database_type == 'sqlite':
            string = 'sqlite:////tmp/{}.db'.format(
                self.database_name)
            # data['host'],data['database_name'])
        return string
