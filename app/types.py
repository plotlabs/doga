from sqlalchemy import types
import base64


class ImageType(types.TypeDecorator):

    impl = types.LargeBinary
