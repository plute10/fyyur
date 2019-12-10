"""empty message

Revision ID: 467424c4f00c
Revises: dee5db872b88
Create Date: 2019-12-10 18:26:05.141007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '467424c4f00c'
down_revision = 'dee5db872b88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('date', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'date')
    # ### end Alembic commands ###
