import json
import datetime
import requests

from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_jwt_extended import (jwt_required, create_access_token,
                                create_refresh_token)

from sqlalchemy.exc import OperationalError, IntegrityError, StatementError

from app import db
from app.modulename.models import modelname
from app.utils import AlchemyEncoder

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
        data = request.get_json()
        model_obj = model_name.query.filter_by(id=id).first()
        if model_obj is not None:
            for col in model_name.__table__.columns:
                col_name = col.name
                if col_name not in ['id', 'create_dt']:
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
                                          "is string and not of type"
                                          " {}".format(col.name, col.type)}, 400

                    if len(col.foreign_keys) > 0:
                        for f in col.foreign_keys:
                            model_endp = str(f).split("'")[1].split('.')[0]
                            foreign_obj = requests.get(
                                'http://{}:{}/'.format(HOST, PORT) + model_endp
                                + '/' + str(data[col.name]))
                            result = json.loads(foreign_obj.content)[
                                "result"]

                            if len(result) == 0:
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
            return {"result": "missing field: " + str(e)}, 400


class Register(Resource):
    """API to regiter model_obj."""

    def post(self):
        data = request.get_json()
        model_obj = model_name()
        for col in model_name.__table__.columns:
            col_name = col.name
            if col_name not in ['id', 'create_dt']:
                if str(col.type).upper() == "DATE":
                    try:
                        data[col.name] = datetime.datetime.strptime(
                            data[col.name], "%Y-%m-%d")
                    except ValueError:
                        return {
                            "result": "The format entered for column {} is "
                                      "not correct. Correct format should"
                                      " be of type: YYYY-MM-DD.".format(
                                          col.name)}, 400
                    except TypeError:
                        return {
                            "result": "The format entered for column {} is "
                                      "not correct. Correct format should"
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
                            "result": "The format entered for column {} is "
                                      "not correct. Correct format should"
                                      " be of type: YYYY-MM-DD H:M:S.".format(
                                          col.name)}, 400
                    except TypeError:
                        return {
                            "result": "The format entered for column {} is "
                                      "not correct. Correct format should"
                                      " be of type: YYYY-MM-DD H:M:S.".format(
                                          col.name)}, 400
                    except KeyError:
                        pass

                elif str(col.type).upper() in ['INTEGER', 'BIGINTEGER',
                                               'BIGINT', 'FLOAT', 'INT',
                                               'SMALLINT', 'NUMERIC',
                                               'SMALLINTEGER', 'DECIMAL',
                                               'REAL']:
                    if isinstance(data[col.name], str):
                        return {"result": "The value entered for column {} "
                                          "is string and not of type {}"
                                          "".format(col.name, col.type)}, 400

                if len(col.foreign_keys) > 0:
                    for f in col.foreign_keys:
                        model_endp = str(f).split("'")[1].split('.')[0]
                        foreign_obj = requests.get(
                            'http://localhost:8080/' + model_endp +
                            '/' + str(data[col.name]))
                        result = json.loads(foreign_obj.content)["result"]

                        if len(result) == 0:
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
        return {"result": 'Registered Successfully'}


api_model.add_resource(Login, "/login")
api_model.add_resource(Register, "/register")
api_model.add_resource(Apis, endpoint, param)
