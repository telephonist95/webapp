import sqlalchemy
from .db_session import SqlAlchemyBase


class Floor(SqlAlchemyBase):
    __tablename__ = 'floors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    building_number = sqlalchemy.Column(sqlalchemy.Integer)
    rooms_count = sqlalchemy.Column(sqlalchemy.Integer)
    rooms_coords = sqlalchemy.Column(sqlalchemy.String)
    
    filepath = sqlalchemy.Column(sqlalchemy.String)
