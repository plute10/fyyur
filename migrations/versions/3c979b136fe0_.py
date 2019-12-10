"""empty message

Revision ID: 3c979b136fe0
Revises: ba9eab566130
Create Date: 2019-12-10 20:28:55.028721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c979b136fe0'
down_revision = 'ba9eab566130'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('date', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'date')
    # ### end Alembic commands ###
