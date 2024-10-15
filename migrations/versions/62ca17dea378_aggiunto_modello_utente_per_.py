"""Aggiunto modello Utente per autenticazione

Revision ID: 62ca17dea378
Revises: f80922cd08ce
Create Date: 2024-10-03 10:50:04.515633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62ca17dea378'
down_revision = 'f80922cd08ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('utente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('ruolo', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('utente', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_utente_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('utente', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_utente_username'))

    op.drop_table('utente')
    # ### end Alembic commands ###
