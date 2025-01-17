"""Aggiunto campo lotto a Scatola

Revision ID: 3646aa4d6dea
Revises: 852c3dd4ca71
Create Date: 2024-09-30 12:19:45.126782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3646aa4d6dea'
down_revision = '852c3dd4ca71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scatola', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lotto', sa.String(length=50), nullable=False, server_default='N/A'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scatola', schema=None) as batch_op:
        batch_op.drop_column('lotto')

    # ### end Alembic commands ###
