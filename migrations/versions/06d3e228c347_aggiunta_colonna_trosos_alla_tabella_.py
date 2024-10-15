"""Aggiunta colonna trosos alla tabella Scatola

Revision ID: 06d3e228c347
Revises: 62ca17dea378
Create Date: 2024-10-15 21:21:24.023087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06d3e228c347'
down_revision = '62ca17dea378'
branch_labels = None
depends_on = None


def upgrade():
    # Aggiungi la colonna 'trosos' con default '0'
    with op.batch_alter_table('scatola', schema=None) as batch_op:
        batch_op.add_column(sa.Column('trosos', sa.Float(), nullable=False, server_default='0'))

    # Rimuovi il server_default per evitare default automatici in futuro
    with op.batch_alter_table('scatola', schema=None) as batch_op:
        batch_op.alter_column('trosos', server_default=None)


def downgrade():
    # Rimuovi la colonna 'trosos'
    with op.batch_alter_table('scatola', schema=None) as batch_op:
        batch_op.drop_column('trosos')
