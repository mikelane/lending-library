import logging

import pytest
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from alembic.command import downgrade, upgrade
from alembic.config import Config
from api import create_app
from api import db as _db
from api import ma
from config import basedir

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def app():
    logger.info("Creating test application")
    test_app = create_app()
    with test_app.app_context():
        yield test_app


@pytest.fixture(scope="session", autouse=True)
def db(app):
    alembic_config_path = basedir / "alembic.ini"
    config = Config(alembic_config_path)
    logger.info("Setting up test database")
    upgrade(config, "head")

    _db.init_app(app)
    ma.init_app(app)
    yield _db

    logger.info("Tearing down Test database")
    downgrade(config, "base")


@pytest.fixture(scope="function")
def session(db):
    logger.info("Setting up database session")
    Session = sessionmaker()
    connection = db.engine.connect()
    trans = connection.begin()
    session = Session(bind=connection)
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction.parent.nested:

            # ensure that state is expired the way
            # session.commit() at the top level normally does
            # (optional step)
            session.expire_all()

            session.begin_nested()

    yield session

    logger.info("Rolling back database session")
    session.close()
    trans.rollback()
    connection.close()
