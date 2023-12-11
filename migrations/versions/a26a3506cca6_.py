"""empty message

Revision ID: a26a3506cca6
Revises: c4e45349edc5
Create Date: 2023-12-10 17:52:06.514204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a26a3506cca6'
down_revision = 'c4e45349edc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###