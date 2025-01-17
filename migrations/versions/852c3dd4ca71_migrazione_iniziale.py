"""Migrazione iniziale.

Revision ID: 852c3dd4ca71
Revises: 
Create Date: 2024-09-30 11:43:39.171733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '852c3dd4ca71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scatola',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('numero_scatola', sa.Integer(), nullable=False),
    sa.Column('prima_scelta', sa.Float(), nullable=False),
    sa.Column('seconda_scelta', sa.Float(), nullable=False),
    sa.Column('scarti', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scatola')
    # ### end Alembic commands ###
