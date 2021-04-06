import json
import datetime
import requests

from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_jwt_extended import (jwt_required, create_access_token,
                                create_refresh_token, get_jwt_identity)

from sqlalchemy.exc import (OperationalError, IntegrityError, StatementError,
                            UnsupportedCompilationError)

from app import db
from app.modulename.models import modelname
from app.utils import AlchemyEncoder, verify_jwt

from config import HOST, PORT

jwt_filter_keys = jwt_key

mod_model = Blueprint(bname, __name__)
api_model = Api()
api_model.init_app(mod_model)

model_name = modelname


class Apis(Resource):
    """APIs to create a user and return user info if a user exists"""

    @jwt_required
    def get(self, id=None):
        if not verify_jwt(get_jwt_identity(), model_name):
            return {"result": "JWT authorization invalid, user does not"
                    " exist."}
        if id is None:
            model_obj = model_name.query.all()
            if model_obj is not None:
                obj = json.dumps(model_obj, cls=AlchemyEncoder)
                return {"result": json.loads(obj)}
        else:
            model_obj = model_name.query.filter_by(id=id).first()
            if model_obj is not None:
                obj = json.dumps(model_obj, cls=AlchemyEncoder)
                return {"result": json.loads(obj)}
            else:
                return {"result": []}

    @jwt_required
    def put(self, id):
        if not verify_jwt(get_jwt_identity(), model_name):
            return {"result": "JWT authorization invalid, user does not"
                    " exist."}
        data = request.get_json()

        if data is None:
            return {"response": "JSON body cannot be empty."}, 500

        model_obj = model_name.query.filter_by(id=id).first()
        if model_obj is not None:
            for col in model_name.__table__.columns:
                col_name = col.name
                if col_name not in ['id', 'create_dt']:
                    if 'BLOB' in str(col.type).upper():
                        try:
                            data[col.name] = str(data[col.name]).encode(
                                                                    'utf-8')
                        except KeyError:
                            pass

                    if str(col.type).upper() == "DATE":
                        try:
                            data[col.name] = datetime.datetime.strptime(
                                data[col.name], "%Y-%m-%d")
                        except ValueError:
                            return {
                                "result": "The format entered for column {} is"
                                          " not correct. Correct format should"
                                          " be of type: YYYY-MM-DD.".format(
                                              col.name)}, 400
                        except TypeError:
                            return {
                                "result": "The format entered for column {} is"
                                          " not correct. Correct format should"
                                          " be of type: YYYY-MM-DD.".format(
                                              col.name)}, 400
                        except KeyError:
                            pass

                    elif str(col.type).upper() == "DATETIME":
                        try:
                            data[col.name] = datetime.datetime.strptime(
                                data[col.name], "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            return {
                                "result": "The format entered for column {} is"
                                          " not correct. Correct format should"
                                          " be of type: YYYY-MM-DD H:M:S."
                                          .format(col.name)}, 400
                        except TypeError:
                            return {
                                "result": "The format entered for column {} is"
                                          " not correct. Correct format should"
                                          " be of type: YYYY-MM-DD H:M:S."
                                          .format(col.name)}, 400
                        except KeyError:
                            pass

                    if str(col.type).upper() in ['INTEGER', 'BIGINTEGER',
                                                 'BIGINT', 'FLOAT', 'INT',
                                                 'SMALLINT', 'NUMERIC',
                                                 'SMALLINTEGER', 'DECIMAL',
                                                 'REAL']:
                        if isinstance(data[col.name], str):
                            return {
                                "result": "The value entered for column {} "
                                          "is string and not of type "
                                          "{}".format(col.name, col.type)}, 400

                    if len(col.foreign_keys) > 0:
                        for f in col.foreign_keys:
                            model_endp = str(f).split("'")[1].split('.')[0]
                            foreign_obj = requests.get(
                                'http://{}:{}/'.format(HOST, PORT)
                                + 'module_endp_lower'
                                + '/' + model_endp)
                            result = json.loads(foreign_obj.content)[
                                "result"]

                            if foreign_obj.status_code != 200:
                                return {
                                    "result": "Foreign object does not exist."
                                }
                        if len(result) == 0:
                            return {"result": "Foreign Key constraint "
                                    "failed for column "
                                    "{}".format(col.name)}, 400
                        exists = False
                        try:
                            for entries in result:
                                if entries[str(f).split("'")[1].split('.')[
                                        1]] == data[col.name]:
                                    exists = True
                                    break
                        except Exception as e:
                            return {"result": "Foreign Key constraint "
                                    "failed for column "
                                    "{}".format(col.name),
                                    "error": str(e)}, 400

                        if exists is False:
                            return {"result": "Foreign Key constraint "
                                    "failed for column "
                                    "{}".format(col.name)}, 400

            for key, value in data.items():
                setattr(model_obj, key, value)
            db.session.add(model_obj)

            try:
                db.session.commit()
            except OperationalError as e:
                return {"result": e.orig.args[1].split(' at ')[0]}, 400
            except IntegrityError as e:
                try:
                    return {"result": str(e.orig).split('\n')[0].replace(
                        '"', '').split(',')[1].replace(")", '').title()}, 400
                except IndexError:
                    return {"result": str(e.orig).split('\n')[0].replace(
                        '"', '').title()}, 400
            except StatementError as e:
                return {"result": str(e.orig)}, 400
            return {"result": 'Created row.'}
        else:
            return {"result": 'Does not exist'}, 400

    @jwt_required
    def delete(self, id):
        if not verify_jwt(get_jwt_identity(), model_name):
            return {"result": "JWT authorization invalid, user does not"
                    " exist."}
        try:
            model_name.query.filter_by(id=id).delete()
            db.session.commit()
        except IntegrityError as e:
            try:
                return {"result": str(e.orig).split('\n')[0].replace(
                    '"', '').split(',')[1].split(' (')[0].title()}, 400
            except IndexError:
                return {"result": str(e.orig).split('\n')[0].replace(
                    '"', '').title()}, 400
        return {"result": "Successfully deleted."}


