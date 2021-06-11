from __future__ import absolute_import

import os

from admin import utils
from admin.models.base_model_ import Model


class Sms_Notify(Model):
    def __init__(
        self,
        account_sid=None,
        auth_token=None,
        _from=None,
        to=None,
        message=None,
        errors=None,
    ):

        self.param_types = {
            "account_sid": str,
            "auth_token": str,
            "_from": str,
            "to": str,
            "message": str,
        }

        self.attribute_map = {
            "account_sid": "account_sid",
            "_from": "_from",
            "auth_token": "auth_token",
            "to": "to",
            "message": "message",
            "errors": "errors",
        }

        self._account_sid = account_sid
        self.__from = _from
        self._auth_token = auth_token
        self._to = to
        self._message = message
        self.errors = {}

    @classmethod
    def from_dict(cls, dikt) -> "Email_Notify":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Admin of this Email_Notify.
        :rtype: Email_Notify
        """
        return utils.deserialize_model(dikt, cls)

    @property
    def _from(self) -> str:
        """Gets the phone number of the Sender.


        :return: The string phone number of sender.
        :rtype: str
        """
        return self.__from

    @_from.setter
    def _from(self, _from: str):
        """Sets the phone number of the Sender.

        The phone number that will be used to send emails

        :type _from: str
        """
        # phone_regex =   # noqa 401

        if _from is None or "":
            self.errors["_from"] = (
                "Invalid value for `_from`, must not be `None`."
            )
        # if not re.match(phone_regex, _from):
        #    self.errors['_from'] = "Invalid  please re-enter a valid"\
        else:
            self.__from = _from

    @property
    def account_sid(self) -> str:
        """Gets the account_sid of the user.

        :return: The account_sid
        :rtype: str
        """
        return self._account_sid

    @account_sid.setter
    def account_sid(self, account_sid: str):
        """Sets the account_sid of the user..

        :type account_sid: str
        """
        if account_sid is None or "":
            self.errors["account_sid"] = (
                "Invalid value for `account_sid`, must not be `None`."
            )
        else:
            self._account_sid = account_sid

    @property
    def auth_token(self):
        """Gets the name and auth_token of the user and stores it as a string
           to add to the template
        """
        return self._auth_token

    @auth_token.setter
    def auth_token(self, auth_token: str):
        """Sets the auth_token of the user..

        :type auth_token: str
        """
        if auth_token is None or "":
            self.errors["auth_token"] = (
                "Invalid value for `auth_token`, must not be `None`."
            )
        else:
            self._auth_token = auth_token

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, to):

        try:

            to = str(to + "  # noqa E401")
            self._to = to

        except Exception as error:
            self.errors["to_emails"] = (
                "Please format recipient numbers properly."
            )

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    def return_result(self):
        if len(self.errors) != 0:
            return {"result": "error", "errors": self.errors, }, 500

        parent_dir = os.sep.join(__file__.split(os.sep)[:-3])
        # create folder
        Sms_Notifications = open(parent_dir + "/templates/Twilio_sms.py", "r")
        Sms_Notify_Contents = Sms_Notifications.read()
        Sms_Notifications.close()

        Sms_Notify_Contents = Sms_Notify_Contents.replace(
            "REPLACE_WITH_SID", self._account_sid
        )
        Sms_Notify_Contents = Sms_Notify_Contents.replace(
            "REPLACE_WITH_AUTH_TOKEN", self._auth_token
        )
        Sms_Notify_Contents = Sms_Notify_Contents.replace(
            "REPLACE_WITH_TO", self._to
        )
        Sms_Notify_Contents = Sms_Notify_Contents.replace(
            "REPLACE_WITH_MESSAGE", self._message
        )
        Sms_Notify_Contents = Sms_Notify_Contents.replace(
            "REPLACE_WITH_FROM", self.__from
        )

        _dir = parent_dir + "/Exports/Notifications/"

        if not os.path.exists(_dir):
            os.makedirs(_dir)

        file = open(_dir + "SmsNotifications.py", "w+")
        file.write(Sms_Notify_Contents)
        file.close()

        return {"result": "Success create SMS notification module."}, 200
