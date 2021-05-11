from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401
import re

from admin import utils
from admin.models.base_model_ import Model


class Column(Model):
    def __init__(
        self,
        name: str = None,
        type: str = None,
        unique: bool = None,
        default: str = None,
        foreign_key: str = None,
        nullable: bool = None,
    ):
        """Column

        :param default: The default of this Column.
        :type default: str

        :param foreign_key: The foreign_key of this Column.
        :type foreign_key: str

        :param name: The name of this Column.
        :type name: str

        :param nullable: The nullable of this Column.
        :type nullable: bool

        :param type: The type of this Column.
        :type type: str

        :param unique: The unique of this Column.
        :type unique: bool
        """
        self.param_types = {
            "default": str,
            "foreign_key": str,
            "name": str,
            "nullable": bool,
            "type": str,
            "unique": bool,
        }

        self.attribute_map = {
            "default": "default",
            "foreign_key": "foreign_key",
            "name": "name",
            "nullable": "nullable",
            "type": "type",
            "unique": "unique",
        }

        self._default = default
        self._foreign_key = foreign_key
        self._name = name
        self._nullable = nullable
        self._type = type
        self._unique = unique

    @classmethod
    def from_dict(cls, dikt) -> "Column":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Column of this Column.
        :rtype: Column
        """
        return utils.deserialize_model(dikt, cls)

    @property
    def default(self) -> str:
        """Gets the default of this Column.


        :return: The default of this Column.
        :rtype: str
        """
        return self._default

    @default.setter
    def default(self, default: str):
        """Sets the default of this Column.


        :param default: The default of this Column.
        :type default: str
        """
        self._default = default

    @property
    def foreign_key(self) -> str:
        """Gets the foreign_key of this Column.


        :return: The foreign_key of this Column.
        :rtype: str
        """
        return self._foreign_key

    @foreign_key.setter
    def foreign_key(self, foreign_key: str):
        """Sets the foreign_key of this Column.


        :param foreign_key: The foreign_key of this Column.
        :type foreign_key: str
        """

        self._foreign_key = foreign_key

    @property
    def name(self) -> str:
        """Gets the name of this Column.


        :return: The name of this Column.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Column.


        :param name: The name of this Column.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for column name, `name` must not be `None`"
            )
        if name is not None and len(name) > 32:
            raise ValueError(
                "Invalid value for column `name`, length must be"
                " less than or equal to `32`."
            )
        if name is not None and len(name) < 1:
            raise ValueError(
                "Invalid value for column `name`, length must be "
                "greater than or equal to `6`."
            )
        if not re.match("^([a-z]+[0-9_]*)*$", name):
            raise ValueError(
                "Invalid value for column_name: {}, must contain"
                " only alphabets, numbers and _".format(name)
            )

        self._name = name.lower()

    @property
    def nullable(self) -> bool:
        """Gets the nullable of this Column.


        :return: The nullable of this Column.
        :rtype: bool
        """
        return self._nullable

    @nullable.setter
    def nullable(self, nullable: bool):
        """Sets the nullable of this Column.


        :param nullable: The nullable of this Column.
        :type nullable: bool
        """
        if nullable is None:
            raise ValueError(
                "Invalid value for `nullable`, must not be `None`"
            )

        self._nullable = nullable

    @property
    def type(self) -> str:
        """Gets the type of this Column.


        :return: The type of this Column.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Column.


        :param type: The type of this Column.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

    @property
    def unique(self) -> bool:
        """Gets the unique of this Column.


        :return: The unique of this Column.
        :rtype: bool
        """
        return self._unique

    @unique.setter
    def unique(self, unique: bool):
        """Sets the unique of this Column.


        :param unique: The unique of this Column.
        :type unique: bool
        """
        if unique is None:
            raise ValueError("Invalid value for `unique`, must not be `None`")

        self._unique = unique
