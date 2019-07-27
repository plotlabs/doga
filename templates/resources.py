import json
import datetime
import requests

from flask import request, Blueprint
from flask_restful import Resource, Api

from app import db
from app.modulename.models import modelname
from app.utils import AlchemyEncoder
from sqlalchemy.exc import OperationalError, IntegrityError, StatementError


mod_model = Blueprint(bname, __name__)
api_model = Api()
api_model.init_app(mod_model)

model_name = modelname


class Apis(Resource):
    """APIs to create a user and return user info if a user exists"""

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

    def post(self):
        data = request.get_json()
        model_obj = model_name()
        for col in model_name.__table__.columns:
            col_name = col.name
            if col_name not in ['id', 'create_dt']:
                if str(col.type) == 'DATETIME':
                    try:
                        data[col.name] = datetime.datetime.strptime(
                            data[col.name], "%Y/%m/%d")
                    except ValueError:
                        return {
                            "result": "The format entered for column {} is "
                                      "not correct. Correct format should"
                                      " be of type: YYYY/MM/DD.".format(
                                col.name)}
                    except TypeError:
                        return {
                            "result": "The format entered for column {} is "
                                      "not correct. Correct format should"
                                      " be of type: YYYY/MM/DD.".format(
                                col.name)}
                    except KeyError:
                        pass

                if str(col.type) in ['INTEGER', 'BIGINTEGER', 'BIGINT']:
                    if isinstance(data[col.name], str):
                        return {"result": "The value entered for column {} "
                                          "is string and not of type"
                                          " {}".format(col.name, col.type)}

                if len(col.foreign_keys) > 0:
                    for f in col.foreign_keys:
                        model_endpoint = str(f).split("'")[1].split('.')[0]
                        foreign_obj = requests.get(
                            'http://localhost:8080/' + model_endpoint +
                            '/' + str(data[col.name]))
                        result = json.loads(foreign_obj.content)["result"]

                        if len(result) == 0:
                            return {"result": "Foreign Key constraint "
                                              "failed for column "
                                              "{}".format(col.name)}

        for key, value in data.items():
            setattr(model_obj, key, value)
        db.session.add(model_obj)

        try:
            db.session.commit()
        except OperationalError as e:
            return {"result": e.orig.args[1].split(' at ')[0]}
        except IntegrityError as e:
            return {"result": str(e.orig).split('\n')[0]}
        except StatementError as e:
            return {"result": str(e.orig)}
        return {"result": 'Created row.'}

    def put(self, id):
        data = request.get_json()
        model_obj = model_name.query.filter_by(id=id).first()
        if model_obj is not None:
            for col in model_name.__table__.columns:
                col_name = col.name
                if col_name not in ['id', 'create_dt']:
                    if str(col.type).upper() in ['DATETIME', 'DATE']:
                        try:
                            data[col.name] = datetime.datetime.strptime(
                                data[col.name], "%Y/%m/%d")
                        except ValueError:
                            return {
                                "result": "The format entered for column {} "
                                          "is not correct. Correct format "
                                          "should be of type: "
                                          "YYYY/MM/DD.".format(col.name)}
                        except TypeError:
                            return {
                                "result": "The format entered for column {} "
                                          "is not correct. Correct format "
                                          "should be of type: "
                                          "YYYY/MM/DD.".format(col.name)}
                        except KeyError:
                            pass

                    if str(col.type).upper() in ['INTEGER', 'BIGINTEGER',
                                                 'BIGINT', 'FLOAT', 'INT',
                                                 'SMALLINT', 'NUMERIC',
                                                 'SMALLINTEGER']:
                        if isinstance(data[col.name], str):
                            return {
                                "result": "The value entered for column {} "
                                          "is string and not of type"
                                          " {}".format(col.name, col.type)}

                    if len(col.foreign_keys) > 0:
                        for f in col.foreign_keys:
                            model_endpoint = str(f).split("'")[1].split('.')[0]
                            foreign_obj = requests.get(
                                'http://localhost:8080/' + model_endpoint +
                                '/' + str(data[col.name]))
                            result = json.loads(foreign_obj.content)[
                                "result"]

                            if len(result) == 0:
                                return {"result": "Foreign Key constraint "
                                                  "failed for column "
                                                  "{}".format(col.name)}

            for key, value in data.items():
                setattr(model_obj, key, value)
            db.session.add(model_obj)

            try:
                db.session.commit()
            except OperationalError as e:
                return {"result": e.orig.args[1].split(' at ')[0]}
            except IntegrityError as e:
                return {"result": str(e.orig).split('\n')[0]}
            except StatementError as e:
                return {"result": str(e.orig)}
            return {"result": 'Created row.'}
        else:
            return {"result": 'Does not exist'}

    def delete(self, id):
        model_name.query.filter_by(id=id).delete()
        db.session.commit()
        return {"result": "Successfully deleted."}


api_model.add_resource(Apis, endpoint, param)
