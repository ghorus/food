"""empty message

Revision ID: b01c55321584
Revises: b411ac696e4a
Create Date: 2023-12-15 08:36:24.960837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b01c55321584'
down_revision = 'b411ac696e4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('adlib_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('authors', sa.String(length=30), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('adlib_post', schema=None) as batch_op:
        batch_op.drop_column('authors')

    # ### end Alembic commands ###
