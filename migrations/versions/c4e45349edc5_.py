"""empty message

Revision ID: c4e45349edc5
Revises: c1e844bf1d3d
Create Date: 2023-12-10 17:43:07.999501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4e45349edc5'
down_revision = 'c1e844bf1d3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
