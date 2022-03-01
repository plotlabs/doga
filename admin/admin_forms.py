"""Form object declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length


class SignupForm(FlaskForm):
    """Sign up for a user account."""

    email = StringField(
        "Email", [Email(message="Not a valid email address."),
                  DataRequired()])
    password = PasswordField(
        "Password",
        [DataRequired(message="Please enter a password.")],
    )
    confirmPassword = PasswordField(
        "Repeat Password",
        [EqualTo(password, message="Passwords must match.")])
    name = StringField("Name", [DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    """Signup for existing admin"""

    email = StringField(
        "Email", [Email(message="Not a valid email address."),
                  DataRequired()])
    password = PasswordField(
        "Password",
        [DataRequired(message="Please enter a password.")],
    )
    submit = SubmitField("Submit")
