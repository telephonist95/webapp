import datetime
import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class Floor(SqlAlchemyBase):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    building_number = sqlalchemy.Column(sqlalchemy.Integer)
    floor_number = sqlalchemy.Column(sqlalchemy.Integer)
    number = sqlalchemy.Column(sqlalchemy.Integer)
    rooms_count = sqlalchemy.Column(sqlalchemy.Integer)
    rooms_coords = sqlalchemy.Column(sqlalchemy.String)
