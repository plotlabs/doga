from flask import Blueprint, render_template, make_response, redirect, url_for
from flask_restful import Api, Resource, marshal_with, fields

from admin.frontend_utils import *
from datetime import datetime

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

    @marshal_with('signup')
    def post(self):
        form = SignupForm()
        if form.validate_on_submit():
            return {'redirect(url_for("success"))'}, 200

        else:
            return "sad"


api_frontend.add_resource(test, "/test")
api_frontend.add_resource(Signup, "/signup")


@api_frontend.representation("text/html")
def out_html(data, code, headers):
    return make_response(data)