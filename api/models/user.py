from uuid import uuid4

from sqlalchemy_utils import EmailType, UUIDType

from api import db


class User(db.Model):
    id = db.Column(UUIDType, primary_key=True, default=uuid4)
    email = db.Column(EmailType, nullable=False)

    def __repr__(self):
        return f"<User: {self.email}>"
