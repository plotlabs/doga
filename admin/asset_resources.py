from os import path, mkdir
import base64

from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy.exc import IntegrityError

from app.utils import verify_jwt


from admin.models import (Admin, JWT, Restricted_by_JWT, Notifications,
                          Assets_Table)

from app import db

assets = Blueprint("assets", __name__)
api_utils = Api()
api_utils.init_app(assets)

metadata = db.metadata


class ListAssets(Resource):
    """
    Endpoint to list available assets
    """
    @jwt_required
    def get(self, asset_type):
        admin = get_jwt_identity()

        if not verify_jwt(admin, Admin):
            return {"result": "JWT authorization invalid, user does not"
                    " exist."}, 401

        assets = Assets_Table.query.filter_by(asset_type=asset_type)
        if assets != []:
            obj = []
            for asset in assets:
                obj.extend([asset.create_dict()])
            return obj, 200
        else:
            return ['No assets of this type found!'], 200



class UploadAssets(Resource):
    """
    Endpoint to list available assets
    """
    @jwt_required
    def post(self, asset_type):
        dest = '/'.join(path.dirname(__file__).split("/")[:-1]) + \
                 '/doga-frontend/public/uploads/'

        admin = get_jwt_identity()

        if not verify_jwt(admin, Admin):
            return {"result": "JWT authorization invalid, user does not"
                    " exist."}, 401

        if asset_type == 'image':
            if 'image' not in request.files:
                return {'result': 'Error, please attach file with request.'
                        }, 400
            img = request.files['image']
            filename = img.filename
            file_type = img.mimetype

            if not path.exists(dest):
                mkdir(dest)

            dest = dest + filename
            img.save(dest)

            try:
                asset = Assets_Table(
                                     asset_name=filename,
                                     asset_type='image',
                                     image_data=base64.b64encode(open(dest, "rb").
                                                                 read()),
                                     extension=file_type,
                                     asset_path=dest,
                                     user=admin['email']

                    )
                db.session.add(asset)
                db.session.commit()

            except IntegrityError:
                return { "result":
                        "Please upload a different asset, assset with this "\
                        "name is already present."
                }


api_utils.add_resource(UploadAssets, '/upload/<asset_type>')
api_utils.add_resource(ListAssets, '/list/<asset_type>')
