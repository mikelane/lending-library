import logging

import pytest
import sqlalchemy

from api.models import User

logger = logging.getLogger(__name__)


class TestUserModel:
    class TestNormalCase:
        def it_creates_a_user(self, session, user_factory):
            # GIVEN No user exists in our database
            assert session.query(User).count() == 0

            # WHEN we add a new user
            test_user = user_factory()
            logger.debug(f"Added {test_user=}")

            # THEN the user is persisted in the database
            actual_user = session.query(User).get(test_user.id)
            assert actual_user.id == test_user.id
            assert actual_user.email == test_user.email
            assert repr(actual_user) == f"<User: {test_user.email}>"

    class TestErrorCase:
        def it_requires_a_user_email(self, session):
            with pytest.raises(sqlalchemy.exc.IntegrityError):
                test_user = User()
                session.add(test_user)
                session.commit()
