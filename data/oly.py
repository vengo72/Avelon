import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Oly(SqlAlchemyBase):
    __tablename__ = 'oly'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    rate = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    last_news = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    materials_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # user_id = sqlalchemy.Column(sqlalchemy.Integer,
    #                             sqlalchemy.ForeignKey("users.id"))
    # user = orm.relationship('User')

    def __repr__(self):
        return f'Название: {self.name}\n' \
               f'Ссылка: {self.link}\n' \
               f'Начало: {self.start}'
