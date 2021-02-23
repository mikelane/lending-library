"""Create User table

Revision ID: d890997b9101
Revises: 
Create Date: 2021-02-22 06:34:32.713914+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy_utils import EmailType, UUIDType

revision = 'd890997b9101'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', UUIDType, primary_key=True),
        sa.Column('email', EmailType, nullable=False)
    )


def downgrade():
    op.drop_table('user')
