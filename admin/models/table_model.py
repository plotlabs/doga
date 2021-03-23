from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401

import re

from typing import List, Dict  # noqa: F401

from admin import utils
from admin.models.base_model_ import Model
from admin.models.column_model import Column

from dbs import DB_DICT


class Table(Model):

    def __init__(self, table_name: str = None,
                 connection_name: str = None,
                 columns: List[Column] = None):
        """Table - a model used to wrap the json object defining content

        :param table_name: The table_name of this Table.
        :type table_name: str

        :param connection_name: The connection_name of this Table.
        :type connection_name: str

        :param columns: The columns of this Table.
        :type columns: List[Column]
        """
        self.param_types = {
            'table_name': str,
            'connection_name': str,
            'columns': List[Column]
        }

        self.attribute_map = {
            'table_name': 'table_name',
            'connection_name': 'connection_name',
            'columns': 'columns'
        }

        self._table_name = table_name
        self._connection_name = connection_name
        self._columns = columns

    @classmethod
    def from_dict(cls, dikt) -> 'Table':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Table of this Table.
        :rtype: Table
        """
        return utils.deserialize_model(dikt, cls)

    @property
    def table_name(self) -> str:
        """Gets the table_name of this Table.


        :return: The table_name of this Table.
        :rtype: str
        """
        return self._table_name

    @table_name.setter
    def table_name(self, table_name: str):
        """Sets the table_name of this Table.


        :param table_name: The table_name of this Table.
        :type table_name: str
        """
        if table_name is None:
            raise ValueError("Invalid value for `table_name`, must not"
                             " be `None`")
        if table_name is not None and len(table_name) > 32:
            raise ValueError("Invalid value for `table_name`, length must be"
                             " less than or equal to `32`.")
        if table_name is not None and table_name.isspace() is True:
            raise ValueError("Invalid value for `table_name`, must contain "
                             "characters")
        if not re.match("^[a-z0-9_]+$", table_name):
            raise ValueError("Invalid value for `table_name`m mist contain"
                             " only alphabets, numbers and -")

        self._table_name = table_name.lower()

    @property
    def connection_name(self) -> str:
        """Gets the connection_name of this Table.


        :return: The connection_name of this Table.
        :rtype: str
        """
        return self._connection_name

    @connection_name.setter
    def connection_name(self, connection_name: str):
        """Sets the connection_name of this Table.


        :param connection_name: The connection_name of this Table.
        :type connection_name: str
        """
        if connection_name is None:
            raise ValueError("Invalid value for `connection_name`, must not"
                             " be `None`")
        if connection_name not in DB_DICT:
            raise ValueError("The database connection given does not exist.")

        self._connection_name = connection_name

    @property
    def columns(self) -> List[Column]:
        """Gets the columns of this Table.


        :return: The columns of this Table.
        :rtype: List[Column]
        """
        return self._columns

    @columns.setter
    def columns(self, columns: List[Column]):
        """Sets the columns of this Table.


        :param columns: The columns of this Table.
        :type columns: List[Column]
        """
        if columns is None:
            raise ValueError("Invalid value for `columns`, must not be `None`")
        if len(columns) < 1:
            raise ValueError("At least one column is required.")

        self._columns = columns
