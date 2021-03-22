from sqlalchemy import Integer, String, DateTime, text, Boolean
from sqlalchemy.schema import UniqueConstraint

from app import db

Base = db.Model
Column = db.Column
ForeignKey = db.ForeignKey
metadata = db.metadata
relationship = db.relationship


class Admin(Base):
    __tablename__ = 'admin'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255))
    create_dt = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))

    def get_unread_notifs(self, reverse=False):
        """Get unread notifications for this user
        """
        notifs = []
        unread_notifs = Notifications.query.filter_by(user=self.id,
                                                      has_read=False)
        for notif in unread_notifs:
            notifs.append({
                'title': notif.foramt_notification(),
                'received_at': humanize.naturaltime(datetime.now() -
                                                    notif.received_at),
                'mark_read': setattr(notif, 'mark_read', True)
            })

        if reverse:
            return list(reversed(notifs))
        else:
            return notifs


class JWT(Base):
    """ Defines a table jwt stored in /tmp/test.db to store the table that is
        jwt for the particular connection
    """
    __tablename__ = 'jwt'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    jwt_flag = Column(Boolean, nullable=False, unique=False)
    connection_name = Column(String(255), nullable=False, unique=True)
    table = Column(String(255), nullable=False, unique=False)
    filter_keys = Column(String(255), nullable=False, unique=False)
    UniqueConstraint('database_name', 'table', name='uix_1')

    # confirm length for the filter key fields ( and find a better way
    # to store the filter keys keep in mind Arrays are not allowed in SQLite)

    filter_keys = Column(String(255), nullable=False)
    create_dt = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))


class Restricted_by_JWT(Base):
    """ Defines a table Restricted_by_JWT to store the tables restricted by a
    JWT for a particular connection/app
    """
    __tablename__ = 'restricted_by_jwt'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    connection_name = Column(String(255), ForeignKey('jwt.connection_name'))
    db_name = Column(String(255), nullable=False)
    restricted_tables = Column(String(1000))


class Deployments(Base):
    """ Defines a table Deployments to store the deployed apps and where they
    have been deployed
    """
    __tablename__ = 'deployments'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    app_name = Column(String(255))
    platfrom = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    # ID of the things & other dicts
    exports = Column(Integer, nullable=False)
    create_dt = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))


class Relationship(Base):
    """ Defines a table Relationships to store the deployed apps and where they
    have been deployed
    """
    __tablename__ = 'relationships'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    app_name = Column(String(255))
    table1_column = Column(String(255), nullable=False)
    relationship = Column(String(255), nullable=False)
    table2_column = Column(String(255), nullable=False)
    UniqueConstraint('id', 'table1_column', 'relationship', 'table2_column',
                     name='uix_1')


class Notifications(Base):
    """ Defines a table Notifications to store the info regarding apps and
    any new events that need to be passes to the user
    """
    __tablename__ = 'notifications'
    __bind_key__ = 'default'

    id = Column(Integer, primary_key=True)
    app_name = Column(String(255))
    user = Column(String(255), nullable=False)
    received_at = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))
    action_status = Column(String(255), nullable=False)
    message = Column(String(255), nullable=False)
    completed_action_at = Column(DateTime(), nullable=True)
    mark_read = Column(Boolean, server_default=text('False'))

    def foramt_notification(self):
        return f'[{self.id}][{self.received_at}]: {self.action_status}\
                 {self.completed_action_at}'

    def create_dict(self):

        if self.completed_action_at is None:
            completed_action_at = None
        else:
            completed_action_at = self.completed_action_at.strftime(
                                                        "%m/%d/%Y, %H:%M:%S")

        return {'id': self.id,
                'app_name': self.app_name,
                'user': self.user,
                'received_at': self.received_at.strftime("%m/%d/%Y, %H:%M:%S"),
                'action_status': self.action_status,
                'message': self.message,
                'completed_action_at': completed_action_at,
                "mark_read": self.mark_read
                }
