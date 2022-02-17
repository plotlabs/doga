from flask import Blueprint, render_template, make_response, redirect, url_for, request, flash
from flask_restful import Api, Resource, marshal_with, fields

from admin.models.admin_model import Admin as AdminObject

from admin.admin_forms import *

from app import db

from passlib.handlers.sha2_crypt import sha512_crypt

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
        print(admin)
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
            return {
                "result": "Admin created successfully.",
                "id": admin.id,
                "email": admin.email,
            }, 200

        else:
            return {"result": "Admin already exists."}, 403


api_frontend.add_resource(test, "/test")
api_frontend.add_resource(Signup, "/signup")


@api_frontend.representation("text/html")
def out_html(data, code, headers):
    return make_response(data)