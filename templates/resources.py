import json

from flask import request, Blueprint
from flask_restful import Resource, Api

from app import db
from app.modulename.models import modelname
from app.utils import AlchemyEncoder


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
        for key, value in data.items():
            setattr(model_obj, key, value)
        db.session.add(model_obj)
        db.session.commit()
        return {"result": 'Created row.'}

    def put(self, id):
        data = request.get_json()
        model_obj = model_name.query.filter_by(id=id).first()
        if model_obj is not None:
            for key, value in data.items():
                setattr(model_obj, key, value)
            db.session.add(model_obj)
            db.session.commit()
            return {"result": 'Updated row.'}
        else:
            return {"result": 'Does not exist'}

    def delete(self, id):
        model_name.query.filter_by(id=id).delete()
        db.session.commit()
        return {"result": "Successfully deleted."}


api_model.add_resource(Apis, endpoint, param)
