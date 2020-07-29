import json

from flask import Blueprint, request, jsonify
from passlib.handlers.sha2_crypt import sha512_crypt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

ALGORITHM = sha512_crypt

filter_key = jwt_key


class Login(Resource):
    """API to login model_obj."""

    def post(self):
        data = request.get_json()
        try:
            model_obj = model_name.query.filter_by(
                **{filter_key: data[filter_key]}).first()
            if model_obj is None:
                return {"result": model_name + " does not exist."}, 401
            else:
                # match = ALGORITHM.verify(data["password"], .password)
                # if not match:
                #   return {"result": "Invalid password."}, 401
                # else:
                access_token = create_access_token(
                    identity=model_obj.__dict__[filter_key])
                refresh_token = create_refresh_token(
                    identity=model_obj.__dict__[filter_key])
                return {"result": "Logged in Successfully.",
                        "id": model_obj.id, 
                        'access_token': access_token,
                        'refresh_token': refresh_token}
        except KeyError as e:
            return {"result": "Key error", "error": str(e)}, 500


api_model.add_resource(Login, "/login")
