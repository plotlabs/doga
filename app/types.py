from sqlalchemy import types

from sqlalchemy import BLOB, Table, event


class ImageType(types.TypeDecorator):

    impl = types.LargeBinary
