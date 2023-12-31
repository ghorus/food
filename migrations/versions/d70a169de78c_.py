"""empty message

Revision ID: d70a169de78c
Revises: b01c55321584
Create Date: 2023-12-15 08:43:46.888506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd70a169de78c'
down_revision = 'b01c55321584'
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
