from flask import Blueprint, render_template, make_response, redirect, url_for, request, flash
from flask_restful import Api, Resource, marshal_with, fields

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                set_access_cookies)

from datetime import datetime as dt
from datetime import timedelta

from admin.models.admin_model import Admin as AdminObject
from admin.models import Admin

from admin.admin_forms import *

from app import db

from passlib.handlers.sha2_crypt import sha512_crypt

from typing import Tuple, Dict

ALGORITHM = sha512_crypt

mod_frontend = Blueprint("frontend",
                         __name__,
                         template_folder="templates",
                         static_folder="static")

api_frontend = Api()
api_frontend.init_app(mod_frontend)


class test(Resource):
    def get(self):
        return render_template("home.html",
                               my_string="Wheeeee!",
                               my_list=[0, 1, 2, 3, 4, 5])


class Signup(Resource):
    def get(self):
        """User sign-up form for account creation."""
        form = SignupForm()
        return render_template("signup.jinja2",
                               form=form,
                               template="form-template",
                               title="Signup Form")

    def post(self):
        """
        Defines responses for the `/admin/admin_adminprofile`
        endpoint
        It creates a Admin object from the request body it receives,
        checking if all values satisfy the model constraints and then writing
        data to the `amin` database.

        Parameters:
        ----------
        - name:
          in: json body
          type: string
          required: true
          description: Name of the Admin User

        - email:
          in: json body
          type: string
          format: email
          required: true
          description: E-mail id (unique) corresponding to the user

        - password:
          in : json body
          type: string
          format: length
          required: true

        Returns:
        -------
            json serializable dict
            integer response code

            responses:
            - 200
              description: Success registering admin
              schema:
                type: json
                parameters:
                - result
                  type: string
                - id
                  type: integer
                - email
                  type: string
                  format: email
            - 400
              description: Error message
              schema:
              type: json
              parameters:
              - result
                type: string
                description: Error message
            - 403
              description: Admin already registered
        """
        """TODO: delete unnecessary validation code

        json_request = request.get_json()
        if json_request is None:
            return {"result": "Error json body cannot be None."}, 400

        required_keys = {"name", "email", "password"}

        missed_keys = required_keys.difference(json_request.keys())

        if len(missed_keys) != 0:
            return (
                {
                    "result": "Values for fields cannot be null",
                    "required values": list(missed_keys),
                },
                400,
            )"""

        form = SignupForm(request.form)
        try:
            admin = AdminObject.from_dict({
                "name": form.name.data,
                "email": form.email.data,
                "password": form.password.data
            })
        except ValueError as err:
            flash("Error: ".join(err.args))
            return render_template("signup.jinja2",
                                   form=form,
                                   template="form-template",
                                   title="Signup Form")

        admin_exists = Admin.query.filter_by(email=admin.email.lower()).first()
        if admin_exists is None:
            password_hash = ALGORITHM.hash(admin.password)
            admin = Admin(
                email=admin.email.lower(),
                password=password_hash,
                name=admin.name,
                create_dt=dt.now(),
            )
            db.session.add(admin)
            db.session.commit()
            flash("Admin created successfully.")
            return redirect(url_for("frontend.login"))

        else:

            #refresh signup and notification of error
            flash("Admin already exists.")
            return redirect(url_for("frontend.signup"))


class Login(Resource):
    """API to login admin."""
    def get(self):
        form = LoginForm(request.form)
        return render_template("login.jinja2", form=form)

    def post(self) -> Tuple[Dict[str, str], int]:
        # def post(self) -> Tuple[Dict[str, str], int]:
        """
        Defines responses for the `/admin/login/` endpoint.
        It allows a registered Admin user to login and receive a jwt, that can
        be used to access the other restricted endpoints.

        Parameters:
        -----------
        - email:
          in: json body
          required: true
          type: string
          format: email

        - password
          in: json body
          required: true
          type: string

        Returns:
        -------
            responses:
            - 200
        """

        form = LoginForm(request.form)
        try:
            admin = Admin.query.filter_by(
                email=form.email.data.lower()).first()
            if admin is None:
                return {"result": "Admin does not exist."}, 404
            else:
                match = ALGORITHM.verify(form.password.data, admin.password)
                expiry_time = timedelta(hours=4)
                if not match:
                    return {"result": "Invalid password."}, 401
                else:
                    filter_keys = {"email": form.email.data}

                    access_token = create_access_token(
                        identity=filter_keys, expires_delta=expiry_time)
                    refresh_token = create_refresh_token(identity=filter_keys)

                    response = make_response(
                        redirect(url_for("dashboard.admindashboardstats")))
                    set_access_cookies(response, access_token)

                    return response

        except KeyError as e:
            return {"result": "Key error", "error": str(e)}, 500


api_frontend.add_resource(test, "/test")
api_frontend.add_resource(Signup, "/signup")
api_frontend.add_resource(Login, "/login")


@api_frontend.representation("text/html")
def out_html(data, code, headers):
    return make_response(data)