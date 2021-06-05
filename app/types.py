from sqlalchemy import types


class ImageType(types.TypeDecorator):

    impl = types.LargeBinary
