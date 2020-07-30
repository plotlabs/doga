import json

from flask import Blueprint, request, jsonify
from passlib.handlers.sha2_crypt import sha512_crypt
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity)

ALGORITHM = sha512_crypt

jwt_filter_keys = jwt_key


class Login(Resource):
    """API to login model_obj."""

    def post(self):
        data = request.get_json()
        try:
            filter_keys = {key: data[key] for key in jwt_filter_keys}
            model_obj = model_name.query.filter_by(
                **filter_keys).first()
            if model_obj is None:
                return {"result": model_name.__tablename__ +
                        " does not exist."}, 401
            else:
                # match = ALGORITHM.verify(data["password"], .password)
                # if not match:
                #   return {"result": "Invalid password."}, 401
                # else:
                access_token = create_access_token(
                    identity=filter_keys)
                refresh_token = create_refresh_token(
                    identity=filter_keys)
                return {"result": "Logged in Successfully.",
                        "id": model_obj.id,
                        'access_token': access_token,
                        'refresh_token': refresh_token}
        except KeyError as e:
            return {"result": "Key error", "error": str(e)}, 500


api_model.add_resource(Login, "/login")
