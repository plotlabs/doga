from sqlalchemy import Integer, String, DateTime, text, Boolean, Enum
from sqlalchemy.schema import UniqueConstraint

from app import db
from app.types import ImageType

Base = db.Model
Column = db.Column
ForeignKey = db.ForeignKey
metadata = db.metadata
relationship = db.relationship


class Admin(Base):
    __tablename__ = "admin"
    __bind_key__ = "default"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255))
    create_dt = Column(DateTime(), server_default=text("CURRENT_TIMESTAMP"))

    def get_unread_notifs(self, reverse=False):
        """Get unread notifications for this user
        """
        notifs = []
        unread_notifs = Notifications.query.filter_by(
            user=self.id, has_read=False
        )
        for notif in unread_notifs:
            notifs.append(
                {
                    "title": notif.foramt_notification(),
                    "received_at": humanize.naturaltime(
                        datetime.now() - notif.received_at
                    ),
                    "mark_read": setattr(notif, "mark_read", True),
                }
            )

        if reverse:
            return list(reversed(notifs))
        else:
            return notifs


class JWT(Base):
    """ Defines a table jwt stored in /tmp/test.db to store the table that is
        jwt for the particular connection
    """

    __tablename__ = "jwt"
    __bind_key__ = "default"

    id = Column(Integer, primary_key=True)
    jwt_flag = Column(Boolean, nullable=False, unique=False)
    connection_name = Column(String(255), nullable=False, unique=True)
    table = Column(String(255), nullable=False, unique=False)
    filter_keys = Column(String(255), nullable=False, unique=False)
    UniqueConstraint("database_name", "table", name="uix_1")

    # confirm length for the filter key fields ( and find a better way
    # to store the filter keys keep in mind Arrays are not allowed in SQLite)

    filter_keys = Column(String(255), nullable=False)
    create_dt = Column(DateTime(), server_default=text("CURRENT_TIMESTAMP"))


class Restricted_by_JWT(Base):
    """ Defines a table Restricted_by_JWT to store the tables restricted by a
    JWT for a particular connection/app
    """

    __tablename__ = "restricted_by_jwt"
    __bind_key__ = "default"

    id = Column(Integer, primary_key=True)
    connection_name = Column(String(255), ForeignKey("jwt.connection_name"))
    restricted_tables = Column(String(1000))


class Deployments(Base):
    """ Defines a table Deployments to store the deployed apps and where they
    have been deployed
    """

    __tablename__ = "deployments"
    __bind_key__ = "default"

    id = Column(Integer, primary_key=True)
    app_name = Column(String(255))
    platfrom = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    # ID of the things & other dicts
    exports = Column(Integer, nullable=False)
    create_dt = Column(DateTime(), server_default=text("CURRENT_TIMESTAMP"))


class Relationship(Base):
    """ Defines a table Relationships to store the deployed apps and where they
    have been deployed
    """

    __tablename__ = "relationships"
    __bind_key__ = "default"

    id = Column(Integer, primary_key=True)
    app_name = Column(String(255))
    table1_column = Column(String(255), nullable=False)
    relationship = Column(String(255), nullable=False)
    table2_column = Column(String(255), nullable=False)
    UniqueConstraint(
        "id", "table1_column", "relationship", "table2_column", name="uix_1"
    )


class Notifications(Base):
    """ Defines a table Notifications to store the info regarding apps and
    any new events that need to be passes to the user
    """

    __tablename__ = "notifications"
    __bind_key__ = "default"

    id = Column(Integer, primary_key=True)
    app_name = Column(String(255))
    user = Column(String(255), ForeignKey("admin.email"), nullable=False)
    received_at = Column(DateTime(), server_default=text("CURRENT_TIMESTAMP"))
    action_status = Column(String(255), nullable=False)
    message = Column(String(255), nullable=False)
    completed_action_at = Column(DateTime(), nullable=True)
    action_type = Column(
        Enum(
            "create-content-tables",
            "deploy-app",
            "delete-content-tables",
            name="doga_action_types",
        ),
        nullable=True,
    )
    mark_read = Column(Boolean, server_default=text("False"))
    full_notif = Column(String(255))

    def foramt_notification(self):
        self.full_notif = (
            f"{self.action_status.title()}: "
            f"{self.app_name} "
            f"{self.message}"
        )

        return self.full_notif

    def create_dict(self):

        if self.completed_action_at is None:
            completed_action_at = None
        else:
            completed_action_at = self.completed_action_at.strftime(
                "%m/%d/%Y, %H:%M:%S"
            )
        self.foramt_notification()
        return {
            "id": self.id,
            "app_name": self.app_name,
            "user": self.user,
            "received_at": self.received_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "action_status": self.action_status,
            "action_type": self.action_type,
            "message": self.message,
            "full_message": self.full_notif,
            "completed_action_at": completed_action_at,
            "mark_read": self.mark_read,
        }


class Assets_Table(Base):
    """ Defines a table Notifications to store the info regarding apps and
    any new events that need to be passes to the user
    """

    __tablename__ = "assets_table"
    __bind_key__ = "default"

    id = Column(Integer, primary_key=True)
    asset_name = Column(String(255), nullable=False)
    asset_type = Column(Enum("image", name="doga_asset_types",), nullable=True)
    app_name = Column(String(255))
    image_data = Column(ImageType, nullable=True)
    extension = Column(String(10), nullable=False)
    asset_path = Column(String(255), nullable=False, unique=True)
    user = Column(String(255), ForeignKey("admin.email"), nullable=False)
    uploaded_at = Column(DateTime(), server_default=text("CURRENT_TIMESTAMP"))
    UniqueConstraint("asset_name", "asset_type", name="uix_1")

    def create_dict(self):
        return {
            "asset_name": self.asset_name,
            "asset_type": self.asset_type,
            "asset_path": self.asset_path,
            "image": self.image_data.decode("utf-8"),
            "uploaded_at": self.uploaded_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "user": self.user,
        }
