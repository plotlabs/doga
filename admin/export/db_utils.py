from app import db

from admin.models import Admin, JWT, Restricted_by_JWT


def delete_admin():
    Admin.__table__.drop()


def drop_all_jwt(connection_name):
    JWT.__tablename__.drop()
    db.session.query(Restricted_by_JWT).filter(Restricted_by_JWT.connection_name != connection_name).delete()  # noqa 501
    db.session.commit()
