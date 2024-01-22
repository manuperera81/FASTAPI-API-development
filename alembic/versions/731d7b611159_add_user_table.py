"""add user table

Revision ID: 731d7b611159
Revises: da624c823046
Create Date: 2024-01-22 12:26:26.472464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '731d7b611159'
down_revision = 'da624c823046'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')

