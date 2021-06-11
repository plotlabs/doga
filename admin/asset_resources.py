from os import mkdir, path, remove
import base64

from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy.exc import IntegrityError

from app.utils import verify_jwt


from admin.models import Admin, Assets_Table

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
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )

        assets_ = Assets_Table.query.filter_by(asset_type=asset_type)
        if assets_:
            obj = []
            for asset in assets_:
                obj.extend([asset.create_dict()])
            return obj, 200
        else:
            return ["No assets of this type found!"], 200


class UploadAssets(Resource):
    """
    Endpoint to upload/delete assets
    Resource admin/assets/upload/<asset_type>
    Endpoints:
        - POST
        - DELETE
    """

    @jwt_required
    def post(self, asset_type):
        """Allows for a file to be uploaded to the DOGA's assets database,

           Parameters:
           ----------
           - asset_type:
             in: path
             type: string
             enum:
                - Image
           - assetfile
             in: form-data
             type: .*

           Responses:
           ---------
            - 200:
              description: Successful upload
            - 400:
              description: Error
            - 500:
              description: Server Error
        """

        dest = (
                    "/".join(path.dirname(__file__).split("/")[:-1])
                    + "/doga-frontend/public/uploads/"
                )

        admin = get_jwt_identity()

        if not verify_jwt(admin, Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )

        if asset_type == "image":
            if "image" not in request.files:
                return (
                    {"result": "Error, please attach file with request."},
                    400,
                )
            img = request.files["image"]
            filename = img.filename
            file_type = img.mimetype

            if not path.exists(dest):
                mkdir(dest)

            dest = dest + filename
            img.save(dest)

            try:
                asset = Assets_Table(
                    asset_name=filename,
                    asset_type="image",
                    image_data=base64.b64encode(open(dest, "rb").read()),
                    extension=file_type,
                    asset_path=dest,
                    user=admin["email"],
                )
                db.session.add(asset)
                db.session.commit()
                return {"result": "Uploaded image successfully."}, 200

            except IntegrityError:
                return (
                    {
                        "result": "Please upload a different asset, "
                        "assset with this "
                        "name is already present."
                    },
                    400,
                )

    @jwt_required
    def delete(self, asset_type):
        """Deletes the asset from the database.

           Parameters:
           ----------
           - asset_type:
                 type: string
                 in: path
                 enum:
                    - Image

           - asset_name:
                 type: string
                 in : json body
                 description: The name of the asset to be deleted.
        """

        admin = get_jwt_identity()

        dest = (
                    "/".join(path.dirname(__file__).split("/")[:-1])
                    + "/doga-frontend/public/uploads/"
                )

        if not verify_jwt(admin, Admin):
            return (
                {
                    "result": "JWT authorization invalid, user does not"
                    " exist."
                },
                401,
            )

        if asset_type == "image":

            try:
                image_name = request.get_json()['asset_name']
            except KeyError:
                return {
                    "result": "Missing required paramenter asset_name"
                }, 400

            try:
                db.session.query(Assets_Table).filter(
                    Assets_Table.asset_name == image_name,
                    Assets_Table.asset_type == "Image"
                    ).delete()
                db.session.commit()
            except Exception as e:
                return {"result": e}, 500

            remove(dest + image_name)

            return {"result": "Successfully deleted asset: " + image_name}, 200


api_utils.add_resource(UploadAssets, "/upload/<asset_type>")
api_utils.add_resource(ListAssets, "/list/<asset_type>")
