"""add content column for the post table

Revision ID: da624c823046
Revises: 5bca9ca9530f
Create Date: 2024-01-22 12:21:26.722827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da624c823046'
down_revision = '5bca9ca9530f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String,nullable= False))


def downgrade():
    op.drop_column('posts','content')
