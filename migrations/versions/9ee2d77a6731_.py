"""empty message

Revision ID: 9ee2d77a6731
Revises: 04e431a2b72e
Create Date: 2019-12-10 13:50:23.154083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ee2d77a6731'
down_revision = '04e431a2b72e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'id')
    # ### end Alembic commands ###
