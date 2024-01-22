"""Create Posts Table

Revision ID: 5bca9ca9530f
Revises: 
Create Date: 2024-01-16 15:53:37.047619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bca9ca9530f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('email', sa.String(),
                              unique=True, nullable=False),
                    sa.Column('password', sa.String(), nullable=False))
                  

def downgrade():
    op.drop_table('posts')
