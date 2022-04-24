import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Room(SqlAlchemyBase):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    building_number = sqlalchemy.Column(sqlalchemy.Integer)
    floor_number = sqlalchemy.Column(sqlalchemy.Integer)
    number = sqlalchemy.Column(sqlalchemy.Integer)
