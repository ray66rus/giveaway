"""
Client related model.

Client has:
    First Name
    Last Name
    Patronymic
    Year of birth
    Code word (optional)
    List of giveaways handled to him/her
"""
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Text

from giveaway.model import DeclarativeBase, metadata, DBSession

class Client(DeclarativeBase):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    patronymic = Column(Text, nullable=False, default='')
    year_of_birth = Column(Integer, nullable=False)
    code_word = Column(Text, nullable=False, default='')
    giveaways = relation('Giveaway', backref='client', lazy='dynamic')

    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', 'patronymic', 'year_of_birth', 'code_word', name='identity'),
    )