"""
Giveaway related model.

Giveaway has:
	Date
	Goods number
	employee (user) id
    client id
"""
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Text

from giveaway.model import DeclarativeBase, metadata, DBSession

class Giveaway(DeclarativeBase):
    __tablename__ = 'giveaway'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    goods_number = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'))
    user_id = Column(Integer, ForeignKey('tg_user.user_id'))