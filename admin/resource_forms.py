"""Form objects that will be used by the JINJA templates to collect the
users preferences for the creation of their own apps.
"""

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (IntegerField, PasswordField, StringField, SubmitField,
                     SelectField, BooleanField)

from wtforms.validators import URL, DataRequired, Email, EqualTo, Length, Regexp

from admin.form_utils import *


class DatabaseCreation(FlaskForm):
    """Create a from for a new app"""

    database_type = SelectField(
        "Database Type",
        [DataRequired(message="Please select a valid database type.")],
        choices=["mysql", "sqlite", "postgresql"])

    username = StringField("Database username")
    password = PasswordField("Database user passoword")
    host = StringField("Host Address", [
        Regexp(
            "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        )
    ])
    port = IntegerField("Host Port")
    app_name = StringField("Name the app you wish to create")

    submit = SubmitField("Submit")


class ColumnForm(FlaskForm):
    """Add tables to the form created"""

    app_name = StringField(
        "Name of the application the data belongs to ",
        render_kw={'disabled': ''},
    )

    table_name = StringField(
        "Name of the collection the data belongs to ",
        render_kw={'disabled': ''},
    )

    column_name = StringField(
        "Data Group Name",
        [DataRequired(message="Please specify the name of the Data Field")])

    col_types = all_coltypes()

    column_types = SelectField("Data Type", [
        DataRequired(
            message="Please specify the Type of data you'd like in this field")
    ],
                               choices=col_types)

    nullable = BooleanField(
        "Allow null values",
        [
            DataRequired(),
        ],
    )

    unique = BooleanField(
        "Allow duplicate values",
        [
            DataRequired(),
        ],
    )

    #todo: get all the foreign key candidates and display appropriately
    foreign_key = StringField("Add foreign_key values", )

    default = StringField("Default value", )
    submit = SubmitField("Save")


class TableForm(FlaskForm):
    """Add the table name"""
