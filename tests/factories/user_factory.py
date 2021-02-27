import factory

from api import db
from api.models import User
from tests.factories import ModelFactory


class UserFactory(ModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Faker("uuid4")
    email = factory.Faker("email")
