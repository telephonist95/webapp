import sqlalchemy
from .db_session import SqlAlchemyBase


class Building(SqlAlchemyBase):
    __tablename__ = 'buildings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, index=True, unique=True)
    address = sqlalchemy.Column(sqlalchemy.String, unique=True)
    floors_count = sqlalchemy.Column(sqlalchemy.Integer)

    filepath = sqlalchemy.Column(sqlalchemy.String)
