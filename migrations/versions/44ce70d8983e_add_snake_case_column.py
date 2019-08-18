"""add snake_case column

Revision ID: 44ce70d8983e
Revises: c0619a0269e0
Create Date: 2019-08-17 23:32:48.952959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44ce70d8983e'
down_revision = 'c0619a0269e0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('entity', sa.Column('snake_case', sa.String(255), nullable=True))


def downgrade():
    pass
