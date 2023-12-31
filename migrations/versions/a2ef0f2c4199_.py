"""empty message

Revision ID: a2ef0f2c4199
Revises: e3e6ed4e00ac
Create Date: 2023-12-11 09:51:27.137557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2ef0f2c4199'
down_revision = 'e3e6ed4e00ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game__room', schema=None) as batch_op:
        batch_op.alter_column('messages',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game__room', schema=None) as batch_op:
        batch_op.alter_column('messages',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)

    # ### end Alembic commands ###
