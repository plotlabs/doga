from __future__ import absolute_import

import re

from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from admin import utils
from admin.models.base_model_ import Model


class Admin(Model):
    def __init__(
        self, email: str = None, password: str = None, name: str = None
    ):  # noqa: E501
        """Admin

        :param email: The email of this Admin.
        :type  email: str

        :param password: The password of this Admin.
        :type  password: str

        :param name: The name of this Admin.
        :type  name: str
        """

        self.param_types = {"email": str, "password": str, "name": str}

        self.attribute_map = {
            "email": "email",
            "password": "password",
            "name": "name",
        }

        self._email = email
        self._password = password
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> "Admin":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Admin of this Admin.
        :rtype: Admin
        """
        return utils.deserialize_model(dikt, cls)

    @property
    def email(self) -> str:
        """Gets the email of this Admin.

        The email-id the admin will use to login

        :return: The email of this Admin.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this Admin.

        The email-id the admin will use to login

        :param email: The email of this Admin.
        :type email: str
        """
        email_regex = (
            "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"  # noqa 401
        )

        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`.")
        if not re.match(email_regex, email):
            raise ValueError(
                "Invalid email id, please re-enter a valid email address"
            )

        self._email = email

    @property
    def password(self) -> str:
        """Gets the password of this Admin.

        Password that the admin will use to login

        :return: The password of this Admin.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this Admin.

        Password that the admin will use to login

        :param password: The password of this Admin.
        :type password: str
        """
        if password is None:
            raise ValueError(
                "Invalid value for `password`, must not be `None`."
            )
        if password is not None and len(password) > 32:
            raise ValueError(
                "Invalid value for `password`, length must be"
                " less than or equal to `32`."
            )
        if password is not None and len(password) < 6:
            raise ValueError(
                "Invalid value for `password`, length must be "
                "greater than or equal to `6`."
            )

        self._password = password

    @property
    def name(self) -> str:
        """Gets the name of this Admin.

        This is the name of the admin

        :return: The name of this Admin.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Admin.

        This is the name of the admin

        :param name: The name of this Admin.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`.")
        if name is not None and len(name) > 32:
            raise ValueError(
                "Invalid value for `name`, length must be less. "
                "than or equal to `32`"
            )
        if name is not None and len(name) < 4:
            raise ValueError(
                "Invalid value for `name`, length must be greater"
                " than or equal to `4`."
            )

        self._name = name
