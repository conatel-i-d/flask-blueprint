"""entity

Revision ID: c0619a0269e0
Revises: 
Create Date: 2019-08-09 23:20:50.990471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0619a0269e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'entity',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('purpose', sa.String(255), nullable=False),
    )

def downgrade():
    op.drop_table('entity')
