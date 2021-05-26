from __future__ import absolute_import

import ast

import os
import re

import json
from json import JSONDecodeError

from admin import utils
from admin.models.base_model_ import Model


class Email_Notify(Model):
    def __init__(
        self,
        api_key=None,
        _from=None,
        to_emails=None,
        template_key=None,
        subject=None,
        content=None,
        errors=None,
    ):
        """Email_Notify

        api_key
        _from
        to_emails
        template_key
        subject
        content
        """

        self.param_types = {
            "api_key": str,
            "_from": str,
            "to_emails": str,
            "template_key": str,
            "subject": str,
            "content": str,
        }

        self.attribute_map = {
            "api_key": "api_key",
            "_from": "_from",
            "to_emails": "to_emails",
            "template_key": "template_key",
            "subject": "subject",
            "content": "content",
            "errors": "errors",
        }

        self._api_key = api_key
        self.__from = _from
        self._to_emails = to_emails
        self._template_key = template_key
        self._subject = subject
        self._content = content
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
        """Gets the email of the Sender.

        The email-id that will be used to send emails

        :return: The string email of sender.
        :rtype: str
        """
        return self.__from

    @_from.setter
    def _from(self, _from: str):
        """Sets the email of the Sender.

        The email-id that will be used to send emails

        :type email: str
        """
        email_regex = (
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
        )

        if _from is None or "":
            self.errors["_from"] = (
                "Invalid value for `email`, must not be `None`."
            )
        if not re.match(email_regex, _from):
            self.errors["_from"] = (
                "Invalid email id, please re-enter a valid email address."
            )
        else:
            self.__from = _from

    @property
    def api_key(self) -> str:
        """Gets the api_key of the user.

        :return: The api_key
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str):
        """Sets the api_key of the user..

        :type api_key: str
        """
        if api_key is None or "":
            self.errors["api_key"] = (
                "Invalid value for `api_key`, must not be `None`."
            )
        else:
            self._api_key = api_key

    @property
    def to_emails(self):
        """Gets the name and emails of the users and stores them as a string
           to add to the template
        """
        return self._to_emails

    @to_emails.setter
    def to_emails(self, to_emails):
        to_emails_formatted = ""
        to_emails = to_emails.replace("'", '"')
        to_emails = json.loads(to_emails)
        for name, email in to_emails.items():
            to_emails_formatted = to_emails_formatted + "(" + '"' + name + '", "' + email + '"),\n'
        self._to_emails = to_emails_formatted

    @property
    def template_key(self):
        return self._template_key

    @template_key.setter
    def template_key(self, template_key):
        print(template_key)
        if template_key is None or "":
            self._template_key = ""
        else:
            self._template_key = template_key

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject):
        if subject is None or "":
            self.errors["subject"] = (
               "Invalid value for `subject`, must not be `None`."
            )
        else:
            self._subject = subject

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):

        try:
            eval_json = json.loads(content.replace("'", '"'))
        except JSONDecodeError:
            pass
        except Exception as error:
            self.errors["content"]: str(error)
        self._content = content

    def return_result(self):
        if len(self.errors) != 0:
            return {"result": "error", "errors": self.errors, }, 500

        parent_dir = os.sep.join(__file__.split(os.sep)[:-3])

        if self._template_key in ["None", None, ""]:
            Email_Notifications = open(
                parent_dir + "/templates/nt_SendGrid_email.py", "r"
            )
            Email_Notify_Contents = Email_Notifications.read()
            Email_Notifications.close()
            Email_Notify_Contents = Email_Notify_Contents.replace(
                "REPLACE_CONTENT", self.content
            )

        else:
            # create folder
            Email_Notifications = open(
                parent_dir + "/templates/SendGrid_email.py", "r"
            )
            Email_Notify_Contents = Email_Notifications.read()
            Email_Notifications.close()
            Email_Notify_Contents = Email_Notify_Contents.replace(
                "REPLACE_TEMPLATE_ID", self._template_key
            )
            file_json = open(parent_dir + "dynamic_data.json", "w+")
            json.dump(self.content, file_json)
            file_json.close()

        Email_Notify_Contents = Email_Notify_Contents.replace(
            "REPLACE_SENDGRID_API_KEY", self._api_key
        )
        Email_Notify_Contents = Email_Notify_Contents.replace(
            "REPLACE_EMAIL_ID", self.__from
        )
        Email_Notify_Contents = Email_Notify_Contents.replace(
            '"REPLACE_RECIPIENT_EMAILS"', self._to_emails
        )
        Email_Notify_Contents = Email_Notify_Contents.replace(
            "REPLACE_EMAIL_SUBJECT", self._subject
        )

        _dir = parent_dir + "/Exports/Notifications/"
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        print(Email_Notify_Contents)
        file = open(_dir + "EmailNotifications.py", "w+")
        file.write(Email_Notify_Contents)
        file.close()

        return (
            {"result": "Successfully created E-mail notification script."},
            200,
        )
