"""Form objects that will be used by the JINJA templates to collect the
users preferences for the creation of their own apps.
"""

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
)

from wtforms.validators import URL, DataRequired, Email, EqualTo, Length


class DatabaseCreation(FlaskForm):
    """Create a from for a new app"""

    database_type = SelectField(
        "Database Type",
        [DataRequired(message="Please select a valid database type.")],
        choices=["mysql", "sqlite", "postgresql"])

    username = StringField("Database username")
    password = PasswordField("Database user passoword")
    host = StringField("Host Address")
    port = IntegerField("Host Port")
    app_name = StringField("Name the app you wish to create")

    submit = SubmitField("Submit")
