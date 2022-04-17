import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Item(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    room_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("rooms.id"))
    building_number = sqlalchemy.Column(sqlalchemy.Integer)
    floor_number = sqlalchemy.Column(sqlalchemy.Integer)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    item_type = sqlalchemy.Column(sqlalchemy.Integer, 
                                  sqlalchemy.ForeignKey("types.id"))
    name = sqlalchemy.Column(sqlalchemy.String)
    room = orm.relation('Room')
    type = orm.relation('Type')
