"""empty message

Revision ID: 9c9329aba976
Revises: b514d7f151a1
Create Date: 2019-12-09 18:33:03.959050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c9329aba976'
down_revision = 'b514d7f151a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shows',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id')
    )
    op.drop_table('shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], name='shows_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='shows_venue_id_fkey'),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id', name='shows_pkey')
    )
    op.drop_table('Shows')
    # ### end Alembic commands ###
