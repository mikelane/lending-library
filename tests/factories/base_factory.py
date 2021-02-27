from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import scoped_session

from api import db


class ModelFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = scoped_session(lambda: db.session, scopefunc=lambda: db.session)
        sqlalchemy_session_persistence = "commit"
