import logging

import pytest
from pytest_factoryboy import register

from alembic.command import downgrade, upgrade
from alembic.config import Config
from api import create_app
from api import db as _db
from config import basedir
from tests.factories import UserFactory

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
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

    yield _db

    logger.info("Tearing down Test database")
    downgrade(config, "base")


@pytest.fixture(scope="function")
def session(db, request):
    db.session.begin_nested()

    def teardown():
        db.session.rollback()
        db.session.close()

    request.addfinalizer(teardown)
    return db.session


register(UserFactory)