class Login(Resource):
    """API to login"""

    def post(self):
        data = request.get_json()

        if data is None:
            return {"response": "JSON body cannot be empty."}, 500

        try:
            filter_keys = {key: data[key] for key in jwt_filter_keys}
            model_obj = model_name.query.filter_by(
                **filter_keys).first()
            if model_obj is None:
                return {"result": model_name.__tablename__ +
                        " does not exist."}, 401
            else:
                expiry_time = datetime.timedelta(expiry_unit=expiry_value)
                access_token = create_access_token(
                    identity=filter_keys, expires_delta=expiry_time)
                refresh_token = create_refresh_token(
                    identity=filter_keys)
                return {"result": "Logged in Successfully.",
                        "id": model_obj.id,
                        'access_token': access_token,
                        'refresh_token': refresh_token}
        except KeyError as e:
            return {"result": "Missing field: " + str(e)}, 400


class Register(Resource):
    """API to register model_obj."""

    def post(self):
        data = request.get_json()
        if data is None:
            return {"response": "JSON body cannot be empty."}, 500

        model_obj = model_name()
        for col in model_name.__table__.columns:
            col_name = col.name
            if col_name not in ['id', 'create_dt']:
                try:
                    if 'BLOB' in str(col.type).upper():
                        try:
                            data[col.name] = str(data[col.name]).encode(
                                                                    'utf-8')
                        except KeyError:
                            pass

                    if str(col.type).upper() == "DATE":
                        try:
                            data[col.name] = datetime.datetime.strptime(
                                data[col.name], "%Y-%m-%d")
                        except ValueError:
                            return {
                                "result": "The format entered for column {}"
                                " is not correct. Correct format should be"
                                " of type: YYYY-MM-DD.".format(
                                    col.name)}, 400
                        except TypeError:
                            return {
                                "result": "The format entered for column {} "
                                "is not correct. Correct format should be "
                                "of type: YYYY-MM-DD.".format(
                                    col.name)}, 400
                        except KeyError:
                            pass

                    elif str(col.type).upper() == "DATETIME":
                        try:
                            data[col.name] = datetime.datetime.strptime(
                                data[col.name], "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            return {
                                "result": "The format entered for column {} "
                                "is not correct. Correct format "
                                "should be of type: YYYY-MM-DD H:M:S.".format(
                                    col.name)}, 400
                        except TypeError:
                            return {
                                "result": "The format entered for column {} "
                                          "is not correct. Correct format "
                                          "should be of type: "
                                          "YYYY-MM-DD H:M:S.".format(
                                           col.name)}, 400
                        except KeyError:
                            pass

                    elif str(col.type).upper() in ['INTEGER', 'BIGINTEGER',
                                                   'BIGINT', 'FLOAT', 'INT',
                                                   'SMALLINT', 'NUMERIC',
                                                   'SMALLINTEGER', 'DECIMAL',
                                                   'REAL']:
                        if isinstance(data[col.name], str):
                            return {
                                "result": "The value entered for column {} "
                                "is string and not of type {}"
                                "".format(
                                    col.name, col.type)}, 400
                except UnsupportedCompilationError as error:
                    if 'JSON' in str(error).upper():
                        pass
                    else:
                        return {
                            "result": "Cannot interpret type of the"
                                      " column {}.".format(col.name)
                        }

                if len(col.foreign_keys) > 0:
                    for f in col.foreign_keys:
                        model_endp = str(f).split("'")[1].split('.')[0]
                        foreign_obj = requests.get(
                            'http://{}:{}/'.format(HOST, PORT)
                            + 'module_endp_lower'
                            + '/' + model_endp)

                        if foreign_obj.status_code != 200:
                            return {
                                "result": "Foreign object does not exist."
                            }

                        result = json.loads(foreign_obj.content)["result"]

                        if len(result) == 0:
                            return {"result": "Foreign Key constraint "
                                    "failed for column "
                                    "{}".format(col.name)}, 400
                        exists = False
                        try:
                            for entries in result:
                                if entries[str(f).split("'")[1].split('.')[
                                        1]] == data[col.name]:
                                    exists = True
                                    break
                        except Exception as e:
                            return {"result": "Foreign Key constraint "
                                              "failed for column "
                                              "{}".format(col.name),
                                              "error": str(e)}, 400

                        if exists is False:
                            return {"result": "Foreign Key constraint "
                                              "failed for column "
                                              "{}".format(col.name)}, 400

        for key, value in data.items():
            setattr(model_obj, key, value)
        db.session.add(model_obj)

        try:
            db.session.commit()
        except OperationalError as e:
            return {"result": e.orig.args[1].split(' at ')[0]}, 400
        except IntegrityError as e:
            try:
                return {"result": str(e.orig).split('\n')[0].replace(
                    '"', '').split(',')[1].replace(")", '').title()}, 400
            except IndexError:
                return {"result": str(e.orig).split('\n')[0].replace(
                    '"', '').title()}, 400
        except StatementError as e:
            return {"result": str(e.orig)}, 400

        filter_keys = {key: getattr(model_obj, key) for key in jwt_filter_keys}
        expiry_time = datetime.timedelta(hours=4)
        access_token = create_access_token(
            identity=filter_keys, expires_delta=expiry_time)
        refresh_token = create_refresh_token(
            identity=filter_keys)

        return {"result": "Registered & Logged in Successfully.",
                "id": model_obj.id,
                'access_token': access_token,
                'refresh_token': refresh_token}


api_model.add_resource(Login, "/login")
api_model.add_resource(Register, "/register")
api_model.add_resource(Apis, endpoint, param)
